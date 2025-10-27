#!/bin/bash
# 小莫 OCR - macOS 一键安装脚本
# 双击即可运行！

# 获取脚本所在目录
cd "$(dirname "$0")"

# 设置颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印横幅
clear
echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║                                                          ║"
echo "║         小莫 OCR - macOS 一键安装                        ║"
echo "║         DeepSeek OCR 智能文字识别                        ║"
echo "║                                                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# 检查系统
echo -e "${BLUE}📱 检测系统环境...${NC}"
OS_VERSION=$(sw_vers -productVersion)
echo -e "   macOS 版本: ${GREEN}$OS_VERSION${NC}"

# 检查架构
ARCH=$(uname -m)
if [ "$ARCH" = "arm64" ]; then
    echo -e "   处理器: ${GREEN}Apple Silicon (M1/M2/M3)${NC}"
    USE_MPS=true
else
    echo -e "   处理器: ${GREEN}Intel${NC}"
    USE_MPS=false
fi

echo ""

# 步骤1: 检查并安装 Homebrew
echo -e "${BLUE}🍺 步骤 1/5: 检查 Homebrew...${NC}"
if ! command -v brew &> /dev/null; then
    echo -e "${YELLOW}   Homebrew 未安装，正在自动安装...${NC}"
    echo -e "${YELLOW}   这可能需要几分钟，请输入您的密码${NC}"
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

    # 设置环境变量
    if [ "$ARCH" = "arm64" ]; then
        echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
        eval "$(/opt/homebrew/bin/brew shellenv)"
    fi
else
    echo -e "   ${GREEN}✅ Homebrew 已安装${NC}"
fi

echo ""

# 步骤2: 安装系统依赖
echo -e "${BLUE}📦 步骤 2/5: 安装系统依赖...${NC}"

# 安装 Python 3.11
if ! command -v python3.11 &> /dev/null; then
    echo -e "${YELLOW}   正在安装 Python 3.11...${NC}"
    brew install python@3.11
else
    echo -e "   ${GREEN}✅ Python 3.11 已安装${NC}"
fi

# 安装 poppler (PDF支持)
if ! command -v pdfinfo &> /dev/null; then
    echo -e "${YELLOW}   正在安装 Poppler (PDF支持)...${NC}"
    brew install poppler
else
    echo -e "   ${GREEN}✅ Poppler 已安装${NC}"
fi

echo ""

# 步骤3: 创建虚拟环境
echo -e "${BLUE}🐍 步骤 3/5: 创建 Python 环境...${NC}"

# 使用 venv
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}   正在创建虚拟环境...${NC}"
    python3.11 -m venv venv
    echo -e "   ${GREEN}✅ 虚拟环境创建完成${NC}"
else
    echo -e "   ${GREEN}✅ 虚拟环境已存在${NC}"
fi

# 激活虚拟环境
source venv/bin/activate

echo ""

# 步骤4: 安装 Python 依赖
echo -e "${BLUE}📚 步骤 4/5: 安装 Python 库...${NC}"
echo -e "${YELLOW}   这可能需要 10-15 分钟，请耐心等待...${NC}"

# 升级 pip
pip install --upgrade pip

# 根据架构安装不同的依赖
if [ "$ARCH" = "arm64" ]; then
    echo -e "${YELLOW}   为 Apple Silicon 优化安装...${NC}"

    # 安装 PyTorch (支持 MPS)
    pip install torch torchvision torchaudio

else
    echo -e "${YELLOW}   为 Intel 处理器安装...${NC}"

    # 安装 PyTorch (CPU版本)
    pip install torch torchvision torchaudio
fi

# 安装其他依赖
pip install transformers>=4.46.0
pip install Pillow>=10.0.0
pip install pdf2image>=1.16.0
pip install numpy>=1.24.0

# 检查是否成功
if [ $? -eq 0 ]; then
    echo -e "   ${GREEN}✅ Python 库安装完成${NC}"
else
    echo -e "   ${RED}❌ 安装失败，请检查错误信息${NC}"
    exit 1
fi

echo ""

# 步骤5: 下载模型
echo -e "${BLUE}📥 步骤 5/5: 准备 OCR 模型...${NC}"
echo -e "${YELLOW}   首次运行时会自动下载模型（约 6.67GB）${NC}"
echo -e "${YELLOW}   模型会缓存到: ~/.cache/huggingface/${NC}"

# 创建启动脚本
cat > "启动小莫OCR.command" << 'EOFSTART'
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
python app/xiaomo_ocr_gui.py
EOFSTART

chmod +x "启动小莫OCR.command"

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║                                                          ║"
echo "║         ${GREEN}🎉 安装完成！${NC}                                  ║"
echo "║                                                          ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo -e "${GREEN}✅ 所有组件已安装完成！${NC}"
echo ""
echo -e "${BLUE}📝 使用说明:${NC}"
echo "   1. 双击 ${GREEN}启动小莫OCR.command${NC} 打开应用"
echo "   2. 或者在终端运行: ${GREEN}./启动小莫OCR.command${NC}"
echo ""
echo -e "${YELLOW}💡 提示:${NC}"
echo "   - 首次运行会下载模型，请保持网络连接"
echo "   - Apple Silicon 芯片会自动使用 GPU 加速"
echo "   - 所有数据都在本地处理，完全私密"
echo ""
echo -e "${BLUE}按任意键继续...${NC}"
read -n 1

# 询问是否立即启动
echo ""
read -p "是否现在启动小莫 OCR？(y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    ./启动小莫OCR.command
fi
