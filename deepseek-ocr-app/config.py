"""
配置文件
"""
import os
from pathlib import Path

# 应用配置
APP_NAME = "DeepSeek OCR"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Open Source Community"

# DeepSeek API 配置
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
DEEPSEEK_API_BASE = "https://api.deepseek.com/v1"

# 支持的图片格式
SUPPORTED_IMAGE_FORMATS = [
    ("所有图片", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff *.webp"),
    ("PNG", "*.png"),
    ("JPEG", "*.jpg *.jpeg"),
    ("BMP", "*.bmp"),
    ("GIF", "*.gif"),
    ("TIFF", "*.tiff"),
    ("WebP", "*.webp"),
]

# 应用目录
APP_DIR = Path.home() / ".deepseek-ocr"
HISTORY_DIR = APP_DIR / "history"
CONFIG_FILE = APP_DIR / "config.json"

# 确保目录存在
APP_DIR.mkdir(parents=True, exist_ok=True)
HISTORY_DIR.mkdir(parents=True, exist_ok=True)

# UI 配置
WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 700
FONT_FAMILY = "Microsoft YaHei UI" if os.name == "nt" else "Arial"
FONT_SIZE = 10
