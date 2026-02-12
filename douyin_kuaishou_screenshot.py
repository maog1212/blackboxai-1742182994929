#!/usr/bin/env python3
"""抖音/快手截图工具（manual + openclaw + mobile portal）。"""

from __future__ import annotations

import argparse
import json
import os
import pathlib
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

DEFAULT_VIEWPORT = {"width": 1440, "height": 2560}


@dataclass
class CapturePlan:
    url: str
    selector: str = ""
    full_page: bool = False
    wait_ms: int = 5000


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="抖音/快手截图工具（含 OpenClaw 与移动端下载门户）")

    parser.add_argument("--mode", choices=["manual", "openclaw", "portal"], default="manual")
    parser.add_argument("--platform", choices=["douyin", "kuaishou"], default="douyin")

    parser.add_argument("--url", default="")
    parser.add_argument("--request-text", default="")
    parser.add_argument("--output", default="./shots/output.png")

    parser.add_argument("--browser", choices=["chromium", "firefox", "webkit"], default="chromium")
    parser.add_argument("--headless", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--wait-ms", type=int, default=5000)
    parser.add_argument("--timeout-ms", type=int, default=45000)
    parser.add_argument("--full-page", action="store_true")
    parser.add_argument("--selector", default="")
    parser.add_argument("--state", default="domcontentloaded", choices=["load", "domcontentloaded", "networkidle", "commit"])

    parser.add_argument("--deepseek-api-key", default=os.getenv("DEEPSEEK_API_KEY", ""))
    parser.add_argument("--deepseek-model", default="deepseek-chat")
    parser.add_argument("--deepseek-base-url", default="https://api.deepseek.com")
    parser.add_argument("--dry-run-plan", action="store_true")

    parser.add_argument("--host", default="0.0.0.0", help="portal 模式监听地址")
    parser.add_argument("--port", type=int, default=8765, help="portal 模式端口")
    parser.add_argument("--android-package", default="./mobile_downloads/app-release.apk", help="Android 包路径")
    parser.add_argument("--ios-package", default="./mobile_downloads/app-release.ipa", help="iOS 包路径")

    return parser.parse_args()


def build_openclaw_prompt(platform: str, request_text: str, fallback_url: str) -> str:
    return (
        "你是截图计划生成器。输出 JSON，不要多余文本。\n"
        "schema: {\"url\": string, \"selector\": string, \"full_page\": boolean, \"wait_ms\": number}\n"
        "规则: url 必须 http/https; selector 为空表示整页; wait_ms 1500~12000。\n"
        f"平台: {platform}\n"
        f"用户需求: {request_text}\n"
        f"fallback_url: {fallback_url or 'https://www.douyin.com/'}"
    )


def request_deepseek_plan(
    *,
    api_key: str,
    model: str,
    base_url: str,
    platform: str,
    request_text: str,
    fallback_url: str,
) -> CapturePlan:
    if not api_key:
        raise ValueError("缺少 DeepSeek API Key")
    if not request_text.strip():
        raise ValueError("缺少 request_text")

    endpoint = base_url.rstrip("/") + "/chat/completions"
    payload = {
        "model": model,
        "temperature": 0,
        "messages": [
            {"role": "system", "content": "你只输出 JSON。"},
            {"role": "user", "content": build_openclaw_prompt(platform, request_text, fallback_url)},
        ],
    }
    req = urllib.request.Request(
        endpoint,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"DeepSeek API HTTPError: {exc.code} {detail}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"DeepSeek API URLError: {exc}") from exc

    content = data["choices"][0]["message"]["content"].strip()
    plan_obj = json.loads(content)

    url = str(plan_obj.get("url") or fallback_url or "").strip()
    if not (url.startswith("http://") or url.startswith("https://")):
        raise ValueError(f"非法 URL: {url}")
    wait_ms = max(1500, min(int(plan_obj.get("wait_ms", 5000)), 12000))

    return CapturePlan(
        url=url,
        selector=str(plan_obj.get("selector", "") or ""),
        full_page=bool(plan_obj.get("full_page", False)),
        wait_ms=wait_ms,
    )


def call_deepseek_for_plan(args: argparse.Namespace) -> CapturePlan:
    return request_deepseek_plan(
        api_key=args.deepseek_api_key,
        model=args.deepseek_model,
        base_url=args.deepseek_base_url,
        platform=args.platform,
        request_text=args.request_text,
        fallback_url=args.url,
    )


def run_capture(args: argparse.Namespace, plan: CapturePlan) -> int:
    output_path = pathlib.Path(args.output).expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
        from playwright.sync_api import sync_playwright
    except Exception:
        print("❌ 未检测到 playwright，请先安装：python -m pip install -r requirements.txt", file=sys.stderr)
        return 3

    with sync_playwright() as p:
        browser_launcher = getattr(p, args.browser)
        browser = browser_launcher.launch(headless=args.headless)
        context = browser.new_context(viewport=DEFAULT_VIEWPORT)
        page = context.new_page()

        try:
            page.goto(plan.url, wait_until=args.state, timeout=args.timeout_ms)
            if plan.wait_ms > 0:
                page.wait_for_timeout(plan.wait_ms)

            if plan.selector:
                locator = page.locator(plan.selector)
                locator.first.wait_for(state="visible", timeout=args.timeout_ms)
                locator.first.screenshot(path=str(output_path))
            else:
                page.screenshot(path=str(output_path), full_page=plan.full_page)

            print(f"✅ Screenshot saved: {output_path}")
            return 0
        except PlaywrightTimeoutError as exc:
            print(f"❌ Timeout while loading or locating content: {exc}", file=sys.stderr)
            return 2
        finally:
            context.close()
            browser.close()


def is_openclaw_install_valid(apk_path: pathlib.Path, ipa_path: pathlib.Path) -> tuple[bool, list[str]]:
    errors: list[str] = []
    for package_path, label in ((apk_path, "android"), (ipa_path, "ios")):
        if not package_path.exists():
            errors.append(f"{label} package missing")
            continue
        if package_path.stat().st_size < 20:
            errors.append(f"{label} package corrupted or placeholder too small")
    return len(errors) == 0, errors


def reinstall_openclaw_packages(apk_path: pathlib.Path, ipa_path: pathlib.Path) -> dict[str, str]:
    apk_path.parent.mkdir(parents=True, exist_ok=True)
    ipa_path.parent.mkdir(parents=True, exist_ok=True)
    apk_path.write_text("OpenClaw placeholder APK reinstalled. Replace with real signed package.", encoding="utf-8")
    ipa_path.write_text("OpenClaw placeholder IPA reinstalled. Replace with real signed package.", encoding="utf-8")
    return {"android": str(apk_path), "ios": str(ipa_path)}


def mobile_html() -> str:
    return """<!doctype html>
<html>
<head>
  <meta charset='utf-8'/>
  <meta name='viewport' content='width=device-width,initial-scale=1'/>
  <title>OpenClaw Mobile</title>
  <style>
    body{font-family:-apple-system,BlinkMacSystemFont,Segoe UI,Roboto,sans-serif;background:#0b1020;color:#fff;padding:16px}
    .card{max-width:720px;margin:0 auto;background:#141a33;padding:16px;border-radius:12px}
    .btn{display:block;text-align:center;padding:12px;margin:8px 0;border-radius:10px;background:#4f7cff;color:#fff;text-decoration:none;border:0;width:100%}
    .btn.secondary{background:#2f3a66}
    .muted{opacity:.85;font-size:13px}
    textarea,input,select{width:100%;margin:6px 0 10px;padding:10px;border-radius:8px;border:1px solid #2b335f;background:#0f1530;color:#fff;box-sizing:border-box}
    .ok{color:#9df3b6}.err{color:#ff9ca2}
  </style>
</head>
<body>
  <div class='card'>
    <h2>抖音/快手截图移动端</h2>
    <p class='muted'>支持 Android / iOS 下载入口，兼容 OpenClaw 计划接口。</p>

    <a class='btn' href='/download/android'>下载 Android 安装包 (APK)</a>
    <a class='btn' href='/download/ios'>下载 iOS 安装包 (IPA)</a>
    <button class='btn secondary' onclick='oneClickRepair()'>OpenClaw 一键安装检测 / 修复重装</button>
    <pre id='installOut' class='muted'></pre>

    <hr/>
    <h3>OpenClaw API 配置（可随时更新）</h3>
    <label>API Key</label>
    <input id='apiKey' placeholder='sk-...'/>
    <label>Model</label>
    <input id='apiModel' value='deepseek-chat'/>
    <label>Base URL</label>
    <input id='apiBaseUrl' value='https://api.deepseek.com'/>
    <button class='btn secondary' onclick='updateApiConfig()'>保存并更新 API 配置</button>
    <pre id='cfgOut' class='muted'></pre>

    <hr/>
    <h3>OpenClaw 计划预览</h3>
    <label>平台</label>
    <select id='platform'><option value='douyin'>douyin</option><option value='kuaishou'>kuaishou</option></select>
    <label>URL</label>
    <input id='url' placeholder='https://...'/>
    <label>需求描述</label>
    <textarea id='req' rows='4' placeholder='例如：截取主页第一屏头像和昵称'></textarea>
    <button class='btn' onclick='genPlan()'>生成计划</button>
    <pre id='out' class='muted'></pre>
  </div>

  <script>
    async function oneClickRepair(){
      const r = await fetch('/api/openclaw/install/repair',{method:'POST'});
      const t = await r.text();
      document.getElementById('installOut').textContent=t;
    }
    async function updateApiConfig(){
      const body={
        deepseek_api_key:document.getElementById('apiKey').value,
        deepseek_model:document.getElementById('apiModel').value,
        deepseek_base_url:document.getElementById('apiBaseUrl').value,
      };
      const r = await fetch('/api/openclaw/config',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
      document.getElementById('cfgOut').textContent=await r.text();
    }
    async function genPlan(){
      const body={
        platform:document.getElementById('platform').value,
        url:document.getElementById('url').value,
        request_text:document.getElementById('req').value,
      };
      const r=await fetch('/api/openclaw-plan',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)});
      const t=await r.text();
      document.getElementById('out').textContent=t;
    }
  </script>
</body>
</html>"""


def run_portal_server(args: argparse.Namespace) -> int:
    android_path = pathlib.Path(args.android_package).expanduser().resolve()
    ios_path = pathlib.Path(args.ios_package).expanduser().resolve()
    if not android_path.exists() or not ios_path.exists():
        reinstall_openclaw_packages(android_path, ios_path)

    runtime_config = {
        "deepseek_api_key": args.deepseek_api_key,
        "deepseek_model": args.deepseek_model,
        "deepseek_base_url": args.deepseek_base_url,
        "platform": args.platform,
    }

    class Handler(BaseHTTPRequestHandler):
        def _json(self, payload: Any, status: int = 200) -> None:
            data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)

        def _serve_file(self, file_path: pathlib.Path, content_type: str) -> None:
            if not file_path.exists():
                self.send_error(HTTPStatus.NOT_FOUND, "file not found")
                return
            content = file_path.read_bytes()
            self.send_response(HTTPStatus.OK)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(content)))
            self.send_header("Content-Disposition", f"attachment; filename={file_path.name}")
            self.end_headers()
            self.wfile.write(content)

        def _read_json(self) -> dict[str, Any]:
            length = int(self.headers.get("Content-Length", "0"))
            body = self.rfile.read(length)
            if not body:
                return {}
            return json.loads(body.decode("utf-8"))

        def do_GET(self) -> None:  # noqa: N802
            if self.path == "/":
                html = mobile_html().encode("utf-8")
                self.send_response(HTTPStatus.OK)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(html)))
                self.end_headers()
                self.wfile.write(html)
                return
            if self.path == "/healthz":
                self._json({"ok": True, "mode": "portal"})
                return
            if self.path == "/download/android":
                self._serve_file(android_path, "application/vnd.android.package-archive")
                return
            if self.path == "/download/ios":
                self._serve_file(ios_path, "application/octet-stream")
                return
            if self.path == "/api/openclaw/install/check":
                ok, errors = is_openclaw_install_valid(android_path, ios_path)
                self._json({"ok": ok, "errors": errors, "android": str(android_path), "ios": str(ios_path)})
                return
            self.send_error(HTTPStatus.NOT_FOUND, "not found")

        def do_POST(self) -> None:  # noqa: N802
            if self.path == "/api/openclaw/install/repair":
                before_ok, errors = is_openclaw_install_valid(android_path, ios_path)
                if before_ok:
                    self._json({"ok": True, "message": "OpenClaw 已安装且完整，无需重装"})
                    return
                paths = reinstall_openclaw_packages(android_path, ios_path)
                self._json({"ok": True, "message": "检测到未安装/损坏，已自动重装占位安装包", "previous_errors": errors, "paths": paths})
                return

            if self.path == "/api/openclaw/config":
                try:
                    obj = self._read_json()
                    new_key = str(obj.get("deepseek_api_key", "")).strip()
                    new_model = str(obj.get("deepseek_model", "")).strip()
                    new_base = str(obj.get("deepseek_base_url", "")).strip()
                    if new_key:
                        runtime_config["deepseek_api_key"] = new_key
                    if new_model:
                        runtime_config["deepseek_model"] = new_model
                    if new_base:
                        runtime_config["deepseek_base_url"] = new_base
                    self._json({
                        "ok": True,
                        "message": "API 配置已更新并立即生效",
                        "active": {
                            "deepseek_model": runtime_config["deepseek_model"],
                            "deepseek_base_url": runtime_config["deepseek_base_url"],
                            "has_api_key": bool(runtime_config["deepseek_api_key"]),
                        },
                    })
                except Exception as exc:
                    self._json({"ok": False, "error": str(exc)}, status=400)
                return

            if self.path == "/api/openclaw-plan":
                try:
                    obj = self._read_json()
                    plan = request_deepseek_plan(
                        api_key=runtime_config["deepseek_api_key"],
                        model=runtime_config["deepseek_model"],
                        base_url=runtime_config["deepseek_base_url"],
                        platform=str(obj.get("platform") or runtime_config["platform"]),
                        request_text=str(obj.get("request_text") or ""),
                        fallback_url=str(obj.get("url") or ""),
                    )
                    self._json({"ok": True, "plan": plan.__dict__})
                except Exception as exc:
                    self._json({"ok": False, "error": str(exc)}, status=400)
                return

            self.send_error(HTTPStatus.NOT_FOUND, "not found")

        def log_message(self, fmt: str, *a: Any) -> None:
            return

    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(f"✅ Portal running: http://{args.host}:{args.port}")
    print(f"   Android package: {android_path}")
    print(f"   iOS package: {ios_path}")
    print("   Stop with Ctrl+C")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nPortal stopped.")
    finally:
        server.server_close()
    return 0


def main() -> int:
    args = parse_args()

    try:
        if args.mode == "portal":
            return run_portal_server(args)

        if args.mode == "manual":
            if not args.url.strip():
                print("❌ manual 模式必须提供 --url", file=sys.stderr)
                return 1
            plan = CapturePlan(url=args.url, selector=args.selector, full_page=args.full_page, wait_ms=args.wait_ms)
        else:
            plan = call_deepseek_for_plan(args)
            if args.selector:
                plan.selector = args.selector
            if args.full_page:
                plan.full_page = True
            if args.wait_ms != 5000:
                plan.wait_ms = args.wait_ms

        if args.dry_run_plan:
            print("OpenClaw plan:")
            print(json.dumps(plan.__dict__, ensure_ascii=False, indent=2))
            return 0

        return run_capture(args, plan)
    except Exception as exc:
        print(f"❌ {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
