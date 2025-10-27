"""
小莫 DeepSeek-OCR API服务器
提供RESTful API接口用于图片和PDF的OCR识别
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
from pathlib import Path
import json
from datetime import datetime
from deepseek_ocr import DeepSeekOCR

app = Flask(__name__)
CORS(app)  # 允许跨域请求

# 配置
UPLOAD_FOLDER = '../uploads'
OUTPUT_FOLDER = '../outputs'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff', 'pdf'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# 确保目录存在
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# 初始化OCR模型（全局单例）
ocr_engine = None


def allowed_file(filename):
    """检查文件扩展名是否允许"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    """API主页"""
    return jsonify({
        "service": "小莫 DeepSeek-OCR API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "POST /api/ocr/image": "处理单张图片",
            "POST /api/ocr/pdf": "处理PDF文件",
            "POST /api/ocr/batch": "批量处理图片",
            "GET /api/status": "获取服务状态",
            "GET /api/results/<task_id>": "获取处理结果"
        }
    })


@app.route('/api/status', methods=['GET'])
def get_status():
    """获取服务状态"""
    global ocr_engine
    return jsonify({
        "status": "ready" if ocr_engine else "initializing",
        "model_loaded": ocr_engine is not None,
        "timestamp": datetime.now().isoformat()
    })


@app.route('/api/ocr/init', methods=['POST'])
def initialize_model():
    """初始化OCR模型"""
    global ocr_engine

    if ocr_engine:
        return jsonify({
            "success": True,
            "message": "模型已经加载"
        })

    try:
        data = request.json or {}
        model_path = data.get('model_path', 'deepseek-ai/DeepSeek-OCR')
        use_vllm = data.get('use_vllm', True)

        ocr_engine = DeepSeekOCR(model_path=model_path)

        if use_vllm:
            success = ocr_engine.load_model_vllm()
        else:
            success = ocr_engine.load_model_transformers()

        if success:
            return jsonify({
                "success": True,
                "message": "模型加载成功",
                "model_path": model_path,
                "method": "vLLM" if use_vllm else "Transformers"
            })
        else:
            return jsonify({
                "success": False,
                "error": "模型加载失败"
            }), 500

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/ocr/image', methods=['POST'])
def ocr_image():
    """处理单张图片OCR"""
    global ocr_engine

    if not ocr_engine:
        return jsonify({
            "success": False,
            "error": "模型未初始化，请先调用 /api/ocr/init"
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

    if not allowed_file(file.filename):
        return jsonify({
            "success": False,
            "error": f"不支持的文件格式，仅支持: {', '.join(ALLOWED_EXTENSIONS)}"
        }), 400

    try:
        # 保存上传的文件
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)

        # 获取参数
        mode = request.form.get('mode', 'ocr')
        resolution = request.form.get('resolution', '1024x1024')
        output_format = request.form.get('output_format', 'markdown')

        # 执行OCR
        if ocr_engine.llm:
            result = ocr_engine.process_image_vllm(
                image_path=filepath,
                mode=mode,
                resolution=resolution,
                output_format=output_format
            )
        else:
            result = ocr_engine.process_image_transformers(
                image_path=filepath,
                output_dir=app.config['OUTPUT_FOLDER']
            )

        # 保存结果
        if result.get('success'):
            result_filename = f"{timestamp}_{Path(filename).stem}_result.json"
            result_filepath = os.path.join(app.config['OUTPUT_FOLDER'], result_filename)
            with open(result_filepath, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)

            result['result_file'] = result_filename

        return jsonify(result)

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/ocr/pdf', methods=['POST'])
def ocr_pdf():
    """处理PDF文件OCR"""
    global ocr_engine

    if not ocr_engine:
        return jsonify({
            "success": False,
            "error": "模型未初始化，请先调用 /api/ocr/init"
        }), 400

    if 'file' not in request.files:
        return jsonify({
            "success": False,
            "error": "没有上传文件"
        }), 400

    file = request.files['file']
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({
            "success": False,
            "error": "仅支持PDF文件"
        }), 400

    try:
        # 保存上传的PDF
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        file.save(filepath)

        # 获取参数
        mode = request.form.get('mode', 'doc2md')

        # 执行PDF OCR
        result = ocr_engine.process_pdf(
            pdf_path=filepath,
            output_dir=app.config['OUTPUT_FOLDER'],
            mode=mode
        )

        return jsonify(result)

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/ocr/batch', methods=['POST'])
def ocr_batch():
    """批量处理图片"""
    global ocr_engine

    if not ocr_engine:
        return jsonify({
            "success": False,
            "error": "模型未初始化，请先调用 /api/ocr/init"
        }), 400

    if 'files' not in request.files:
        return jsonify({
            "success": False,
            "error": "没有上传文件"
        }), 400

    files = request.files.getlist('files')
    if len(files) == 0:
        return jsonify({
            "success": False,
            "error": "文件列表为空"
        }), 400

    try:
        # 保存所有文件
        saved_files = []
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                unique_filename = f"{timestamp}_{filename}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
                file.save(filepath)
                saved_files.append(filepath)

        # 批量处理
        mode = request.form.get('mode', 'ocr')
        results = ocr_engine.batch_process(
            image_paths=saved_files,
            mode=mode
        )

        return jsonify({
            "success": True,
            "total": len(results),
            "results": results
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


@app.route('/api/results/<filename>', methods=['GET'])
def get_result(filename):
    """获取处理结果文件"""
    try:
        filepath = os.path.join(app.config['OUTPUT_FOLDER'], filename)
        if os.path.exists(filepath):
            return send_file(filepath)
        else:
            return jsonify({
                "success": False,
                "error": "文件不存在"
            }), 404
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500


if __name__ == '__main__':
    print("=" * 60)
    print("小莫 DeepSeek-OCR API 服务器")
    print("=" * 60)
    print("启动服务器...")
    print("API地址: http://localhost:5000")
    print("请访问 http://localhost:5000 查看API文档")
    print("=" * 60)

    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
