"""
小莫 DeepSeek-OCR 自动系统兼容性检测和配置
自动识别系统环境，选择最佳配置方案
"""

import os
import sys
import platform
import subprocess
import json
from typing import Dict, List, Optional, Tuple


class SystemCompatibility:
    """系统兼容性检测器"""

    def __init__(self):
        self.os_type = platform.system()
        self.os_version = platform.version()
        self.python_version = sys.version_info
        self.architecture = platform.machine()
        self.has_cuda = False
        self.cuda_version = None
        self.gpu_info = []
        self.cpu_info = {}
        self.memory_info = {}
        self.recommended_config = {}

    def detect_all(self) -> Dict:
        """检测所有系统信息"""
        print("=" * 60)
        print("🔍 小莫 OCR - 系统兼容性检测")
        print("=" * 60)

        self._detect_os()
        self._detect_python()
        self._detect_cuda()
        self._detect_gpu()
        self._detect_cpu()
        self._detect_memory()
        self._detect_dependencies()
        self._generate_recommendation()

        return self.get_summary()

    def _detect_os(self):
        """检测操作系统"""
        print(f"\n📱 操作系统: {self.os_type} {self.os_version}")
        print(f"   架构: {self.architecture}")

        if self.os_type == "Linux":
            try:
                with open("/etc/os-release", "r") as f:
                    for line in f:
                        if line.startswith("PRETTY_NAME"):
                            distro = line.split("=")[1].strip().strip('"')
                            print(f"   发行版: {distro}")
                            break
            except:
                pass

    def _detect_python(self):
        """检测 Python 版本"""
        version_str = f"{self.python_version.major}.{self.python_version.minor}.{self.python_version.micro}"
        print(f"\n🐍 Python 版本: {version_str}")

        if self.python_version < (3, 9):
            print("   ⚠️  警告: Python 版本过低，推荐 3.12+")
        elif self.python_version >= (3, 12):
            print("   ✅ Python 版本满足要求")
        else:
            print("   ⚡ Python 版本可用，建议升级到 3.12+")

    def _detect_cuda(self):
        """检测 CUDA"""
        print(f"\n🎮 GPU/CUDA 检测:")

        # 方法1: 使用 nvidia-smi
        try:
            result = subprocess.run(
                ["nvidia-smi", "--query-gpu=driver_version", "--format=csv,noheader"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                driver_version = result.stdout.strip()
                print(f"   NVIDIA 驱动: {driver_version}")
                self.has_cuda = True
        except:
            pass

        # 方法2: 检查 CUDA 工具包
        if self.has_cuda:
            try:
                result = subprocess.run(
                    ["nvcc", "--version"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    for line in result.stdout.split('\n'):
                        if 'release' in line.lower():
                            self.cuda_version = line.split('release')[1].split(',')[0].strip()
                            print(f"   CUDA 版本: {self.cuda_version}")
                            break
            except:
                pass

        # 方法3: 检查 PyTorch CUDA
        try:
            import torch
            if torch.cuda.is_available():
                self.has_cuda = True
                cuda_version = torch.version.cuda
                print(f"   PyTorch CUDA: {cuda_version}")
                print(f"   CUDA 设备数: {torch.cuda.device_count()}")
            else:
                print("   ⚠️  PyTorch 无法使用 CUDA")
        except ImportError:
            print("   ℹ️  PyTorch 未安装")

        if not self.has_cuda:
            print("   ⚠️  未检测到 CUDA，将使用 CPU 模式（速度较慢）")

    def _detect_gpu(self):
        """检测 GPU 信息"""
        if not self.has_cuda:
            return

        print(f"\n💻 GPU 信息:")

        try:
            result = subprocess.run(
                ["nvidia-smi", "--query-gpu=name,memory.total,memory.free",
                 "--format=csv,noheader,nounits"],
                capture_output=True,
                text=True,
                timeout=5
            )

            if result.returncode == 0:
                for line in result.stdout.strip().split('\n'):
                    parts = [p.strip() for p in line.split(',')]
                    if len(parts) == 3:
                        gpu_info = {
                            'name': parts[0],
                            'total_memory': int(parts[1]),
                            'free_memory': int(parts[2])
                        }
                        self.gpu_info.append(gpu_info)
                        print(f"   {gpu_info['name']}")
                        print(f"   └─ 显存: {gpu_info['total_memory']}MB "
                              f"(可用: {gpu_info['free_memory']}MB)")
        except Exception as e:
            print(f"   ⚠️  无法获取详细 GPU 信息: {e}")

    def _detect_cpu(self):
        """检测 CPU 信息"""
        print(f"\n🖥️  CPU 信息:")

        try:
            cpu_count = os.cpu_count() or 0
            print(f"   核心数: {cpu_count}")
            self.cpu_info['count'] = cpu_count

            if self.os_type == "Linux":
                with open("/proc/cpuinfo", "r") as f:
                    for line in f:
                        if "model name" in line:
                            cpu_name = line.split(":")[1].strip()
                            print(f"   型号: {cpu_name}")
                            self.cpu_info['name'] = cpu_name
                            break
            elif self.os_type == "Darwin":  # macOS
                result = subprocess.run(
                    ["sysctl", "-n", "machdep.cpu.brand_string"],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    cpu_name = result.stdout.strip()
                    print(f"   型号: {cpu_name}")
                    self.cpu_info['name'] = cpu_name
        except:
            pass

    def _detect_memory(self):
        """检测内存信息"""
        print(f"\n💾 内存信息:")

        try:
            if self.os_type == "Linux":
                with open("/proc/meminfo", "r") as f:
                    for line in f:
                        if "MemTotal" in line:
                            mem_kb = int(line.split()[1])
                            mem_gb = mem_kb / 1024 / 1024
                            print(f"   总内存: {mem_gb:.1f} GB")
                            self.memory_info['total'] = mem_gb
                        elif "MemAvailable" in line:
                            mem_kb = int(line.split()[1])
                            mem_gb = mem_kb / 1024 / 1024
                            print(f"   可用内存: {mem_gb:.1f} GB")
                            self.memory_info['available'] = mem_gb
                            break

            elif self.os_type == "Darwin":  # macOS
                result = subprocess.run(
                    ["sysctl", "hw.memsize"],
                    capture_output=True,
                    text=True
                )
                if result.returncode == 0:
                    mem_bytes = int(result.stdout.split()[1])
                    mem_gb = mem_bytes / 1024 / 1024 / 1024
                    print(f"   总内存: {mem_gb:.1f} GB")
                    self.memory_info['total'] = mem_gb

            elif self.os_type == "Windows":
                import ctypes
                kernel32 = ctypes.windll.kernel32
                c_ulong = ctypes.c_ulong

                class MEMORYSTATUSEX(ctypes.Structure):
                    _fields_ = [
                        ("dwLength", c_ulong),
                        ("dwMemoryLoad", c_ulong),
                        ("ullTotalPhys", ctypes.c_ulonglong),
                        ("ullAvailPhys", ctypes.c_ulonglong),
                        ("ullTotalPageFile", ctypes.c_ulonglong),
                        ("ullAvailPageFile", ctypes.c_ulonglong),
                        ("ullTotalVirtual", ctypes.c_ulonglong),
                        ("ullAvailVirtual", ctypes.c_ulonglong),
                        ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
                    ]

                memoryStatus = MEMORYSTATUSEX()
                memoryStatus.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
                kernel32.GlobalMemoryStatusEx(ctypes.byref(memoryStatus))

                mem_gb = memoryStatus.ullTotalPhys / 1024 / 1024 / 1024
                avail_gb = memoryStatus.ullAvailPhys / 1024 / 1024 / 1024
                print(f"   总内存: {mem_gb:.1f} GB")
                print(f"   可用内存: {avail_gb:.1f} GB")
                self.memory_info['total'] = mem_gb
                self.memory_info['available'] = avail_gb

        except Exception as e:
            print(f"   ⚠️  无法获取内存信息: {e}")

    def _detect_dependencies(self):
        """检测依赖包"""
        print(f"\n📦 关键依赖检测:")

        dependencies = [
            ('torch', '深度学习框架'),
            ('transformers', 'Transformers 库'),
            ('vllm', 'vLLM 推理引擎'),
            ('PIL', 'Pillow 图像处理'),
            ('flask', 'Flask Web 框架'),
            ('pdf2image', 'PDF 转换工具')
        ]

        for pkg_name, desc in dependencies:
            try:
                if pkg_name == 'PIL':
                    from PIL import Image
                    import PIL
                    version = PIL.__version__
                else:
                    module = __import__(pkg_name)
                    version = getattr(module, '__version__', 'unknown')

                print(f"   ✅ {desc} ({pkg_name}): {version}")
            except ImportError:
                print(f"   ❌ {desc} ({pkg_name}): 未安装")

        # 检查系统工具
        print(f"\n🔧 系统工具检测:")

        tools = [
            ('poppler', 'pdfinfo', 'PDF 处理工具'),
        ]

        for tool_name, command, desc in tools:
            try:
                result = subprocess.run(
                    [command, '--version'],
                    capture_output=True,
                    timeout=2
                )
                if result.returncode == 0:
                    print(f"   ✅ {desc}: 已安装")
                else:
                    print(f"   ❌ {desc}: 未安装")
            except:
                print(f"   ❌ {desc}: 未安装")

    def _generate_recommendation(self):
        """生成推荐配置"""
        print(f"\n" + "=" * 60)
        print("🎯 推荐配置方案")
        print("=" * 60)

        # 推理引擎选择
        if self.has_cuda and self.gpu_info:
            max_memory = max([gpu['total_memory'] for gpu in self.gpu_info])

            if max_memory >= 40000:  # 40GB+
                print("\n✅ 推荐使用: vLLM + GPU (高性能)")
                self.recommended_config['engine'] = 'vllm'
                self.recommended_config['device'] = 'cuda'
                self.recommended_config['resolution'] = '1280x1280'
                self.recommended_config['batch_size'] = 4
            elif max_memory >= 24000:  # 24GB+
                print("\n✅ 推荐使用: vLLM + GPU (标准)")
                self.recommended_config['engine'] = 'vllm'
                self.recommended_config['device'] = 'cuda'
                self.recommended_config['resolution'] = '1024x1024'
                self.recommended_config['batch_size'] = 2
            elif max_memory >= 12000:  # 12GB+
                print("\n⚡ 推荐使用: Transformers + GPU (经济)")
                self.recommended_config['engine'] = 'transformers'
                self.recommended_config['device'] = 'cuda'
                self.recommended_config['resolution'] = '768x768'
                self.recommended_config['batch_size'] = 1
            else:
                print("\n⚠️  GPU 显存不足，推荐使用 CPU 模式")
                self.recommended_config['engine'] = 'transformers'
                self.recommended_config['device'] = 'cpu'
                self.recommended_config['resolution'] = '512x512'
                self.recommended_config['batch_size'] = 1
        else:
            print("\n⚡ 推荐使用: Transformers + CPU (兼容)")
            self.recommended_config['engine'] = 'transformers'
            self.recommended_config['device'] = 'cpu'
            self.recommended_config['resolution'] = '512x512'
            self.recommended_config['batch_size'] = 1

        # 显示详细配置
        print(f"\n配置详情:")
        print(f"  - 推理引擎: {self.recommended_config['engine']}")
        print(f"  - 计算设备: {self.recommended_config['device']}")
        print(f"  - 推荐分辨率: {self.recommended_config['resolution']}")
        print(f"  - 批处理大小: {self.recommended_config['batch_size']}")

        # 性能预估
        self._estimate_performance()

    def _estimate_performance(self):
        """预估性能"""
        print(f"\n📊 性能预估:")

        config = self.recommended_config

        if config['engine'] == 'vllm' and config['device'] == 'cuda':
            if config['resolution'] == '1280x1280':
                print(f"  - 单图处理: ~1-2 秒")
                print(f"  - PDF 页面: ~2500 tokens/秒")
                print(f"  - 日处理量: ~15-20 万页")
            else:
                print(f"  - 单图处理: ~0.5-1 秒")
                print(f"  - PDF 页面: ~2000 tokens/秒")
                print(f"  - 日处理量: ~10-15 万页")
        elif config['engine'] == 'transformers' and config['device'] == 'cuda':
            print(f"  - 单图处理: ~2-5 秒")
            print(f"  - PDF 页面: ~1000 tokens/秒")
            print(f"  - 日处理量: ~5-10 万页")
        else:
            print(f"  - 单图处理: ~10-30 秒")
            print(f"  - PDF 页面: ~100 tokens/秒")
            print(f"  - 日处理量: ~1-2 万页")
            print(f"  ⚠️  CPU 模式速度较慢，建议使用 GPU")

    def get_summary(self) -> Dict:
        """获取检测摘要"""
        return {
            'os': {
                'type': self.os_type,
                'version': self.os_version,
                'architecture': self.architecture
            },
            'python': {
                'version': f"{self.python_version.major}.{self.python_version.minor}.{self.python_version.micro}"
            },
            'cuda': {
                'available': self.has_cuda,
                'version': self.cuda_version
            },
            'gpu': self.gpu_info,
            'cpu': self.cpu_info,
            'memory': self.memory_info,
            'recommended_config': self.recommended_config
        }

    def save_config(self, filepath: str = "auto_config.json"):
        """保存配置到文件"""
        config = self.get_summary()
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        print(f"\n💾 配置已保存到: {filepath}")

    def install_dependencies(self, auto_install: bool = False):
        """安装缺失的依赖"""
        print(f"\n" + "=" * 60)
        print("📦 依赖安装")
        print("=" * 60)

        if not auto_install:
            response = input("\n是否自动安装缺失的依赖? (y/n): ")
            if response.lower() != 'y':
                print("已取消安装")
                return

        print("\n正在安装依赖...")

        # 安装 Python 依赖
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r",
                 "../config/requirements.txt"],
                check=True
            )
            print("✅ Python 依赖安装完成")
        except Exception as e:
            print(f"❌ Python 依赖安装失败: {e}")

        # 安装系统依赖
        if self.os_type == "Linux":
            print("\n请手动安装系统依赖:")
            print("  sudo apt-get install -y poppler-utils")
        elif self.os_type == "Darwin":
            print("\n请手动安装系统依赖:")
            print("  brew install poppler")


def main():
    """主函数"""
    detector = SystemCompatibility()
    summary = detector.detect_all()

    # 保存配置
    detector.save_config()

    print(f"\n" + "=" * 60)
    print("✅ 检测完成")
    print("=" * 60)
    print(f"\n提示:")
    print(f"  1. 配置文件已保存到 auto_config.json")
    print(f"  2. 启动服务时将自动使用推荐配置")
    print(f"  3. 如需手动调整，请编辑配置文件")
    print(f"\n" + "=" * 60)


if __name__ == "__main__":
    main()
