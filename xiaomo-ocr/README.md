# 小莫 - DeepSeek OCR 集成方案

> 基于 DeepSeek-OCR 开源模型的高性能 OCR 文字识别系统

![DeepSeek-OCR](https://img.shields.io/badge/DeepSeek--OCR-3B-blue)
![Python](https://img.shields.io/badge/Python-3.12+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 📖 项目简介

小莫 OCR 是一个基于 DeepSeek 最新开源的 DeepSeek-OCR 模型构建的文字识别系统，提供：

- 🚀 **高速识别** - 单 A100 GPU 日处理 20 万页文档
- 🎯 **高精准度** - 压缩比 10× 下达到 97% 识别精度
- 📄 **多格式支持** - 支持图片（PNG/JPG等）和 PDF 文档
- 🔄 **多种模式** - 通用 OCR、文档转 Markdown、图表解析
- 🌐 **Web 界面** - 简洁美观的前端界面
- 🔌 **RESTful API** - 完整的后端 API 服务

## 🏗️ 项目结构

```
xiaomo-ocr/
├── backend/                # 后端代码
│   ├── deepseek_ocr.py    # DeepSeek-OCR 核心模块
│   └── api_server.py      # Flask API 服务器
├── frontend/               # 前端代码
│   ├── index.html         # Web 界面
│   └── app.js             # 前端交互脚本
├── config/                 # 配置文件
│   └── requirements.txt   # Python 依赖
├── examples/              # 示例代码
├── uploads/               # 上传文件目录
├── outputs/               # 输出结果目录
└── README.md              # 项目文档
```

## 🚀 快速开始

### 1. 环境要求

- **操作系统**: Linux (Ubuntu 20.04+) / macOS / Windows
- **Python**: 3.12+
- **CUDA**: 11.8+ (GPU 推理必需)
- **GPU**: 建议 NVIDIA A100 40G 或更高配置
- **内存**: 建议 16GB+

### 2. 安装依赖

#### 系统依赖 (Ubuntu/Debian)

```bash
sudo apt-get update
sudo apt-get install -y poppler-utils
```

#### 系统依赖 (macOS)

```bash
brew install poppler
```

#### Python 依赖

```bash
cd xiaomo-ocr
pip install -r config/requirements.txt
```

### 3. 启动服务

#### 方式一：使用 vLLM（推荐，速度更快）

```bash
cd backend
python api_server.py
```

服务启动后访问: http://localhost:5000

#### 方式二：使用 Transformers

修改 `api_server.py` 中的初始化参数：

```python
ocr_engine.load_model_transformers()  # 使用 Transformers
```

### 4. 初始化模型

首次使用需要初始化模型（约需 5-10 分钟，取决于网络速度）：

```bash
curl -X POST http://localhost:5000/api/ocr/init \
  -H "Content-Type: application/json" \
  -d '{"use_vllm": true}'
```

或在 Web 界面中点击"服务状态"按钮检查。

### 5. 打开 Web 界面

```bash
cd frontend
python -m http.server 8080
```

访问: http://localhost:8080

## 💻 使用示例

### Web 界面使用

1. 打开 http://localhost:8080
2. 选择识别模式（通用 OCR / 文档转 Markdown / 图表解析）
3. 拖拽或上传图片/PDF 文件
4. 点击"开始识别"
5. 查看识别结果，支持复制和下载

### API 调用示例

#### 1. 单张图片 OCR

```bash
curl -X POST http://localhost:5000/api/ocr/image \
  -F "file=@test.jpg" \
  -F "mode=ocr" \
  -F "resolution=1024x1024"
```

#### 2. PDF 文档识别

```bash
curl -X POST http://localhost:5000/api/ocr/pdf \
  -F "file=@document.pdf" \
  -F "mode=doc2md"
```

#### 3. 批量图片处理

```bash
curl -X POST http://localhost:5000/api/ocr/batch \
  -F "files=@image1.jpg" \
  -F "files=@image2.jpg" \
  -F "files=@image3.jpg" \
  -F "mode=ocr"
```

### Python SDK 使用

```python
from deepseek_ocr import DeepSeekOCR

# 初始化
ocr = DeepSeekOCR()
ocr.load_model_vllm()

# 处理单张图片
result = ocr.process_image_vllm(
    image_path="test.jpg",
    mode="ocr",
    resolution="1024x1024"
)

print(result['text'])

# 处理 PDF
result = ocr.process_pdf(
    pdf_path="document.pdf",
    output_dir="./outputs",
    mode="doc2md"
)

print(f"处理完成，共 {result['total_pages']} 页")
print(f"输出文件: {result['output_file']}")
```

## 🎨 功能特性

### 识别模式

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| **通用 OCR** | 提取图片中的所有文字 | 照片、截图、扫描件 |
| **文档转 Markdown** | 将文档转换为 Markdown 格式 | 书籍、论文、报告 |
| **图表解析** | 解析和描述图表内容 | 统计图、流程图 |

### 分辨率选项

| 分辨率 | Token 数 | 速度 | 精度 | 推荐场景 |
|--------|---------|------|------|----------|
| 512×512 | 64 | ⚡⚡⚡ | ⭐⭐⭐ | 快速预览 |
| 768×768 | 144 | ⚡⚡ | ⭐⭐⭐⭐ | 一般文档 |
| **1024×1024** | 256 | ⚡⚡ | ⭐⭐⭐⭐⭐ | **推荐默认** |
| 1280×1280 | 400 | ⚡ | ⭐⭐⭐⭐⭐ | 高精度需求 |

## 🔧 配置说明

### API 服务器配置

编辑 `backend/api_server.py`:

```python
# 上传文件大小限制
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

# 允许的文件格式
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'pdf'}

# 服务器端口
PORT = 5000
```

### 模型配置

```python
# 使用 HuggingFace 模型（默认）
ocr = DeepSeekOCR(model_path="deepseek-ai/DeepSeek-OCR")

# 使用本地模型
ocr = DeepSeekOCR(model_path="/path/to/local/model")
```

## 📊 性能基准

基于 DeepSeek-OCR 官方数据：

- **模型大小**: 3B 参数
- **处理速度**:
  - 单张图片: ~0.5-2秒 (A100-40G)
  - PDF 页面: ~2500 tokens/sec
  - 日处理量: 20 万页+ (单 A100)
- **识别精度**: 97% (10× 压缩比)
- **显存占用**: ~10GB (推理)

## 🐛 常见问题

### 1. 模型加载失败

**问题**: `Failed to load model`

**解决方案**:
- 检查网络连接，确保可以访问 HuggingFace
- 使用镜像: `export HF_ENDPOINT=https://hf-mirror.com`
- 手动下载模型到本地

### 2. CUDA 内存不足

**问题**: `CUDA out of memory`

**解决方案**:
- 降低分辨率设置
- 使用更大显存的 GPU
- 使用 CPU 模式（速度较慢）

### 3. PDF 转换失败

**问题**: `pdf2image.exceptions.PDFInfoNotInstalledError`

**解决方案**:
```bash
# Ubuntu/Debian
sudo apt-get install poppler-utils

# macOS
brew install poppler
```

### 4. 服务无法启动

**问题**: `Address already in use`

**解决方案**:
```bash
# 查找占用端口的进程
lsof -i :5000

# 杀死进程或更换端口
```

## 🔗 相关资源

- [DeepSeek-OCR GitHub](https://github.com/deepseek-ai/DeepSeek-OCR)
- [DeepSeek-OCR HuggingFace](https://huggingface.co/deepseek-ai/DeepSeek-OCR)
- [DeepSeek 官网](https://www.deepseek.com/)
- [vLLM 文档](https://docs.vllm.ai/)

## 📝 更新日志

### v1.0.0 (2025-10)

- ✅ 集成 DeepSeek-OCR 3B 模型
- ✅ 实现 vLLM 和 Transformers 两种推理方式
- ✅ 提供 RESTful API 服务
- ✅ 开发 Web 前端界面
- ✅ 支持图片和 PDF 识别
- ✅ 支持批量处理
- ✅ 三种识别模式（OCR / Doc2MD / Figure）

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目基于 MIT 许可证开源。

DeepSeek-OCR 模型遵循其原始许可证。

## 💬 联系方式

- 项目主页: https://github.com/your-username/xiaomo-ocr
- 问题反馈: https://github.com/your-username/xiaomo-ocr/issues

---

**小莫 AI** - 让 OCR 识别更简单、更强大 🚀
