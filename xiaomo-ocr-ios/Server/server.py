#!/usr/bin/env python3
"""
小莫 OCR - iOS 配套服务器
轻量级服务器，可在 Mac 或局域网中运行
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
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
    print("⚠️  DeepSeek-OCR 未安装，将使用模拟模式")

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 配置
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# 全局模型
ocr_model = None
ocr_tokenizer = None
model_loaded = False


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
    """API 主页"""
    return jsonify({
        "service": "小莫 OCR - iOS 服务器",
        "version": "1.0.0",
        "model_loaded": model_loaded,
        "platform": "iOS Compatible",
        "endpoints": {
            "GET /": "API 信息",
            "GET /api/status": "服务器状态",
            "POST /api/ocr/image": "图片识别",
            "POST /api/init": "初始化模型"
        }
    })


@app.route('/api/status')
def status():
    """获取服务器状态"""
    return jsonify({
        "status": "ready" if model_loaded else "initializing",
        "model_loaded": model_loaded,
        "has_dependencies": HAS_DEEPSEEK,
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
    print("=" * 60)
    print("小莫 OCR - iOS 配套服务器")
    print("=" * 60)
    print("")

    if HAS_DEEPSEEK:
        print("✅ DeepSeek-OCR 依赖已安装")
        print("💡 启动后访问 /api/init 初始化模型")
    else:
        print("⚠️  DeepSeek-OCR 未安装，使用演示模式")
        print("💡 可以使用 /api/ocr/demo 测试")

    print("")
    print("服务器配置:")
    print(f"  - 地址: http://0.0.0.0:5000")
    print(f"  - iOS 访问: http://[你的Mac IP]:5000")
    print("")
    print("=" * 60)

    # 启动服务器
    app.run(
        host='0.0.0.0',  # 允许局域网访问
        port=5000,
        debug=True
    )
