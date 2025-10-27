#!/bin/bash
# 将小莫 OCR 打包成 macOS .app 应用程序

echo "📦 小莫 OCR - 打包成 .app 应用"
echo "================================"
echo ""

# 检查 py2app
if ! python -c "import py2app" 2>/dev/null; then
    echo "⚠️  py2app 未安装"
    echo "正在安装 py2app..."
    pip install py2app
fi

# 创建 setup.py
cat > setup.py << 'EOF'
from setuptools import setup

APP = ['app/xiaomo_ocr_gui.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'app/icon.icns',  # 如果有图标
    'plist': {
        'CFBundleName': '小莫 OCR',
        'CFBundleDisplayName': '小莫 OCR',
        'CFBundleGetInfoString': "DeepSeek OCR 文字识别工具",
        'CFBundleIdentifier': "com.xiaomo.ocr",
        'CFBundleVersion': "1.0.0",
        'CFBundleShortVersionString': "1.0.0",
        'NSHumanReadableCopyright': "© 2025 小莫 AI",
        'NSHighResolutionCapable': True,
    },
    'packages': ['torch', 'transformers', 'PIL', 'pdf2image'],
    'includes': ['tkinter'],
}

setup(
    app=APP,
    name='小莫 OCR',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
EOF

echo "✅ setup.py 已创建"
echo ""

# 清理旧的构建
echo "🗑️  清理旧构建..."
rm -rf build dist

# 打包
echo "📦 开始打包..."
python setup.py py2app

if [ $? -eq 0 ]; then
    echo ""
    echo "╔══════════════════════════════════════════════════════════╗"
    echo "║                                                          ║"
    echo "║         ✅ 打包成功！                                    ║"
    echo "║                                                          ║"
    echo "╚══════════════════════════════════════════════════════════╝"
    echo ""
    echo "📱 应用程序位置: dist/小莫 OCR.app"
    echo ""
    echo "使用方法:"
    echo "  1. 将 dist/小莫 OCR.app 拖到 应用程序 文件夹"
    echo "  2. 双击启动"
    echo ""
    echo "⚠️  注意:"
    echo "  - 首次运行需要在 系统偏好设置 > 安全性 中允许"
    echo "  - 打包后的应用较大（约 3-4GB），因为包含了 PyTorch"
    echo ""

    # 询问是否打开应用
    read -p "是否打开应用文件夹？(y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        open dist/
    fi
else
    echo ""
    echo "❌ 打包失败，请检查错误信息"
fi

# 清理
rm -f setup.py
