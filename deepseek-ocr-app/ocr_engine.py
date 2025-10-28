"""
DeepSeek OCR 核心引擎
"""
import base64
import json
import requests
from typing import Optional, Dict, Any
from pathlib import Path
import config


class DeepSeekOCR:
    """DeepSeek OCR 引擎"""

    def __init__(self, api_key: str):
        """
        初始化 OCR 引擎

        Args:
            api_key: DeepSeek API 密钥
        """
        self.api_key = api_key
        self.api_base = config.DEEPSEEK_API_BASE
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def encode_image(self, image_path: str) -> str:
        """
        将图片编码为 base64

        Args:
            image_path: 图片路径

        Returns:
            base64 编码的图片字符串
        """
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def ocr_from_path(self, image_path: str, prompt: str = "请识别图片中的所有文字内容，保持原有格式和布局。") -> Dict[str, Any]:
        """
        从图片路径进行 OCR 识别

        Args:
            image_path: 图片路径
            prompt: 自定义提示词

        Returns:
            包含识别结果的字典
        """
        try:
            # 检查文件是否存在
            if not Path(image_path).exists():
                return {
                    "success": False,
                    "error": f"文件不存在: {image_path}"
                }

            # 编码图片
            base64_image = self.encode_image(image_path)

            # 准备请求数据
            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                "temperature": 0.0,
                "max_tokens": 4096
            }

            # 发送请求
            response = requests.post(
                f"{self.api_base}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=30
            )

            # 检查响应
            if response.status_code == 200:
                result = response.json()
                text = result['choices'][0]['message']['content']
                return {
                    "success": True,
                    "text": text,
                    "tokens_used": result.get('usage', {}),
                    "model": result.get('model', 'deepseek-chat')
                }
            else:
                return {
                    "success": False,
                    "error": f"API 错误: {response.status_code} - {response.text}"
                }

        except Exception as e:
            return {
                "success": False,
                "error": f"识别失败: {str(e)}"
            }

    def ocr_from_base64(self, base64_image: str, prompt: str = "请识别图片中的所有文字内容，保持原有格式和布局。") -> Dict[str, Any]:
        """
        从 base64 编码的图片进行 OCR 识别

        Args:
            base64_image: base64 编码的图片
            prompt: 自定义提示词

        Returns:
            包含识别结果的字典
        """
        try:
            # 准备请求数据
            payload = {
                "model": "deepseek-chat",
                "messages": [
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{base64_image}"
                                }
                            }
                        ]
                    }
                ],
                "temperature": 0.0,
                "max_tokens": 4096
            }

            # 发送请求
            response = requests.post(
                f"{self.api_base}/chat/completions",
                headers=self.headers,
                json=payload,
                timeout=30
            )

            # 检查响应
            if response.status_code == 200:
                result = response.json()
                text = result['choices'][0]['message']['content']
                return {
                    "success": True,
                    "text": text,
                    "tokens_used": result.get('usage', {}),
                    "model": result.get('model', 'deepseek-chat')
                }
            else:
                return {
                    "success": False,
                    "error": f"API 错误: {response.status_code} - {response.text}"
                }

        except Exception as e:
            return {
                "success": False,
                "error": f"识别失败: {str(e)}"
            }
