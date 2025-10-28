# DeepSeek OCR - 开源 OCR 桌面应用

一个基于 DeepSeek API 的开源 OCR（光学字符识别）桌面应用程序，提供友好的图形界面，支持多种图片格式的文字识别。

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)

## ✨ 功能特性

- 📷 **多格式支持** - 支持 PNG, JPEG, BMP, GIF, TIFF, WebP 等主流图片格式
- 🎯 **高精度识别** - 基于 DeepSeek 先进的视觉语言模型
- 🎨 **友好界面** - 简洁直观的图形用户界面
- 📋 **便捷操作** - 一键复制识别结果到剪贴板
- 💾 **结果保存** - 支持将识别结果保存为文本文件
- 🔧 **自定义提示词** - 可自定义识别提示词，适应不同场景
- 🖼️ **图片预览** - 实时预览待识别的图片
- 📊 **Token 统计** - 显示 API 调用的 Token 使用情况

## 📋 系统要求

- Python 3.8 或更高版本
- DeepSeek API Key（在 [DeepSeek 平台](https://platform.deepseek.com/api_keys) 获取）

## 🚀 快速开始

### 1. 克隆项目

```bash
git clone https://github.com/yourusername/deepseek-ocr-app.git
cd deepseek-ocr-app
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置 API Key

方式一：通过环境变量（推荐）

```bash
# Linux/macOS
export DEEPSEEK_API_KEY="your_api_key_here"

# Windows (PowerShell)
$env:DEEPSEEK_API_KEY="your_api_key_here"

# Windows (CMD)
set DEEPSEEK_API_KEY=your_api_key_here
```

方式二：通过界面设置

启动应用后，点击「设置 API Key」按钮进行配置。

### 4. 运行应用

```bash
python main.py
```

## 📖 使用说明

### 基本使用流程

1. **设置 API Key**
   - 首次使用需要点击「⚙ 设置 API Key」按钮
   - 输入从 DeepSeek 平台获取的 API Key
   - 点击「保存」

2. **选择图片**
   - 点击「📁 选择图片」按钮
   - 从文件浏览器中选择要识别的图片
   - 图片会在左侧预览区显示

3. **开始识别**
   - （可选）在「提示词」框中自定义识别要求
   - 点击「🔍 开始识别」按钮
   - 等待识别完成，结果会显示在右侧文本框中

4. **处理结果**
   - 点击「📋 复制文本」将结果复制到剪贴板
   - 点击「💾 保存文本」将结果保存为文本文件

### 自定义提示词

默认提示词：`请识别图片中的所有文字内容，保持原有格式和布局。`

你可以根据需求自定义提示词，例如：

- 识别表格：`请识别图片中的表格内容，并以 Markdown 表格格式输出。`
- 识别公式：`请识别图片中的数学公式，使用 LaTeX 格式输出。`
- 提取特定信息：`请提取图片中的身份证号码和姓名。`

## 🏗️ 项目结构

```
deepseek-ocr-app/
├── main.py              # 主应用程序入口
├── ocr_engine.py        # OCR 引擎核心逻辑
├── config.py            # 配置文件
├── requirements.txt     # Python 依赖
├── .env.example         # 环境变量示例
└── README.md           # 项目说明文档
```

## 🔧 配置说明

### 配置文件位置

应用程序会在用户主目录下创建配置文件夹：

- **Linux/macOS**: `~/.deepseek-ocr/`
- **Windows**: `C:\Users\YourName\.deepseek-ocr\`

配置文件结构：

```
.deepseek-ocr/
├── config.json          # API Key 等配置信息
└── history/            # 识别历史记录（未来功能）
```

### 支持的图片格式

- PNG (*.png)
- JPEG (*.jpg, *.jpeg)
- BMP (*.bmp)
- GIF (*.gif)
- TIFF (*.tiff)
- WebP (*.webp)

## 🛠️ 开发说明

### 代码结构

**config.py** - 应用配置管理
- API 端点配置
- 支持的文件格式
- UI 配置参数

**ocr_engine.py** - OCR 核心引擎
- `DeepSeekOCR` 类：封装 DeepSeek API 调用
- `ocr_from_path()`: 从文件路径识别
- `ocr_from_base64()`: 从 base64 编码识别

**main.py** - 主应用程序
- `DeepSeekOCRApp` 类：GUI 应用主类
- 图片显示和预览
- 识别结果处理
- 用户交互逻辑

### 扩展开发

你可以基于此项目进行扩展，例如：

- 批量识别功能
- 识别历史记录
- 多语言支持
- 截图识别
- 表格导出为 Excel
- PDF 文档识别

## 📝 API 说明

### DeepSeek API

本应用使用 DeepSeek Chat API 的视觉能力进行 OCR 识别。

- **API 文档**: https://platform.deepseek.com/docs
- **获取 API Key**: https://platform.deepseek.com/api_keys
- **定价**: 查看 [DeepSeek 定价页面](https://platform.deepseek.com/pricing)

### API 调用示例

```python
from ocr_engine import DeepSeekOCR

# 初始化
ocr = DeepSeekOCR(api_key="your_api_key")

# 识别图片
result = ocr.ocr_from_path(
    image_path="image.png",
    prompt="请识别图片中的所有文字"
)

if result['success']:
    print(result['text'])
    print(f"使用 tokens: {result['tokens_used']}")
else:
    print(f"错误: {result['error']}")
```

## ❓ 常见问题

### Q: 识别速度慢怎么办？

A: 识别速度取决于网络状况和图片大小。建议：
- 使用稳定的网络连接
- 适当调整图片大小（不影响文字清晰度的前提下）

### Q: 识别不准确怎么办？

A: 可以尝试：
- 确保图片清晰，文字对比度高
- 调整自定义提示词，提供更具体的识别要求
- 使用更高质量的图片

### Q: API Key 保存在哪里？

A: API Key 保存在 `~/.deepseek-ocr/config.json`，以明文形式存储。请妥善保管你的 API Key。

### Q: 支持离线使用吗？

A: 本应用依赖 DeepSeek API，需要网络连接才能使用。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

### 贡献指南

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

- [DeepSeek](https://www.deepseek.com/) - 提供强大的 AI 能力
- [Pillow](https://python-pillow.org/) - Python 图像处理库
- [tkinter](https://docs.python.org/3/library/tkinter.html) - Python GUI 库

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 提交 Issue: https://github.com/yourusername/deepseek-ocr-app/issues
- Email: your.email@example.com

## 🔖 更新日志

### v1.0.0 (2025-10-28)

- 首次发布
- 支持基本的 OCR 识别功能
- 图形化用户界面
- 支持多种图片格式
- 自定义提示词功能
- 结果复制和保存功能

---

**注意**: 使用本应用需要 DeepSeek API Key，使用过程中会产生 API 调用费用。请查看 DeepSeek 的定价政策。
