@echo off
REM DeepSeek OCR 启动脚本 (Windows)

echo DeepSeek OCR - 开源 OCR 桌面应用
echo ==================================
echo.

REM 检查 Python
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到 Python
    echo 请先安装 Python 3.8 或更高版本
    pause
    exit /b 1
)

REM 显示 Python 版本
python --version
echo.

REM 检查依赖
python -c "import PIL" >nul 2>&1
if errorlevel 1 (
    echo 首次运行，正在安装依赖...
    pip install -r requirements.txt
    echo.
)

REM 运行应用
echo 正在启动应用...
python main.py

pause
