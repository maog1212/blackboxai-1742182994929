"""
小莫 DeepSeek-OCR 核心模块
提供图片和PDF的OCR文字识别功能
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Optional, Union
from PIL import Image
import time


class DeepSeekOCR:
    """DeepSeek-OCR 核心类"""

    def __init__(self, model_path: str = "deepseek-ai/DeepSeek-OCR"):
        """
        初始化DeepSeek-OCR模型

        Args:
            model_path: 模型路径，默认从HuggingFace加载
        """
        self.model_path = model_path
        self.model = None
        self.tokenizer = None
        self.llm = None

    def load_model_vllm(self):
        """使用vLLM加载模型（推荐，速度更快）"""
        try:
            from vllm import LLM, SamplingParams
            from vllm.model_executor.models.deepseek_ocr import NGramPerReqLogitsProcessor

            print("正在使用vLLM加载DeepSeek-OCR模型...")
            self.llm = LLM(
                model=self.model_path,
                enable_prefix_caching=False,
                mm_processor_cache_gb=0,
                logits_processors=[NGramPerReqLogitsProcessor],
                trust_remote_code=True,
            )
            print("模型加载成功！")
            return True
        except Exception as e:
            print(f"vLLM加载失败: {e}")
            return False

    def load_model_transformers(self):
        """使用Transformers加载模型（备用方案）"""
        try:
            from transformers import AutoModel, AutoTokenizer

            print("正在使用Transformers加载DeepSeek-OCR模型...")
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_path,
                trust_remote_code=True
            )
            self.model = AutoModel.from_pretrained(
                self.model_path,
                trust_remote_code=True,
                device_map="auto"
            )
            print("模型加载成功！")
            return True
        except Exception as e:
            print(f"Transformers加载失败: {e}")
            return False

    def process_image_vllm(
        self,
        image_path: str,
        mode: str = "ocr",
        resolution: str = "1024x1024",
        output_format: str = "markdown"
    ) -> Dict[str, any]:
        """
        使用vLLM处理单张图片

        Args:
            image_path: 图片路径
            mode: 处理模式 - ocr(通用OCR), doc2md(文档转markdown), figure(图表解析)
            resolution: 分辨率 - 512x512, 768x768, 1024x1024, 1280x1280
            output_format: 输出格式 - text, markdown, json

        Returns:
            包含OCR结果的字典
        """
        if not self.llm:
            return {
                "success": False,
                "error": "模型未加载，请先调用load_model_vllm()"
            }

        try:
            from vllm import SamplingParams

            # 构建提示词
            if mode == "doc2md":
                prompt = "Convert this document to markdown format."
            elif mode == "figure":
                prompt = "Parse and describe this figure/chart."
            else:
                prompt = "Extract all text from this image."

            # 准备输入
            inputs = {
                "prompt": prompt,
                "multi_modal_data": {
                    "image": Image.open(image_path)
                }
            }

            # 设置采样参数
            sampling_params = SamplingParams(
                temperature=0.0,
                max_tokens=8192,
            )

            # 执行推理
            start_time = time.time()
            outputs = self.llm.generate(inputs, sampling_params)
            process_time = time.time() - start_time

            # 提取结果
            result_text = outputs[0].outputs[0].text if outputs else ""

            return {
                "success": True,
                "text": result_text,
                "mode": mode,
                "resolution": resolution,
                "image_path": image_path,
                "process_time": f"{process_time:.2f}s",
                "output_format": output_format
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "image_path": image_path
            }

    def process_image_transformers(
        self,
        image_path: str,
        output_dir: Optional[str] = None,
        compress_ratio: float = 10.0
    ) -> Dict[str, any]:
        """
        使用Transformers处理单张图片

        Args:
            image_path: 图片路径
            output_dir: 输出目录
            compress_ratio: 压缩比例

        Returns:
            包含OCR结果的字典
        """
        if not self.model or not self.tokenizer:
            return {
                "success": False,
                "error": "模型未加载，请先调用load_model_transformers()"
            }

        try:
            # 执行推理
            start_time = time.time()
            result = self.model.infer(
                image_path=image_path,
                output_dir=output_dir,
                compress_ratio=compress_ratio
            )
            process_time = time.time() - start_time

            return {
                "success": True,
                "text": result,
                "image_path": image_path,
                "process_time": f"{process_time:.2f}s",
                "compress_ratio": compress_ratio
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "image_path": image_path
            }

    def process_pdf(
        self,
        pdf_path: str,
        output_dir: str,
        mode: str = "doc2md"
    ) -> Dict[str, any]:
        """
        处理PDF文件

        Args:
            pdf_path: PDF文件路径
            output_dir: 输出目录
            mode: 处理模式

        Returns:
            包含处理结果的字典
        """
        try:
            from pdf2image import convert_from_path

            # 将PDF转换为图片
            print(f"正在转换PDF: {pdf_path}")
            images = convert_from_path(pdf_path)

            results = []
            total_text = []

            # 处理每一页
            for i, image in enumerate(images):
                print(f"处理第 {i+1}/{len(images)} 页...")

                # 保存临时图片
                temp_image_path = os.path.join(output_dir, f"temp_page_{i+1}.jpg")
                image.save(temp_image_path, "JPEG")

                # 执行OCR
                if self.llm:
                    result = self.process_image_vllm(temp_image_path, mode=mode)
                else:
                    result = self.process_image_transformers(temp_image_path)

                if result["success"]:
                    total_text.append(f"\n--- Page {i+1} ---\n{result['text']}")
                    results.append(result)

                # 删除临时文件
                os.remove(temp_image_path)

            # 保存完整结果
            output_file = os.path.join(output_dir, f"{Path(pdf_path).stem}_ocr.md")
            with open(output_file, "w", encoding="utf-8") as f:
                f.write("\n".join(total_text))

            return {
                "success": True,
                "pdf_path": pdf_path,
                "total_pages": len(images),
                "output_file": output_file,
                "results": results
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "pdf_path": pdf_path
            }

    def batch_process(
        self,
        image_paths: List[str],
        mode: str = "ocr"
    ) -> List[Dict[str, any]]:
        """
        批量处理多张图片

        Args:
            image_paths: 图片路径列表
            mode: 处理模式

        Returns:
            结果列表
        """
        results = []

        for i, image_path in enumerate(image_paths):
            print(f"处理 {i+1}/{len(image_paths)}: {image_path}")

            if self.llm:
                result = self.process_image_vllm(image_path, mode=mode)
            else:
                result = self.process_image_transformers(image_path)

            results.append(result)

        return results


# 示例使用函数
def demo_usage():
    """演示如何使用DeepSeek-OCR"""

    # 初始化OCR
    ocr = DeepSeekOCR()

    # 方式1: 使用vLLM（推荐）
    if ocr.load_model_vllm():
        # 处理单张图片
        result = ocr.process_image_vllm(
            image_path="test.jpg",
            mode="ocr",
            resolution="1024x1024"
        )
        print(result)

    # 方式2: 使用Transformers
    elif ocr.load_model_transformers():
        result = ocr.process_image_transformers(
            image_path="test.jpg",
            output_dir="./outputs"
        )
        print(result)


if __name__ == "__main__":
    demo_usage()
