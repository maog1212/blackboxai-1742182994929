#!/usr/bin/env python3
"""
OpenClaw 全能压缩精华版 — 一键部署 Web 服务器
提供 Web UI + SSE 实时进度推送 + 部署 API
"""

import http.server
import json
import os
import queue
import re
import socketserver
import subprocess
import sys
import threading
import time
import secrets
from pathlib import Path
from urllib.parse import parse_qs, urlparse

PORT = int(os.environ.get("DEPLOY_PORT", 8080))
HOST = os.environ.get("DEPLOY_HOST", "0.0.0.0")
SCRIPT_DIR = Path(__file__).parent.resolve()
DEPLOY_SCRIPT = SCRIPT_DIR / "deploy.sh"

# ── 全局状态 ─────────────────────────────────────────────────────────────────
deploy_state = {
    "status": "idle",       # idle | running | done | error
    "percent": 0,
    "message": "等待部署...",
    "logs": [],
    "access_url": "",
    "token": "",
    "pid": None,
}
state_lock = threading.Lock()
sse_clients: list[queue.Queue] = []


def broadcast_state():
    """向所有 SSE 客户端推送当前状态"""
    with state_lock:
        data = json.dumps({
            "status": deploy_state["status"],
            "percent": deploy_state["percent"],
            "message": deploy_state["message"],
            "access_url": deploy_state["access_url"],
        })
    for q in list(sse_clients):
        try:
            q.put_nowait(data)
        except queue.Full:
            pass


def run_deploy(config: dict):
    """在后台线程中执行部署脚本"""
    global deploy_state

    with state_lock:
        deploy_state["status"] = "running"
        deploy_state["percent"] = 0
        deploy_state["message"] = "正在初始化部署..."
        deploy_state["logs"] = []
        deploy_state["access_url"] = ""
    broadcast_state()

    env = os.environ.copy()
    env["DEPLOY_MODE"] = config.get("mode", "auto")
    env["AI_PROVIDER"] = config.get("provider", "anthropic")
    env["AI_MODEL"] = config.get("model", "")
    env["API_KEY"] = config.get("api_key", "")
    env["OPENCLAW_GATEWAY_PORT"] = str(config.get("port", 18789))

    # 确保脚本可执行
    os.chmod(str(DEPLOY_SCRIPT), 0o755)

    progress_re = re.compile(r'PROGRESS:\{(.+?)\}')

    try:
        process = subprocess.Popen(
            ["bash", str(DEPLOY_SCRIPT)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=env,
            bufsize=1,
            universal_newlines=True,
        )

        with state_lock:
            deploy_state["pid"] = process.pid

        for line in iter(process.stdout.readline, ""):
            line = line.rstrip("\n")

            # 解析进度
            match = progress_re.search(line)
            if match:
                try:
                    prog = json.loads("{" + match.group(1) + "}")
                    with state_lock:
                        deploy_state["percent"] = prog.get("percent", 0)
                        deploy_state["message"] = prog.get("message", "")
                        if prog.get("status") == "done":
                            deploy_state["status"] = "done"
                            # 提取访问地址
                            msg = prog.get("message", "")
                            if "http" in msg:
                                url_start = msg.index("http")
                                deploy_state["access_url"] = msg[url_start:].strip()
                        elif prog.get("status") == "error":
                            deploy_state["status"] = "error"
                    broadcast_state()
                except json.JSONDecodeError:
                    pass
            else:
                with state_lock:
                    deploy_state["logs"].append(line)
                    # 保留最近 500 行
                    if len(deploy_state["logs"]) > 500:
                        deploy_state["logs"] = deploy_state["logs"][-500:]

        process.wait()

        if process.returncode != 0 and deploy_state["status"] != "done":
            with state_lock:
                deploy_state["status"] = "error"
                deploy_state["message"] = f"部署脚本退出码: {process.returncode}"
            broadcast_state()

    except Exception as e:
        with state_lock:
            deploy_state["status"] = "error"
            deploy_state["message"] = f"部署异常: {str(e)}"
        broadcast_state()


class DeployHandler(http.server.SimpleHTTPRequestHandler):
    """处理静态文件和 API 请求"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(SCRIPT_DIR), **kwargs)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/":
            path = "/index.html"

        if path == "/api/status":
            self._handle_status()
        elif path == "/api/events":
            self._handle_sse()
        elif path == "/api/logs":
            self._handle_logs()
        else:
            self.path = path
            super().do_GET()

    def do_POST(self):
        parsed = urlparse(self.path)

        if parsed.path == "/api/deploy":
            self._handle_deploy()
        elif parsed.path == "/api/stop":
            self._handle_stop()
        else:
            self.send_error(404)

    def _read_body(self) -> dict:
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return {}
        body = self.rfile.read(length)
        try:
            return json.loads(body)
        except json.JSONDecodeError:
            return {}

    def _json_response(self, data: dict, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))

    def _handle_status(self):
        with state_lock:
            data = {
                "status": deploy_state["status"],
                "percent": deploy_state["percent"],
                "message": deploy_state["message"],
                "access_url": deploy_state["access_url"],
            }
        self._json_response(data)

    def _handle_logs(self):
        with state_lock:
            logs = list(deploy_state["logs"])
        self._json_response({"logs": logs})

    def _handle_deploy(self):
        with state_lock:
            if deploy_state["status"] == "running":
                self._json_response({"error": "部署正在进行中"}, 409)
                return

        config = self._read_body()

        thread = threading.Thread(target=run_deploy, args=(config,), daemon=True)
        thread.start()

        self._json_response({"ok": True, "message": "部署已启动"})

    def _handle_stop(self):
        with state_lock:
            pid = deploy_state.get("pid")
        if pid:
            try:
                os.kill(pid, 9)
            except ProcessLookupError:
                pass
            with state_lock:
                deploy_state["status"] = "idle"
                deploy_state["message"] = "部署已取消"
                deploy_state["percent"] = 0
            broadcast_state()
        self._json_response({"ok": True})

    def _handle_sse(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "keep-alive")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        q: queue.Queue = queue.Queue(maxsize=50)
        sse_clients.append(q)

        try:
            # 先发送当前状态
            with state_lock:
                init = json.dumps({
                    "status": deploy_state["status"],
                    "percent": deploy_state["percent"],
                    "message": deploy_state["message"],
                    "access_url": deploy_state["access_url"],
                })
            self.wfile.write(f"data: {init}\n\n".encode())
            self.wfile.flush()

            while True:
                try:
                    data = q.get(timeout=15)
                    self.wfile.write(f"data: {data}\n\n".encode())
                    self.wfile.flush()
                except queue.Empty:
                    # 心跳
                    self.wfile.write(": heartbeat\n\n".encode())
                    self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError, OSError):
            pass
        finally:
            if q in sse_clients:
                sse_clients.remove(q)

    def log_message(self, format, *args):
        """静默常规请求日志"""
        pass


class ThreadedHTTPServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
    daemon_threads = True
    allow_reuse_address = True


def main():
    server = ThreadedHTTPServer((HOST, PORT), DeployHandler)
    url = f"http://{'127.0.0.1' if HOST == '0.0.0.0' else HOST}:{PORT}"
    print(f"""
╔══════════════════════════════════════════════════════════╗
║   🦞  OpenClaw 全能压缩精华版 — 一键部署控制台          ║
╠══════════════════════════════════════════════════════════╣
║                                                        ║
║   打开浏览器访问:  {url:<37s}║
║   点击 "一键部署" 按钮即可开始!                         ║
║                                                        ║
║   Ctrl+C 退出                                          ║
╚══════════════════════════════════════════════════════════╝
""")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n正在关闭服务器...")
        server.shutdown()


if __name__ == "__main__":
    main()
