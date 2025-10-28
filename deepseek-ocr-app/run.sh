#!/bin/bash
# DeepSeek OCR 启动脚本 (Linux/macOS)

echo "DeepSeek OCR - 开源 OCR 桌面应用"
echo "=================================="
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "错误: 未找到 Python 3"
    echo "请先安装 Python 3.8 或更高版本"
    exit 1
fi

# 显示 Python 版本
PYTHON_VERSION=$(python3 --version)
echo "使用: $PYTHON_VERSION"
echo ""

# 检查依赖
if ! python3 -c "import PIL" 2>/dev/null; then
    echo "首次运行，正在安装依赖..."
    pip3 install -r requirements.txt
    echo ""
fi

# 运行应用
echo "正在启动应用..."
python3 main.py
