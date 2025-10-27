#!/usr/bin/env python3
"""
小莫 DeepSeek-OCR 智能启动脚本
自动检测系统环境并使用最佳配置启动服务
"""

import os
import sys
import json
import subprocess
import time
from pathlib import Path


def print_banner():
    """打印启动横幅"""
    print("\n" + "=" * 70)
    print("""
    ██╗  ██╗██╗ █████╗  ██████╗ ███╗   ███╗ ██████╗
    ╚██╗██╔╝██║██╔══██╗██╔═══██╗████╗ ████║██╔═══██╗
     ╚███╔╝ ██║███████║██║   ██║██╔████╔██║██║   ██║
     ██╔██╗ ██║██╔══██║██║   ██║██║╚██╔╝██║██║   ██║
    ██╔╝ ██╗██║██║  ██║╚██████╔╝██║ ╚═╝ ██║╚██████╔╝
    ╚═╝  ╚═╝╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝ ╚═════╝

    DeepSeek-OCR 智能文字识别系统
    """)
    print("=" * 70 + "\n")


def check_config_file():
    """检查配置文件是否存在"""
    config_path = Path("backend/auto_config.json")
    return config_path.exists()


def run_system_detection():
    """运行系统兼容性检测"""
    print("🔍 首次启动，正在进行系统兼容性检测...\n")

    try:
        result = subprocess.run(
            [sys.executable, "backend/system_compat.py"],
            check=True,
            cwd=os.getcwd()
        )
        return True
    except Exception as e:
        print(f"❌ 系统检测失败: {e}")
        return False


def load_config():
    """加载配置文件"""
    config_path = Path("backend/auto_config.json")

    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        return config
    except Exception as e:
        print(f"❌ 配置文件加载失败: {e}")
        return None


def display_config(config):
    """显示当前配置"""
    print("\n" + "=" * 70)
    print("📋 当前配置")
    print("=" * 70)

    # 系统信息
    os_info = config.get('os', {})
    print(f"\n🖥️  系统环境:")
    print(f"  - 操作系统: {os_info.get('type', 'Unknown')}")
    print(f"  - 架构: {os_info.get('architecture', 'Unknown')}")

    # Python
    python_info = config.get('python', {})
    print(f"  - Python: {python_info.get('version', 'Unknown')}")

    # CUDA
    cuda_info = config.get('cuda', {})
    if cuda_info.get('available'):
        print(f"  - CUDA: {cuda_info.get('version', 'Available')}")
    else:
        print(f"  - CUDA: 不可用")

    # GPU
    gpu_info = config.get('gpu', [])
    if gpu_info:
        print(f"\n💻 GPU 信息:")
        for i, gpu in enumerate(gpu_info):
            print(f"  [{i}] {gpu.get('name', 'Unknown')}")
            print(f"      显存: {gpu.get('total_memory', 0)} MB")

    # 内存
    memory_info = config.get('memory', {})
    if memory_info:
        print(f"\n💾 内存: {memory_info.get('total', 0):.1f} GB")

    # 推荐配置
    rec_config = config.get('recommended_config', {})
    if rec_config:
        print(f"\n⚙️  运行配置:")
        print(f"  - 推理引擎: {rec_config.get('engine', 'unknown')}")
        print(f"  - 计算设备: {rec_config.get('device', 'unknown')}")
        print(f"  - 分辨率: {rec_config.get('resolution', 'unknown')}")
        print(f"  - 批处理: {rec_config.get('batch_size', 1)}")

    print("\n" + "=" * 70)


def check_dependencies():
    """检查关键依赖"""
    print("\n🔍 检查依赖包...")

    required = ['flask', 'torch', 'transformers', 'PIL']
    missing = []

    for pkg in required:
        try:
            if pkg == 'PIL':
                import PIL
            else:
                __import__(pkg)
            print(f"  ✅ {pkg}")
        except ImportError:
            print(f"  ❌ {pkg} - 缺失")
            missing.append(pkg)

    if missing:
        print(f"\n⚠️  缺少依赖: {', '.join(missing)}")
        print(f"请运行: pip install -r config/requirements.txt")
        return False

    return True


def start_backend_server(config):
    """启动后端服务器"""
    print("\n🚀 启动后端服务器...")

    # 设置环境变量
    env = os.environ.copy()

    rec_config = config.get('recommended_config', {})
    if rec_config:
        env['XIAOMO_ENGINE'] = rec_config.get('engine', 'transformers')
        env['XIAOMO_DEVICE'] = rec_config.get('device', 'cpu')
        env['XIAOMO_RESOLUTION'] = rec_config.get('resolution', '1024x1024')
        env['XIAOMO_BATCH_SIZE'] = str(rec_config.get('batch_size', 1))

    try:
        # 启动 Flask 服务器
        backend_process = subprocess.Popen(
            [sys.executable, "backend/api_server.py"],
            env=env,
            cwd=os.getcwd()
        )

        print("✅ 后端服务器启动中...")
        print("   API 地址: http://localhost:5000")

        return backend_process
    except Exception as e:
        print(f"❌ 后端启动失败: {e}")
        return None


def start_frontend_server():
    """启动前端服务器"""
    print("\n🌐 启动前端服务器...")

    try:
        frontend_process = subprocess.Popen(
            [sys.executable, "-m", "http.server", "8080"],
            cwd=os.path.join(os.getcwd(), "frontend")
        )

        print("✅ 前端服务器启动中...")
        print("   访问地址: http://localhost:8080")

        return frontend_process
    except Exception as e:
        print(f"❌ 前端启动失败: {e}")
        return None


def wait_for_server(url: str, timeout: int = 30):
    """等待服务器就绪"""
    import urllib.request
    import urllib.error

    print(f"\n⏳ 等待服务器就绪...")

    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            urllib.request.urlopen(url, timeout=1)
            print("✅ 服务器已就绪")
            return True
        except:
            time.sleep(1)
            print(".", end="", flush=True)

    print("\n⚠️  服务器启动超时")
    return False


def main():
    """主函数"""
    print_banner()

    # 检查或运行系统检测
    if not check_config_file():
        print("ℹ️  首次运行，需要进行系统兼容性检测\n")
        if not run_system_detection():
            print("\n❌ 系统检测失败，请检查错误信息")
            sys.exit(1)

    # 加载配置
    config = load_config()
    if not config:
        print("❌ 无法加载配置文件")
        sys.exit(1)

    # 显示配置
    display_config(config)

    # 检查依赖
    if not check_dependencies():
        print("\n❌ 依赖检查失败，请先安装依赖")
        sys.exit(1)

    # 确认启动
    print("\n" + "=" * 70)
    response = input("是否启动服务? (Y/n): ")
    if response.lower() == 'n':
        print("已取消启动")
        sys.exit(0)

    # 启动服务
    print("\n" + "=" * 70)
    print("🚀 启动小莫 OCR 服务")
    print("=" * 70)

    backend_process = start_backend_server(config)
    if not backend_process:
        print("❌ 后端服务启动失败")
        sys.exit(1)

    # 等待后端就绪
    time.sleep(3)

    frontend_process = start_frontend_server()
    if not frontend_process:
        print("❌ 前端服务启动失败")
        backend_process.terminate()
        sys.exit(1)

    # 显示使用说明
    print("\n" + "=" * 70)
    print("✅ 服务启动成功")
    print("=" * 70)
    print("""
📝 使用说明:
  1. 访问 http://localhost:8080 使用 Web 界面
  2. 后端 API: http://localhost:5000
  3. 首次使用需要初始化模型 (约需 5-10 分钟)

⌨️  快捷键:
  - Ctrl+C: 停止服务

📚 文档: 查看 README.md 获取详细说明
    """)
    print("=" * 70)

    # 等待中断
    try:
        backend_process.wait()
    except KeyboardInterrupt:
        print("\n\n⏹️  正在停止服务...")
        backend_process.terminate()
        frontend_process.terminate()
        print("✅ 服务已停止")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ 启动失败: {e}")
        sys.exit(1)
