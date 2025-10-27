# 小莫 OCR - 本地部署指南（无需API）

> 完全基于GitHub开源代码的本地部署方案

## 📦 官方开源仓库

DeepSeek-OCR 是完全开源的项目，无需任何API密钥！

**官方GitHub**: https://github.com/deepseek-ai/DeepSeek-OCR
**HuggingFace**: https://huggingface.co/deepseek-ai/DeepSeek-OCR

## 🚀 方案一：使用官方源代码（推荐）

### 1. 克隆官方仓库

```bash
# 克隆DeepSeek-OCR官方仓库
git clone https://github.com/deepseek-ai/DeepSeek-OCR.git
cd DeepSeek-OCR
```

### 2. 创建Python环境

```bash
# 创建conda环境
conda create -n deepseek-ocr python=3.12.9 -y
conda activate deepseek-ocr
```

### 3. 安装依赖

```bash
# 安装PyTorch (CUDA 11.8)
pip install torch==2.6.0 torchvision==0.21.0 --index-url https://download.pytorch.org/whl/cu118

# 安装其他依赖
pip install transformers==4.46.3
pip install tokenizers==0.20.3
pip install einops
pip install addict
pip install easydict
pip install flash-attn==2.7.3
pip install Pillow
pip install vllm==0.8.5
```

### 4. 直接使用官方代码

#### 方式 A: 使用 Transformers（最简单）

创建文件 `simple_ocr.py`:

```python
from transformers import AutoModel, AutoTokenizer
import torch
import os

# 设置GPU
os.environ["CUDA_VISIBLE_DEVICES"] = '0'

# 加载模型（首次会自动从HuggingFace下载，约6.67GB）
model_name = 'deepseek-ai/DeepSeek-OCR'
print("正在加载模型...")

tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
model = AutoModel.from_pretrained(
    model_name,
    _attn_implementation='flash_attention_2',  # 使用Flash Attention加速
    trust_remote_code=True,
    use_safetensors=True
)

# 模型加载到GPU并设置为半精度
model = model.eval().cuda().to(torch.bfloat16)
print("✅ 模型加载完成！")

# OCR识别
def ocr_image(image_path, output_dir='./outputs', mode='ocr'):
    """
    OCR识别函数

    Args:
        image_path: 图片路径
        output_dir: 输出目录
        mode: 识别模式
            - 'ocr': 通用OCR
            - 'doc2md': 文档转Markdown
            - 'grounding': 带坐标的OCR
    """

    # 构建提示词
    if mode == 'doc2md':
        prompt = "<image>\n<|grounding|>Convert the document to markdown."
    elif mode == 'grounding':
        prompt = "<image>\n<|grounding|>Extract text with positions."
    else:
        prompt = "<image>\nExtract all text from the image."

    # 执行推理
    result = model.infer(
        tokenizer,
        prompt=prompt,
        image_file=image_path,
        output_path=output_dir,
        base_size=1024,      # 基础分辨率
        image_size=640,      # 图块大小
        crop_mode=True,      # 启用裁剪模式
        save_results=True,   # 保存结果
        test_compress=True   # 测试压缩
    )

    return result

# 使用示例
if __name__ == "__main__":
    # 识别单张图片
    result = ocr_image('test.jpg', output_dir='./outputs', mode='ocr')
    print("\n识别结果:")
    print(result)
```

运行：

```bash
python simple_ocr.py
```

#### 方式 B: 使用 vLLM（高性能）

官方仓库已经提供了vLLM版本，在 `DeepSeek-OCR-vllm/` 目录下：

```bash
cd DeepSeek-OCR-vllm

# 修改配置
vim config.py  # 设置输入输出路径

# 处理图片
python run_dpsk_ocr_image.py

# 处理PDF
python run_dpsk_ocr_pdf.py
```

官方vLLM代码示例：

```python
from vllm import LLM, SamplingParams
from vllm.model_executor.models.deepseek_ocr import NGramPerReqLogitsProcessor

# 初始化vLLM
llm = LLM(
    model="deepseek-ai/DeepSeek-OCR",
    enable_prefix_caching=False,
    mm_processor_cache_gb=0,
    logits_processors=[NGramPerReqLogitsProcessor],
    trust_remote_code=True
)

# 设置采样参数
sampling_params = SamplingParams(
    temperature=0.0,
    max_tokens=8192
)

# 准备输入
inputs = {
    "prompt": "Extract text from this image",
    "multi_modal_data": {"image": "path/to/image.jpg"}
}

# 执行推理（速度超快！）
outputs = llm.generate(inputs, sampling_params)
print(outputs[0].outputs[0].text)
```

## 🔧 方案二：使用Rust版本（无需Python）

如果你不想配置Python环境，还有Rust版本！

```bash
# 克隆Rust实现
git clone https://github.com/TimmyOVO/deepseek-ocr.rs.git
cd deepseek-ocr.rs

# 编译（或直接下载预编译版本）
cargo build --release

# 直接运行
./target/release/deepseek-ocr --image test.jpg
```

## 📖 完整使用示例

### 示例1: 批量处理图片

```python
import os
from glob import glob
from simple_ocr import ocr_image

# 批量处理目录下所有图片
image_dir = './images'
output_dir = './outputs'

for image_path in glob(f"{image_dir}/*.jpg"):
    print(f"处理: {image_path}")
    result = ocr_image(image_path, output_dir, mode='ocr')
    print(f"✅ 完成")
```

### 示例2: 处理PDF文档

```python
from pdf2image import convert_from_path
from simple_ocr import ocr_image
import os

def ocr_pdf(pdf_path, output_dir):
    """处理PDF文件"""

    # PDF转图片
    print(f"转换PDF: {pdf_path}")
    images = convert_from_path(pdf_path)

    all_text = []

    # 逐页处理
    for i, image in enumerate(images):
        print(f"处理第 {i+1}/{len(images)} 页...")

        # 保存临时图片
        temp_path = f"{output_dir}/temp_page_{i}.jpg"
        image.save(temp_path, 'JPEG')

        # OCR识别
        result = ocr_image(temp_path, output_dir, mode='doc2md')
        all_text.append(f"\n--- 第 {i+1} 页 ---\n{result}")

        # 删除临时文件
        os.remove(temp_path)

    # 保存完整结果
    output_file = f"{output_dir}/full_result.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(all_text))

    print(f"✅ PDF处理完成: {output_file}")
    return output_file

# 使用
ocr_pdf('document.pdf', './outputs')
```

### 示例3: Web界面调用本地模型

修改我们之前创建的 `backend/deepseek_ocr.py`，直接调用本地模型：

```python
from transformers import AutoModel, AutoTokenizer
import torch

class LocalDeepSeekOCR:
    """本地DeepSeek-OCR（无API）"""

    def __init__(self):
        self.model = None
        self.tokenizer = None

    def load_model(self):
        """加载本地模型"""
        print("正在加载DeepSeek-OCR模型...")

        model_name = 'deepseek-ai/DeepSeek-OCR'

        self.tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            trust_remote_code=True
        )

        self.model = AutoModel.from_pretrained(
            model_name,
            _attn_implementation='flash_attention_2',
            trust_remote_code=True,
            use_safetensors=True
        )

        self.model = self.model.eval().cuda().to(torch.bfloat16)
        print("✅ 模型加载成功！")

    def recognize(self, image_path, mode='ocr'):
        """识别图片"""
        if mode == 'doc2md':
            prompt = "<image>\n<|grounding|>Convert the document to markdown."
        else:
            prompt = "<image>\nExtract all text."

        result = self.model.infer(
            self.tokenizer,
            prompt=prompt,
            image_file=image_path,
            base_size=1024,
            image_size=640,
            crop_mode=True
        )

        return result

# 在Flask API中使用
ocr = LocalDeepSeekOCR()
ocr.load_model()
```

## ⚙️ 配置说明

### 分辨率设置

```python
# 不同分辨率对应的token数量
resolutions = {
    '512x512': 64,      # 最快
    '768x768': 144,     # 快速
    '1024x1024': 256,   # 推荐
    '1280x1280': 400    # 最精确
}

# 在infer中设置
result = model.infer(
    tokenizer,
    prompt=prompt,
    image_file=image_path,
    base_size=1024,  # 修改这里
    image_size=640
)
```

### GPU显存优化

```python
# 如果显存不足（<12GB）
model = model.eval().cuda().to(torch.float16)  # 使用float16

# 或者使用CPU（慢但稳定）
model = model.eval().cpu().to(torch.float32)
```

## 📊 性能对比

| 方法 | 硬件要求 | 速度 | 适用场景 |
|------|---------|------|----------|
| **vLLM + A100** | 40GB显存 | ⚡⚡⚡⚡⚡ | 生产环境，大批量 |
| **Transformers + RTX 3060** | 12GB显存 | ⚡⚡⚡ | 个人使用，中等批量 |
| **CPU模式** | 16GB内存 | ⚡ | 测试，小批量 |
| **Rust版本** | 任意 | ⚡⚡⚡⚡ | 命令行工具 |

## 🎯 优势总结

✅ **完全开源** - 无需任何API密钥
✅ **本地运行** - 数据隐私100%保护
✅ **离线可用** - 模型下载后可离线使用
✅ **免费使用** - 无任何费用
✅ **高性能** - 单GPU日处理20万页
✅ **多种方案** - Python/Rust/vLLM 任选

## 📝 常见问题

**Q: 首次运行需要下载模型吗？**
A: 是的，首次会自动从HuggingFace下载约6.67GB的模型文件。下载后会缓存到本地。

**Q: 可以完全离线使用吗？**
A: 可以！模型下载后，可以完全离线运行。

**Q: 显存不够怎么办？**
A: 可以使用CPU模式，或者降低分辨率，或者使用量化版本。

**Q: 如何加速下载？**
A: 使用HuggingFace镜像：
```bash
export HF_ENDPOINT=https://hf-mirror.com
```

## 🔗 相关资源

- **官方仓库**: https://github.com/deepseek-ai/DeepSeek-OCR
- **Rust版本**: https://github.com/TimmyOVO/deepseek-ocr.rs
- **模型下载**: https://huggingface.co/deepseek-ai/DeepSeek-OCR
- **使用教程**: https://blog.csdn.net/qq_58607032/article/details/153774639

---

**完全开源，无需API，本地运行，数据安全！** 🚀
