#!/usr/bin/env python3
"""
小莫 OCR - 本地部署演示（无需API）
直接使用DeepSeek-OCR官方开源代码
"""

from transformers import AutoModel, AutoTokenizer
import torch
import os
from pathlib import Path
from PIL import Image
import time
from typing import Optional, List


class LocalOCR:
    """
    本地OCR引擎
    完全基于GitHub开源代码，无需任何API
    """

    def __init__(self, model_name: str = 'deepseek-ai/DeepSeek-OCR'):
        """
        初始化本地OCR

        Args:
            model_name: 模型名称或本地路径
        """
        self.model_name = model_name
        self.model = None
        self.tokenizer = None
        self.device = 'cuda' if torch.cuda.is_available() else 'cpu'

        print(f"🔧 初始化小莫 OCR (本地模式)")
        print(f"   设备: {self.device}")

    def load_model(self, use_flash_attn: bool = True):
        """
        加载模型到本地

        Args:
            use_flash_attn: 是否使用Flash Attention加速
        """
        print(f"\n📥 正在加载模型: {self.model_name}")
        print(f"   首次运行会自动下载约6.67GB模型文件")
        print(f"   下载后会缓存到: ~/.cache/huggingface/")

        start_time = time.time()

        # 加载Tokenizer
        print("\n⏳ 加载Tokenizer...")
        self.tokenizer = AutoTokenizer.from_pretrained(
            self.model_name,
            trust_remote_code=True
        )
        print("   ✅ Tokenizer 加载完成")

        # 加载模型
        print("\n⏳ 加载模型...")
        model_kwargs = {
            'trust_remote_code': True,
            'use_safetensors': True
        }

        # Flash Attention加速（需要GPU）
        if use_flash_attn and self.device == 'cuda':
            try:
                model_kwargs['_attn_implementation'] = 'flash_attention_2'
                print("   使用 Flash Attention 2 加速")
            except:
                print("   ⚠️  Flash Attention 不可用，使用标准注意力")

        self.model = AutoModel.from_pretrained(
            self.model_name,
            **model_kwargs
        )

        # 移动到设备并设置精度
        if self.device == 'cuda':
            self.model = self.model.cuda().to(torch.bfloat16)
            print(f"   ✅ 模型已加载到GPU (bfloat16)")
        else:
            self.model = self.model.cpu().to(torch.float32)
            print(f"   ✅ 模型已加载到CPU (float32)")

        self.model = self.model.eval()

        load_time = time.time() - start_time
        print(f"\n🎉 模型加载完成！耗时: {load_time:.2f}秒")

        return True

    def recognize(
        self,
        image_path: str,
        mode: str = 'ocr',
        resolution: int = 1024,
        output_dir: Optional[str] = None,
        save_result: bool = False
    ) -> str:
        """
        识别图片中的文字

        Args:
            image_path: 图片路径
            mode: 识别模式
                - 'ocr': 通用OCR识别
                - 'doc2md': 文档转Markdown
                - 'grounding': 带位置信息的OCR
            resolution: 分辨率 (512/768/1024/1280)
            output_dir: 输出目录
            save_result: 是否保存结果

        Returns:
            识别出的文本
        """
        if not self.model:
            raise RuntimeError("模型未加载，请先调用 load_model()")

        print(f"\n🔍 开始识别: {image_path}")
        print(f"   模式: {mode}")
        print(f"   分辨率: {resolution}x{resolution}")

        # 检查图片
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"图片不存在: {image_path}")

        # 构建提示词
        prompts = {
            'ocr': "<image>\nExtract all text from this image.",
            'doc2md': "<image>\n<|grounding|>Convert the document to markdown.",
            'grounding': "<image>\n<|grounding|>Extract text with positions."
        }

        prompt = prompts.get(mode, prompts['ocr'])

        # 设置输出目录
        if output_dir is None:
            output_dir = './outputs'
        os.makedirs(output_dir, exist_ok=True)

        # 执行推理
        start_time = time.time()

        try:
            result = self.model.infer(
                self.tokenizer,
                prompt=prompt,
                image_file=image_path,
                output_path=output_dir,
                base_size=resolution,     # 基础分辨率
                image_size=640,           # 图块大小
                crop_mode=True,           # 启用裁剪模式
                save_results=save_result, # 是否保存结果
                test_compress=True        # 测试压缩
            )

            process_time = time.time() - start_time
            print(f"   ✅ 识别完成，耗时: {process_time:.2f}秒")

            return result

        except Exception as e:
            print(f"   ❌ 识别失败: {e}")
            raise

    def batch_recognize(
        self,
        image_paths: List[str],
        mode: str = 'ocr',
        resolution: int = 1024,
        output_dir: str = './outputs'
    ) -> List[str]:
        """
        批量识别图片

        Args:
            image_paths: 图片路径列表
            mode: 识别模式
            resolution: 分辨率
            output_dir: 输出目录

        Returns:
            识别结果列表
        """
        print(f"\n📦 批量识别模式")
        print(f"   共 {len(image_paths)} 张图片")

        results = []

        for i, image_path in enumerate(image_paths):
            print(f"\n进度: {i+1}/{len(image_paths)}")

            try:
                result = self.recognize(
                    image_path=image_path,
                    mode=mode,
                    resolution=resolution,
                    output_dir=output_dir
                )
                results.append(result)
            except Exception as e:
                print(f"   跳过: {e}")
                results.append(None)

        success_count = sum(1 for r in results if r is not None)
        print(f"\n✅ 批量处理完成")
        print(f"   成功: {success_count}/{len(image_paths)}")

        return results

    def recognize_pdf(
        self,
        pdf_path: str,
        mode: str = 'doc2md',
        resolution: int = 1024,
        output_dir: str = './outputs'
    ) -> str:
        """
        识别PDF文档

        Args:
            pdf_path: PDF文件路径
            mode: 识别模式
            resolution: 分辨率
            output_dir: 输出目录

        Returns:
            合并后的识别结果
        """
        try:
            from pdf2image import convert_from_path
        except ImportError:
            raise ImportError("请安装 pdf2image: pip install pdf2image")

        print(f"\n📄 PDF识别模式")
        print(f"   PDF: {pdf_path}")

        # 转换PDF为图片
        print("\n⏳ 转换PDF为图片...")
        images = convert_from_path(pdf_path)
        print(f"   ✅ 共 {len(images)} 页")

        os.makedirs(output_dir, exist_ok=True)
        all_text = []

        # 逐页处理
        for i, image in enumerate(images):
            print(f"\n📖 处理第 {i+1}/{len(images)} 页")

            # 保存临时图片
            temp_path = os.path.join(output_dir, f"temp_page_{i+1}.jpg")
            image.save(temp_path, 'JPEG')

            # 识别
            try:
                result = self.recognize(
                    image_path=temp_path,
                    mode=mode,
                    resolution=resolution,
                    output_dir=output_dir
                )
                all_text.append(f"\n{'='*60}\n第 {i+1} 页\n{'='*60}\n{result}")
            except Exception as e:
                print(f"   ⚠️  第 {i+1} 页识别失败: {e}")
                all_text.append(f"\n{'='*60}\n第 {i+1} 页 (识别失败)\n{'='*60}\n")

            # 删除临时文件
            try:
                os.remove(temp_path)
            except:
                pass

        # 保存完整结果
        output_file = os.path.join(
            output_dir,
            f"{Path(pdf_path).stem}_full_result.md"
        )

        full_text = '\n'.join(all_text)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(full_text)

        print(f"\n✅ PDF处理完成")
        print(f"   输出文件: {output_file}")

        return full_text


def demo_single_image():
    """演示：单张图片识别"""
    print("\n" + "="*70)
    print("示例 1: 单张图片识别")
    print("="*70)

    # 初始化OCR
    ocr = LocalOCR()
    ocr.load_model()

    # 识别图片（请替换为你的图片路径）
    result = ocr.recognize(
        image_path='test.jpg',
        mode='ocr',
        resolution=1024,
        output_dir='./outputs'
    )

    print(f"\n📝 识别结果:\n{result}")


def demo_batch_images():
    """演示：批量图片识别"""
    print("\n" + "="*70)
    print("示例 2: 批量图片识别")
    print("="*70)

    ocr = LocalOCR()
    ocr.load_model()

    # 批量识别
    image_paths = ['image1.jpg', 'image2.jpg', 'image3.jpg']

    results = ocr.batch_recognize(
        image_paths=image_paths,
        mode='ocr',
        resolution=1024,
        output_dir='./outputs'
    )

    for i, result in enumerate(results):
        if result:
            print(f"\n图片 {i+1} 结果:\n{result[:200]}...")


def demo_pdf():
    """演示：PDF文档识别"""
    print("\n" + "="*70)
    print("示例 3: PDF文档识别")
    print("="*70)

    ocr = LocalOCR()
    ocr.load_model()

    # 识别PDF
    result = ocr.recognize_pdf(
        pdf_path='document.pdf',
        mode='doc2md',
        resolution=1024,
        output_dir='./outputs'
    )

    print(f"\n📝 PDF识别完成，共 {len(result)} 字符")


def demo_different_modes():
    """演示：不同识别模式"""
    print("\n" + "="*70)
    print("示例 4: 不同识别模式对比")
    print("="*70)

    ocr = LocalOCR()
    ocr.load_model()

    image_path = 'test.jpg'

    # 测试不同模式
    modes = ['ocr', 'doc2md', 'grounding']

    for mode in modes:
        print(f"\n{'='*60}")
        print(f"模式: {mode}")
        print(f"{'='*60}")

        result = ocr.recognize(
            image_path=image_path,
            mode=mode,
            resolution=1024
        )

        print(f"结果预览:\n{result[:300]}...")


if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║                                                          ║
    ║         小莫 OCR - 本地部署演示                          ║
    ║         基于 DeepSeek-OCR 开源代码                       ║
    ║         无需API，完全本地运行                            ║
    ║                                                          ║
    ╚══════════════════════════════════════════════════════════╝
    """)

    print("\n请选择演示:")
    print("1. 单张图片识别")
    print("2. 批量图片识别")
    print("3. PDF文档识别")
    print("4. 不同模式对比")
    print("5. 运行所有示例")

    choice = input("\n请输入选项 (1-5): ").strip()

    if choice == '1':
        demo_single_image()
    elif choice == '2':
        demo_batch_images()
    elif choice == '3':
        demo_pdf()
    elif choice == '4':
        demo_different_modes()
    elif choice == '5':
        demo_single_image()
        demo_batch_images()
        demo_pdf()
        demo_different_modes()
    else:
        print("❌ 无效选项")

    print("\n" + "="*70)
    print("✅ 演示完成")
    print("="*70)
