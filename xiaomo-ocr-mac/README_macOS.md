# 小莫 OCR - macOS 版本

> 🍎 专为 macOS 优化的 DeepSeek-OCR 文字识别工具
> 📦 开箱即用，无需复杂部署
> 🚀 支持 Apple Silicon (M1/M2/M3) GPU 加速

## ✨ 特性

- ✅ **开箱即用** - 双击安装，自动配置所有依赖
- ✅ **图形界面** - 简洁美观的原生 macOS 风格界面
- ✅ **GPU 加速** - Apple Silicon 自动使用 Metal Performance Shaders
- ✅ **本地运行** - 完全本地处理，数据 100% 隐私
- ✅ **无需 API** - 基于开源模型，不需要任何 API 密钥
- ✅ **离线可用** - 模型下载后可完全离线使用

## 📋 系统要求

### 最低配置
- macOS 11.0 (Big Sur) 或更高版本
- 8GB 内存
- 10GB 可用存储空间（用于模型和依赖）
- 网络连接（仅首次下载模型时需要）

### 推荐配置
- macOS 13.0 (Ventura) 或更高版本
- Apple Silicon (M1/M2/M3) 芯片
- 16GB 或更多内存
- 20GB 可用存储空间

## 🚀 快速开始

### 方法一：双击安装（推荐）

1. **下载并解压**
   ```bash
   # 如果从 Git 下载
   cd xiaomo-ocr-mac
   ```

2. **双击运行安装脚本**
   ```
   📁 找到文件: 一键安装.command
   🖱️ 双击运行（或右键 -> 打开）
   ```

   如果提示"无法打开"：
   - 右键点击文件
   - 选择"打开"
   - 点击"打开"确认

3. **等待自动安装**
   - 脚本会自动安装 Homebrew（如果未安装）
   - 自动安装 Python 3.11 和依赖
   - 创建虚拟环境
   - 安装所有必需的库

4. **启动应用**
   ```
   安装完成后，双击: 启动小莫OCR.command
   ```

### 方法二：命令行安装

```bash
# 1. 克隆或下载项目
cd xiaomo-ocr-mac

# 2. 运行安装脚本
chmod +x 一键安装.command
./一键安装.command

# 3. 启动应用
./启动小莫OCR.command
```

## 📖 使用指南

### 启动应用

**方式1：双击启动**
```
📁 找到: 启动小莫OCR.command
🖱️ 双击运行
```

**方式2：命令行启动**
```bash
cd xiaomo-ocr-mac
./启动小莫OCR.command
```

### 基本操作

1. **加载模型**
   - 点击 `⚡ 加载模型` 按钮
   - 首次运行会自动下载模型（约 6.67GB）
   - 等待加载完成（状态变为🟢 模型已就绪）

2. **添加文件**
   - 点击 `📁 添加图片` 选择图片文件
   - 或点击 `📄 添加 PDF` 选择 PDF 文档
   - 支持格式: JPG, PNG, PDF, BMP, TIFF

3. **选择模式**
   - **通用 OCR**: 提取所有文字
   - **文档转 Markdown**: 转换为 Markdown 格式
   - **图表解析**: 解析图表内容

4. **选择分辨率**
   - `512 (快速)`: 最快，适合预览
   - `768 (均衡)`: 速度与质量平衡
   - `1024 (推荐)`: 推荐设置
   - `1280 (精确)`: 最高精度

5. **开始识别**
   - 点击 `🚀 开始识别`
   - 等待处理完成
   - 结果显示在下方文本框

6. **保存结果**
   - 点击 `💾 保存结果`
   - 选择保存位置和格式

## 🎯 高级功能

### 批量处理

一次添加多个文件，应用会自动依次处理所有文件。

### 快捷键（计划中）

- `⌘ + O`: 打开文件
- `⌘ + S`: 保存结果
- `⌘ + L`: 加载模型
- `⌘ + R`: 开始识别

## 📦 打包成独立应用

如果你想将应用打包成 `.app` 格式：

```bash
# 1. 运行打包脚本
./打包成App.sh

# 2. 等待打包完成
# 打包后的应用在: dist/小莫 OCR.app

# 3. 拖到应用程序文件夹
mv dist/小莫\ OCR.app /Applications/

# 4. 在启动台中找到并运行
```

**注意**: 打包后的应用较大（3-4GB），因为包含了 PyTorch 等库。

## 🔧 问题排查

### 1. 安装脚本无法运行

**问题**: 双击后提示"无法打开"

**解决**:
```bash
# 方法1: 右键 -> 打开
右键点击文件 -> 选择"打开" -> 点击"打开"

# 方法2: 命令行授权
cd xiaomo-ocr-mac
chmod +x 一键安装.command
./一键安装.command
```

### 2. Homebrew 安装失败

**问题**: 网络问题导致 Homebrew 安装失败

**解决**:
```bash
# 使用国内镜像安装 Homebrew
/bin/bash -c "$(curl -fsSL https://gitee.com/ineo6/homebrew-install/raw/master/install.sh)"
```

### 3. 模型下载缓慢

**问题**: HuggingFace 下载速度慢

**解决**:
```bash
# 设置 HuggingFace 镜像
export HF_ENDPOINT=https://hf-mirror.com

# 然后重新启动应用
./启动小莫OCR.command
```

### 4. 内存不足

**问题**: 运行时提示内存不足

**解决**:
- 关闭其他占用内存的应用
- 降低分辨率设置（使用 512 或 768）
- 一次只处理少量文件

### 5. Apple Silicon GPU 未启用

**问题**: Apple Silicon 但未使用 GPU

**解决**:
```bash
# 检查 PyTorch MPS 支持
python3 -c "import torch; print(torch.backends.mps.is_available())"

# 如果显示 False，重新安装 PyTorch
pip install --upgrade torch torchvision torchaudio
```

## 📊 性能基准

### Apple Silicon (M1/M2/M3)

| 分辨率 | 单图耗时 | 精度 | 显存占用 |
|--------|---------|------|---------|
| 512×512 | ~1-2秒 | ⭐⭐⭐ | ~2GB |
| 768×768 | ~2-3秒 | ⭐⭐⭐⭐ | ~3GB |
| 1024×1024 | ~3-5秒 | ⭐⭐⭐⭐⭐ | ~4GB |
| 1280×1280 | ~5-8秒 | ⭐⭐⭐⭐⭐ | ~6GB |

### Intel Mac (CPU)

| 分辨率 | 单图耗时 | 精度 |
|--------|---------|------|
| 512×512 | ~5-10秒 | ⭐⭐⭐ |
| 768×768 | ~10-15秒 | ⭐⭐⭐⭐ |
| 1024×1024 | ~15-25秒 | ⭐⭐⭐⭐⭐ |

## 🗂️ 文件结构

```
xiaomo-ocr-mac/
├── 一键安装.command          # 🔥 双击安装所有依赖
├── 启动小莫OCR.command        # 🔥 双击启动应用
├── 打包成App.sh              # 打包成 .app 应用
├── README_macOS.md          # 本文档
├── requirements-mac.txt     # Python 依赖
├── app/
│   └── xiaomo_ocr_gui.py    # 图形界面主程序
├── venv/                    # Python 虚拟环境（安装后生成）
└── scripts/                 # 辅助脚本
```

## 💡 使用技巧

### 1. 首次使用优化

- 首次运行会下载 6.67GB 模型，建议在 WiFi 环境下进行
- 模型会缓存到 `~/.cache/huggingface/`
- 可以提前手动下载模型放到此目录

### 2. 提升识别精度

- 使用高分辨率设置（1024 或 1280）
- 确保输入图片清晰、光线充足
- 避免图片倾斜或扭曲

### 3. 加快处理速度

- Apple Silicon 用户自动使用 GPU 加速
- 批量处理时一次不要添加太多文件（建议 < 50 个）
- 使用较低分辨率（512 或 768）

### 4. PDF 处理技巧

- 大型 PDF 建议拆分成小文件处理
- 扫描版 PDF 识别效果更好
- 电子版 PDF 可以直接复制文字，无需 OCR

## 🔗 相关资源

- **官方 GitHub**: https://github.com/deepseek-ai/DeepSeek-OCR
- **HuggingFace**: https://huggingface.co/deepseek-ai/DeepSeek-OCR
- **问题反馈**: 提交 Issue 到项目仓库

## 📄 许可证

本项目基于 MIT 许可证开源。

DeepSeek-OCR 模型遵循其原始许可证。

## 🙏 致谢

- [DeepSeek AI](https://www.deepseek.com/) - 提供开源 OCR 模型
- [HuggingFace](https://huggingface.co/) - 模型托管平台
- [PyTorch](https://pytorch.org/) - 深度学习框架

---

**小莫 OCR** - 让 OCR 识别更简单 🚀

适用于 macOS | 完全本地运行 | 开源免费
