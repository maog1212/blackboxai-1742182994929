#!/usr/bin/env python3
"""
小莫 OCR - iOS 配套服务器
轻量级服务器，可在 Mac 或局域网中运行
"""

from flask import Flask, request, jsonify, send_from_directory, render_template_string
from flask_cors import CORS
import os
import socket
from pathlib import Path
import time
from datetime import datetime

# 尝试导入 OCR 模块
try:
    from transformers import AutoModel, AutoTokenizer
    import torch
    HAS_DEEPSEEK = True
except ImportError:
    HAS_DEEPSEEK = False
    print("⚠️  DeepSeek-OCR 未安装，将使用演示模式")

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 配置
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 全局模型
ocr_model = None
ocr_tokenizer = None
model_loaded = False


def get_local_ip():
    """获取本机局域网 IP"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"


# 欢迎页面 HTML
WELCOME_PAGE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>小莫 OCR 服务器</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            padding: 20px;
        }
        .container {
            max-width: 600px;
            width: 100%;
        }
        .card {
            background: rgba(255, 255, 255, 0.15);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 40px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
        }
        h1 {
            font-size: 42px;
            margin-bottom: 10px;
            text-align: center;
        }
        .subtitle {
            text-align: center;
            opacity: 0.9;
            margin-bottom: 30px;
            font-size: 18px;
        }
        .status {
            background: rgba(72, 187, 120, 0.2);
            border: 2px solid rgba(72, 187, 120, 0.5);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 30px;
            text-align: center;
        }
        .status-dot {
            display: inline-block;
            width: 12px;
            height: 12px;
            background: #48bb78;
            border-radius: 50%;
            margin-right: 8px;
            animation: pulse 2s ease-in-out infinite;
        }
        @keyframes pulse {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.5; }
        }
        .info-section {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
        }
        .info-title {
            font-weight: 600;
            font-size: 18px;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
        }
        .info-item {
            display: flex;
            justify-content: space-between;
            padding: 12px 0;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        }
        .info-item:last-child {
            border-bottom: none;
        }
        .info-label {
            opacity: 0.8;
        }
        .info-value {
            font-weight: 600;
            font-family: monospace;
        }
        .url-box {
            background: rgba(0, 0, 0, 0.2);
            border-radius: 8px;
            padding: 15px;
            text-align: center;
            font-size: 20px;
            font-weight: 600;
            font-family: monospace;
            margin: 20px 0;
            cursor: pointer;
            transition: all 0.3s;
        }
        .url-box:hover {
            background: rgba(0, 0, 0, 0.3);
        }
        .qr-code {
            background: white;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            margin: 20px 0;
        }
        .qr-code img {
            max-width: 200px;
            height: auto;
        }
        .instructions {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            padding: 20px;
            line-height: 1.8;
        }
        .step {
            margin-bottom: 15px;
            padding-left: 30px;
            position: relative;
        }
        .step-number {
            position: absolute;
            left: 0;
            top: 0;
            background: white;
            color: #667eea;
            width: 24px;
            height: 24px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 14px;
        }
        .button {
            background: white;
            color: #667eea;
            border: none;
            border-radius: 8px;
            padding: 12px 24px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            width: 100%;
            margin-top: 20px;
            transition: all 0.3s;
        }
        .button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <h1>🚀 小莫 OCR</h1>
            <div class="subtitle">服务器运行中</div>

            <div class="status">
                <span class="status-dot"></span>
                <span>服务正常运行</span>
            </div>

            <div class="info-section">
                <div class="info-title">📱 iPhone 访问地址</div>
                <div class="url-box" onclick="copyUrl()" title="点击复制">
                    {{ webapp_url }}
                </div>
                <div style="text-align: center; font-size: 14px; opacity: 0.8;">
                    点击可复制地址
                </div>
            </div>

            <div class="info-section">
                <div class="info-title">ℹ️ 服务器信息</div>
                <div class="info-item">
                    <span class="info-label">本机 IP</span>
                    <span class="info-value">{{ local_ip }}</span>
                </div>
                <div class="info-item">
                    <span class="info-label">端口</span>
                    <span class="info-value">5000</span>
                </div>
                <div class="info-item">
                    <span class="info-label">模型状态</span>
                    <span class="info-value">{{ model_status }}</span>
                </div>
            </div>

            <div class="instructions">
                <div class="info-title">📖 使用步骤</div>
                <div class="step">
                    <div class="step-number">1</div>
                    确保 iPhone 和 Mac 在同一 WiFi
                </div>
                <div class="step">
                    <div class="step-number">2</div>
                    在 iPhone Safari 中打开上面的地址
                </div>
                <div class="step">
                    <div class="step-number">3</div>
                    首次访问会自动检测并连接服务器
                </div>
                <div class="step">
                    <div class="step-number">4</div>
                    开始拍照识别文字！
                </div>
            </div>

            <button class="button" onclick="testConnection()">
                测试连接
            </button>

            <div style="margin-top: 20px; text-align: center; font-size: 14px; opacity: 0.7;">
                API 文档: <a href="/api/status" style="color: white; text-decoration: underline;">/api/status</a>
            </div>
        </div>
    </div>

    <script>
        function copyUrl() {
            const url = '{{ webapp_url }}';
            navigator.clipboard.writeText(url).then(() => {
                alert('✅ 地址已复制到剪贴板！\\n\\n在 iPhone Safari 中粘贴访问');
            });
        }

        function testConnection() {
            fetch('/api/status')
                .then(r => r.json())
                .then(data => {
                    alert('✅ 服务器连接正常！\\n\\n状态: ' + data.status);
                })
                .catch(e => {
                    alert('❌ 连接失败: ' + e.message);
                });
        }
    </script>
</body>
</html>
"""


def load_model():
    """加载 DeepSeek-OCR 模型"""
    global ocr_model, ocr_tokenizer, model_loaded

    if not HAS_DEEPSEEK:
        print("❌ 无法加载模型：缺少依赖")
        return False

    if model_loaded:
        return True

    try:
        print("📥 正在加载 DeepSeek-OCR 模型...")

        model_name = 'deepseek-ai/DeepSeek-OCR'

        print("   加载 Tokenizer...")
        ocr_tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            trust_remote_code=True
        )

        print("   加载模型...")
        ocr_model = AutoModel.from_pretrained(
            model_name,
            trust_remote_code=True,
            use_safetensors=True
        )

        # 检测设备
        if torch.cuda.is_available():
            device = 'cuda'
            ocr_model = ocr_model.cuda().to(torch.bfloat16)
        elif torch.backends.mps.is_available():
            device = 'mps'
            ocr_model = ocr_model.to('mps')
        else:
            device = 'cpu'
            ocr_model = ocr_model.cpu().to(torch.float32)

        ocr_model = ocr_model.eval()

        model_loaded = True
        print(f"✅ 模型加载成功！设备: {device.upper()}")
        return True

    except Exception as e:
        print(f"❌ 模型加载失败: {e}")
        return False


@app.route('/')
def index():
    """欢迎页面"""
    local_ip = get_local_ip()
    webapp_url = f"http://{local_ip}:5000/webapp"
    model_status = "已加载" if model_loaded else ("演示模式" if not HAS_DEEPSEEK else "未加载")

    return render_template_string(
        WELCOME_PAGE,
        local_ip=local_ip,
        webapp_url=webapp_url,
        model_status=model_status
    )


@app.route('/webapp')
def webapp():
    """Web 应用"""
    return send_from_directory('../WebApp', 'index.html')


@app.route('/api/status')
def status():
    """获取服务器状态"""
    return jsonify({
        "status": "ready" if model_loaded else "initializing",
        "model_loaded": model_loaded,
        "has_dependencies": HAS_DEEPSEEK,
        "local_ip": get_local_ip(),
        "timestamp": datetime.now().isoformat()
    })


@app.route('/api/init', methods=['POST'])
def init_model():
    """初始化模型"""
    if model_loaded:
        return jsonify({
            "success": True,
            "message": "模型已经加载"
        })

    success = load_model()

    if success:
        return jsonify({
            "success": True,
            "message": "模型加载成功"
        })
    else:
        return jsonify({
            "success": False,
            "error": "模型加载失败"
        }), 500


@app.route('/api/ocr/image', methods=['POST'])
def ocr_image():
    """识别图片"""
    global ocr_model, ocr_tokenizer

    # 检查模型
    if not model_loaded:
        return jsonify({
            "success": False,
            "error": "模型未加载，请先调用 /api/init"
        }), 400

    # 检查文件
    if 'file' not in request.files:
        return jsonify({
            "success": False,
            "error": "没有上传文件"
        }), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({
            "success": False,
            "error": "文件名为空"
        }), 400

    try:
        # 保存文件
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{file.filename}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # 获取参数
        mode = request.form.get('mode', 'general')
        resolution = request.form.get('resolution', '1024x1024')
        base_size = int(resolution.split('x')[0])

        # 构建提示词
        if mode == 'doc2md':
            prompt = "<image>\n<|grounding|>Convert the document to markdown."
        elif mode == 'figure':
            prompt = "<image>\n<|grounding|>Parse this figure/chart."
        else:
            prompt = "<image>\nExtract all text from this image."

        # 执行 OCR
        start_time = time.time()

        result = ocr_model.infer(
            ocr_tokenizer,
            prompt=prompt,
            image_file=filepath,
            base_size=base_size,
            image_size=640,
            crop_mode=True
        )

        process_time = time.time() - start_time

        # 删除临时文件
        os.remove(filepath)

        return jsonify({
            "success": True,
            "text": result,
            "mode": mode,
            "resolution": resolution,
            "process_time": f"{process_time:.2f}s"
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/ocr/demo', methods=['POST'])
def ocr_demo():
    """演示模式（无需真实模型）"""
    # 用于测试 iOS 应用，无需加载模型
    file = request.files.get('file')
    mode = request.form.get('mode', 'general')

    demo_texts = {
        'general': '这是一段识别出的文字示例。\n\n小莫 OCR 可以准确识别图片中的文字内容，支持多种语言和格式。',
        'doc2md': '# 文档标题\n\n这是一个转换为 Markdown 格式的文档示例。\n\n## 子标题\n\n- 列表项 1\n- 列表项 2\n- 列表项 3',
        'figure': '图表识别结果：\n\n这是一个柱状图，显示了 2023 年各月销售数据。\n- 1月：100\n- 2月：150\n- 3月：200'
    }

    return jsonify({
        "success": True,
        "text": demo_texts.get(mode, demo_texts['general']),
        "mode": mode,
        "process_time": "0.5s",
        "demo": True
    })


if __name__ == '__main__':
    local_ip = get_local_ip()

    print("=" * 70)
    print("")
    print("   🚀 小莫 OCR - iOS 服务器")
    print("")
    print("=" * 70)
    print("")

    if HAS_DEEPSEEK:
        print("✅ DeepSeek-OCR 依赖已安装")
        print("💡 启动后访问 http://localhost:5000/api/init 初始化模型")
    else:
        print("⚠️  DeepSeek-OCR 未安装，使用演示模式")
        print("💡 可以使用 /api/ocr/demo 测试")

    print("")
    print("📱 iPhone 访问地址:")
    print(f"   http://{local_ip}:5000/webapp")
    print("")
    print("🖥️  浏览器访问 (查看配置):")
    print(f"   http://localhost:5000")
    print("")
    print("💡 提示:")
    print("   - 确保 iPhone 和 Mac 在同一 WiFi")
    print("   - 首次访问会自动检测连接")
    print("   - 配置会保存在浏览器中")
    print("")
    print("=" * 70)

    # 启动服务器
    app.run(
        host='0.0.0.0',  # 允许局域网访问
        port=5000,
        debug=False  # 生产模式
    )
