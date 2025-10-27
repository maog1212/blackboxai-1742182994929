# 小莫 OCR - macOS 专版 🍎

> **开箱即用的 OCR 文字识别工具 - 专为苹果电脑优化**

[![macOS](https://img.shields.io/badge/macOS-11.0+-blue.svg)](https://www.apple.com/macos/)
[![Python](https://img.shields.io/badge/Python-3.11-green.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 项目特点

### ✅ 真正的开箱即用

- **双击安装** - 无需手动配置环境
- **一键启动** - 双击即可运行，无需命令行
- **自动配置** - 自动安装所有依赖和模型
- **图形界面** - 简洁美观的原生 macOS 界面

### 🚀 性能优化

- **Apple Silicon 加速** - M1/M2/M3 自动使用 GPU
- **内存优化** - 针对 macOS 内存管理优化
- **快速响应** - 原生 Python GUI，响应迅速
- **离线可用** - 模型下载后完全离线运行

### 🔒 隐私安全

- **完全本地** - 所有数据本地处理
- **无需 API** - 不需要任何 API 密钥
- **数据不上传** - 100% 隐私保护
- **开源透明** - 代码完全开源

## 📦 快速开始

### 1️⃣ 下载项目

```bash
git clone <repository-url>
cd xiaomo-ocr-mac
```

### 2️⃣ 双击安装

```
找到文件: 一键安装.command
双击运行即可！
```

如果提示无法打开：
- 右键 → 打开 → 再次点击 "打开"

### 3️⃣ 双击启动

```
找到文件: 启动小莫OCR.command
双击运行即可！
```

就这么简单！🎉

## 📸 界面预览

```
┌─────────────────────────────────────────────────┐
│  🤖 小莫 OCR                      🟢 模型已就绪 │
│  基于 DeepSeek-OCR 的智能文字识别               │
├─────────────────────────────────────────────────┤
│                                                 │
│  控制面板                                       │
│  ┌──────────────────────────────────────────┐  │
│  │ 识别模式: ◉通用OCR ○文档转MD ○图表解析  │  │
│  │ 分辨率:   [1024 (推荐) ▼]                │  │
│  └──────────────────────────────────────────┘  │
│                                                 │
│  文件选择                                       │
│  ┌──────────────────────────────────────────┐  │
│  │ [文件列表]                                │  │
│  │                                           │  │
│  └──────────────────────────────────────────┘  │
│  [📁 添加图片] [📄 添加PDF] [🗑️ 清空列表]     │
│                                                 │
│  [⚡ 加载模型]  [🚀 开始识别]  [💾 保存结果]   │
│                                                 │
│  识别结果                                       │
│  ┌──────────────────────────────────────────┐  │
│  │                                           │  │
│  │  识别出的文字内容...                      │  │
│  │                                           │  │
│  └──────────────────────────────────────────┘  │
│                                                 │
│  就绪                    🖥️ arm64 (支持GPU加速) │
└─────────────────────────────────────────────────┘
```

## 💻 系统要求

### 最低配置
- macOS 11.0 (Big Sur) 或更高
- 8GB 内存
- 10GB 可用空间

### 推荐配置
- macOS 13.0 (Ventura) 或更高
- Apple Silicon (M1/M2/M3)
- 16GB 内存
- 20GB 可用空间

## 📖 使用说明

### 基本流程

1. **启动应用** - 双击 `启动小莫OCR.command`
2. **加载模型** - 点击 "⚡ 加载模型" 按钮
3. **添加文件** - 点击 "📁 添加图片" 或 "📄 添加PDF"
4. **选择设置** - 选择识别模式和分辨率
5. **开始识别** - 点击 "🚀 开始识别"
6. **保存结果** - 点击 "💾 保存结果"

### 识别模式

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| **通用 OCR** | 提取所有文字 | 照片、截图、扫描件 |
| **文档转 Markdown** | 转为 MD 格式 | 书籍、文档、报告 |
| **图表解析** | 解析图表 | 统计图、流程图 |

### 分辨率设置

| 分辨率 | 速度 | 精度 | Apple Silicon 耗时 | Intel 耗时 |
|--------|------|------|-------------------|-----------|
| 512 | ⚡⚡⚡⚡ | ⭐⭐⭐ | ~1-2秒 | ~5-10秒 |
| 768 | ⚡⚡⚡ | ⭐⭐⭐⭐ | ~2-3秒 | ~10-15秒 |
| **1024** | ⚡⚡ | ⭐⭐⭐⭐⭐ | ~3-5秒 | ~15-25秒 |
| 1280 | ⚡ | ⭐⭐⭐⭐⭐ | ~5-8秒 | ~25-40秒 |

## 🔧 高级功能

### 打包成 .app 应用

想要更原生的体验？可以打包成独立的 macOS 应用：

```bash
./打包成App.sh
```

打包后：
- 应用位置：`dist/小莫 OCR.app`
- 可拖到"应用程序"文件夹
- 在启动台中启动

⚠️ 注意：打包后的应用约 3-4GB（包含 PyTorch）

### 命令行使用

如果你喜欢命令行：

```bash
# 激活环境
source venv/bin/activate

# 运行 Python 脚本
python app/xiaomo_ocr_gui.py
```

## 🐛 问题排查

### 安装相关

**Q: 双击安装脚本没反应？**
```bash
# 授予执行权限
chmod +x 一键安装.command
./一键安装.command
```

**Q: Homebrew 安装失败？**
```bash
# 使用国内镜像
/bin/bash -c "$(curl -fsSL https://gitee.com/ineo6/homebrew-install/raw/master/install.sh)"
```

### 运行相关

**Q: 模型下载很慢？**
```bash
# 设置 HuggingFace 镜像
export HF_ENDPOINT=https://hf-mirror.com
./启动小莫OCR.command
```

**Q: 内存不足？**
- 关闭其他应用
- 降低分辨率（使用 512 或 768）
- 减少批量文件数量

**Q: Apple Silicon 未使用 GPU？**
```bash
# 检查 MPS 支持
python3 -c "import torch; print(torch.backends.mps.is_available())"

# 重新安装 PyTorch
pip install --upgrade torch torchvision torchaudio
```

## 📁 项目结构

```
xiaomo-ocr-mac/
├── 一键安装.command          # 🔥 双击安装
├── 启动小莫OCR.command        # 🔥 双击启动
├── 快速开始.txt              # 新手指南
├── README.md                 # 本文档
├── README_macOS.md           # 详细文档
├── 打包成App.sh              # 打包脚本
├── requirements-mac.txt      # Python 依赖
├── app/
│   └── xiaomo_ocr_gui.py    # 主程序
└── venv/                    # 虚拟环境（安装后）
```

## 🌟 特色亮点

### 相比其他 OCR 工具

| 特性 | 小莫 OCR | 其他工具 |
|------|---------|---------|
| 安装难度 | ⭐ 双击安装 | ⭐⭐⭐⭐ 需配置环境 |
| 使用方式 | 图形界面 | 命令行 |
| Apple Silicon | ✅ GPU 加速 | ❌ 仅 CPU |
| 隐私保护 | ✅ 完全本地 | ⚠️ 部分上传 |
| 费用 | ✅ 完全免费 | 💰 部分收费 |
| API 依赖 | ✅ 无需 API | ⚠️ 需要 API |

### 为什么选择小莫 OCR？

1. **真正开箱即用** - 其他方案需要配置 Python、CUDA、虚拟环境等，小莫 OCR 只需双击
2. **原生 macOS 优化** - 专为 macOS 优化，支持 Apple Silicon GPU 加速
3. **隐私第一** - 完全本地运行，不上传任何数据
4. **完全免费** - 基于开源模型，无任何费用
5. **持续更新** - 跟随 DeepSeek-OCR 更新

## 📚 相关资源

- **官方模型**: [DeepSeek-OCR GitHub](https://github.com/deepseek-ai/DeepSeek-OCR)
- **模型下载**: [HuggingFace](https://huggingface.co/deepseek-ai/DeepSeek-OCR)
- **问题反馈**: [GitHub Issues](https://github.com/your-repo/issues)

## 📝 更新日志

### v1.0.0 (2025-10)
- ✅ 首次发布
- ✅ macOS 一键安装脚本
- ✅ 原生图形界面
- ✅ Apple Silicon GPU 支持
- ✅ 三种识别模式
- ✅ 批量处理功能
- ✅ PDF 支持

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

## 🙏 致谢

- [DeepSeek AI](https://www.deepseek.com/) - 开源 OCR 模型
- [HuggingFace](https://huggingface.co/) - 模型托管
- [PyTorch](https://pytorch.org/) - 深度学习框架
- [Tkinter](https://docs.python.org/3/library/tkinter.html) - GUI 框架

---

**小莫 OCR** - 让文字识别变得简单 🚀

Made with ❤️ for macOS
