#!/usr/bin/env python3
"""
小莫 OCR - macOS 图形界面版本
简单易用的文字识别工具
"""

import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext, messagebox
from tkinter.dnd import DND_FILES
import threading
import os
import sys
from pathlib import Path
from typing import Optional, List
import platform

# 检测是否为 macOS
IS_MACOS = platform.system() == 'Darwin'
IS_APPLE_SILICON = platform.machine() == 'arm64'


class XiaomoOCRApp:
    """小莫 OCR 主应用"""

    def __init__(self, root):
        self.root = root
        self.root.title("小莫 OCR - 文字识别工具")
        self.root.geometry("900x700")

        # 设置窗口图标和样式
        self.setup_style()

        # 模型相关
        self.model = None
        self.tokenizer = None
        self.model_loaded = False
        self.loading = False

        # 文件列表
        self.file_paths = []

        # 创建界面
        self.create_widgets()

        # 显示欢迎信息
        self.show_welcome()

    def setup_style(self):
        """设置界面样式"""
        # 设置 macOS 原生风格
        if IS_MACOS:
            try:
                self.root.tk.call('source', '/System/Library/Tcl/8.5/tk.tcl')
            except:
                pass

        # 配置颜色方案
        self.colors = {
            'primary': '#667eea',
            'secondary': '#764ba2',
            'success': '#48bb78',
            'warning': '#ed8936',
            'danger': '#f56565',
            'bg': '#f7fafc',
            'text': '#2d3748'
        }

        # 设置全局字体
        if IS_MACOS:
            default_font = ('SF Pro', 13)
            title_font = ('SF Pro', 18, 'bold')
        else:
            default_font = ('Arial', 11)
            title_font = ('Arial', 16, 'bold')

        self.fonts = {
            'default': default_font,
            'title': title_font
        }

    def create_widgets(self):
        """创建界面组件"""

        # 主容器
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)

        # 标题区域
        title_frame = ttk.Frame(main_frame)
        title_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))

        title_label = ttk.Label(
            title_frame,
            text="🤖 小莫 OCR",
            font=self.fonts['title']
        )
        title_label.grid(row=0, column=0, sticky=tk.W)

        subtitle_label = ttk.Label(
            title_frame,
            text="基于 DeepSeek-OCR 的智能文字识别",
            font=self.fonts['default']
        )
        subtitle_label.grid(row=1, column=0, sticky=tk.W)

        # 状态指示器
        self.status_label = ttk.Label(
            title_frame,
            text="⚪ 模型未加载",
            font=self.fonts['default']
        )
        self.status_label.grid(row=0, column=1, rowspan=2, sticky=tk.E)
        title_frame.columnconfigure(1, weight=1)

        # 分隔线
        ttk.Separator(main_frame, orient='horizontal').grid(
            row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 20)
        )

        # 控制面板
        control_frame = ttk.LabelFrame(main_frame, text="控制面板", padding="15")
        control_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        control_frame.columnconfigure(1, weight=1)

        # 模式选择
        ttk.Label(control_frame, text="识别模式:").grid(row=0, column=0, sticky=tk.W, pady=5)

        self.mode_var = tk.StringVar(value="ocr")
        mode_frame = ttk.Frame(control_frame)
        mode_frame.grid(row=0, column=1, sticky=tk.W, padx=10)

        modes = [
            ("通用 OCR", "ocr"),
            ("文档转 Markdown", "doc2md"),
            ("图表解析", "figure")
        ]

        for i, (text, value) in enumerate(modes):
            ttk.Radiobutton(
                mode_frame,
                text=text,
                value=value,
                variable=self.mode_var
            ).grid(row=0, column=i, padx=5)

        # 分辨率选择
        ttk.Label(control_frame, text="分辨率:").grid(row=1, column=0, sticky=tk.W, pady=5)

        self.resolution_var = tk.StringVar(value="1024")
        resolution_combo = ttk.Combobox(
            control_frame,
            textvariable=self.resolution_var,
            values=["512 (快速)", "768 (均衡)", "1024 (推荐)", "1280 (精确)"],
            state='readonly',
            width=20
        )
        resolution_combo.grid(row=1, column=1, sticky=tk.W, padx=10, pady=5)
        resolution_combo.current(2)

        # 文件选择区域
        file_frame = ttk.LabelFrame(main_frame, text="文件选择", padding="15")
        file_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        file_frame.columnconfigure(0, weight=1)

        # 文件列表
        list_frame = ttk.Frame(file_frame)
        list_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        list_frame.columnconfigure(0, weight=1)

        self.file_listbox = tk.Listbox(
            list_frame,
            height=5,
            font=self.fonts['default']
        )
        self.file_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.file_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.file_listbox.configure(yscrollcommand=scrollbar.set)

        # 文件操作按钮
        button_frame = ttk.Frame(file_frame)
        button_frame.grid(row=1, column=0, pady=(10, 0))

        ttk.Button(
            button_frame,
            text="📁 添加图片",
            command=self.add_images
        ).grid(row=0, column=0, padx=5)

        ttk.Button(
            button_frame,
            text="📄 添加 PDF",
            command=self.add_pdf
        ).grid(row=0, column=1, padx=5)

        ttk.Button(
            button_frame,
            text="🗑️ 清空列表",
            command=self.clear_files
        ).grid(row=0, column=2, padx=5)

        # 主按钮区域
        action_frame = ttk.Frame(main_frame)
        action_frame.grid(row=4, column=0, pady=(0, 15))

        self.load_button = ttk.Button(
            action_frame,
            text="⚡ 加载模型",
            command=self.load_model_async,
            width=15
        )
        self.load_button.grid(row=0, column=0, padx=5)

        self.recognize_button = ttk.Button(
            action_frame,
            text="🚀 开始识别",
            command=self.start_recognition,
            width=15,
            state='disabled'
        )
        self.recognize_button.grid(row=0, column=1, padx=5)

        ttk.Button(
            action_frame,
            text="💾 保存结果",
            command=self.save_result,
            width=15
        ).grid(row=0, column=2, padx=5)

        # 进度条
        self.progress_var = tk.DoubleVar()
        self.progress = ttk.Progressbar(
            main_frame,
            mode='indeterminate',
            variable=self.progress_var
        )
        self.progress.grid(row=5, column=0, sticky=(tk.W, tk.E), pady=(0, 15))

        # 结果显示区域
        result_frame = ttk.LabelFrame(main_frame, text="识别结果", padding="10")
        result_frame.grid(row=6, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(6, weight=1)

        self.result_text = scrolledtext.ScrolledText(
            result_frame,
            wrap=tk.WORD,
            font=('Courier', 12),
            height=15
        )
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # 底部信息栏
        info_frame = ttk.Frame(main_frame)
        info_frame.grid(row=7, column=0, sticky=(tk.W, tk.E))
        info_frame.columnconfigure(1, weight=1)

        self.info_label = ttk.Label(
            info_frame,
            text="就绪",
            font=self.fonts['default']
        )
        self.info_label.grid(row=0, column=0, sticky=tk.W)

        # 设备信息
        device_info = f"🖥️ {platform.machine()}"
        if IS_APPLE_SILICON:
            device_info += " (支持 GPU 加速)"

        ttk.Label(
            info_frame,
            text=device_info,
            font=self.fonts['default']
        ).grid(row=0, column=1, sticky=tk.E)

    def show_welcome(self):
        """显示欢迎信息"""
        welcome_text = """
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║         欢迎使用小莫 OCR 文字识别工具                    ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝

🚀 快速开始:

1️⃣  点击 "⚡ 加载模型" 按钮（首次需要下载约 6.67GB）
2️⃣  添加要识别的图片或 PDF 文件
3️⃣  选择识别模式和分辨率
4️⃣  点击 "🚀 开始识别" 按钮

💡 功能特性:
   • 支持图片格式: JPG, PNG, PDF 等
   • 三种识别模式: 通用 OCR / 文档转 MD / 图表解析
   • 完全本地运行，数据隐私 100% 保护
   • 无需网络连接（模型下载后）
"""
        if IS_APPLE_SILICON:
            welcome_text += "   • Apple Silicon GPU 自动加速 🚄\n"

        welcome_text += "\n📝 小提示: 首次运行会自动下载模型，请保持网络连接"

        self.result_text.insert('1.0', welcome_text)
        self.result_text.configure(state='disabled')

    def add_images(self):
        """添加图片文件"""
        files = filedialog.askopenfilenames(
            title="选择图片文件",
            filetypes=[
                ("图片文件", "*.jpg *.jpeg *.png *.bmp *.tiff *.gif"),
                ("所有文件", "*.*")
            ]
        )

        for file in files:
            if file not in self.file_paths:
                self.file_paths.append(file)
                self.file_listbox.insert(tk.END, os.path.basename(file))

        self.update_info(f"已添加 {len(files)} 个文件")

    def add_pdf(self):
        """添加 PDF 文件"""
        files = filedialog.askopenfilenames(
            title="选择 PDF 文件",
            filetypes=[
                ("PDF 文件", "*.pdf"),
                ("所有文件", "*.*")
            ]
        )

        for file in files:
            if file not in self.file_paths:
                self.file_paths.append(file)
                self.file_listbox.insert(tk.END, os.path.basename(file))

        self.update_info(f"已添加 {len(files)} 个 PDF 文件")

    def clear_files(self):
        """清空文件列表"""
        self.file_paths.clear()
        self.file_listbox.delete(0, tk.END)
        self.update_info("已清空文件列表")

    def update_info(self, message):
        """更新信息栏"""
        self.info_label.config(text=message)
        self.root.update()

    def update_status(self, status, color='black'):
        """更新状态指示器"""
        icons = {
            'loading': '🟡',
            'loaded': '🟢',
            'error': '🔴',
            'idle': '⚪'
        }

        status_text = {
            'loading': '正在加载...',
            'loaded': '模型已就绪',
            'error': '加载失败',
            'idle': '模型未加载'
        }

        self.status_label.config(
            text=f"{icons.get(status, '⚪')} {status_text.get(status, '未知状态')}"
        )

    def load_model_async(self):
        """异步加载模型"""
        if self.model_loaded:
            messagebox.showinfo("提示", "模型已经加载！")
            return

        if self.loading:
            messagebox.showwarning("警告", "模型正在加载中，请稍候...")
            return

        # 在新线程中加载模型
        thread = threading.Thread(target=self.load_model)
        thread.daemon = True
        thread.start()

    def load_model(self):
        """加载 OCR 模型"""
        self.loading = True
        self.load_button.config(state='disabled')
        self.update_status('loading')
        self.progress.start(10)

        try:
            self.update_info("正在加载模型... 首次运行需要下载约 6.67GB")

            # 导入必要的库
            import torch
            from transformers import AutoModel, AutoTokenizer

            # 确定设备
            if IS_APPLE_SILICON and torch.backends.mps.is_available():
                device = 'mps'  # Apple Silicon GPU
                self.update_info("使用 Apple Silicon GPU 加速")
            elif torch.cuda.is_available():
                device = 'cuda'
                self.update_info("使用 NVIDIA GPU 加速")
            else:
                device = 'cpu'
                self.update_info("使用 CPU 模式")

            # 加载模型
            model_name = 'deepseek-ai/DeepSeek-OCR'

            self.update_info("正在加载 Tokenizer...")
            self.tokenizer = AutoTokenizer.from_pretrained(
                model_name,
                trust_remote_code=True
            )

            self.update_info("正在加载模型... 请稍候")
            self.model = AutoModel.from_pretrained(
                model_name,
                trust_remote_code=True,
                use_safetensors=True
            )

            # 移动到设备
            if device == 'mps':
                self.model = self.model.to('mps')
            elif device == 'cuda':
                self.model = self.model.cuda().to(torch.bfloat16)
            else:
                self.model = self.model.cpu().to(torch.float32)

            self.model = self.model.eval()

            self.model_loaded = True
            self.update_status('loaded')
            self.recognize_button.config(state='normal')
            self.update_info(f"✅ 模型加载成功！使用设备: {device.upper()}")

            messagebox.showinfo("成功", f"模型加载成功！\n运行设备: {device.upper()}")

        except Exception as e:
            self.update_status('error')
            error_msg = f"模型加载失败: {str(e)}"
            self.update_info(error_msg)
            messagebox.showerror("错误", error_msg)

        finally:
            self.loading = False
            self.load_button.config(state='normal')
            self.progress.stop()

    def start_recognition(self):
        """开始识别"""
        if not self.model_loaded:
            messagebox.showwarning("警告", "请先加载模型！")
            return

        if not self.file_paths:
            messagebox.showwarning("警告", "请先添加要识别的文件！")
            return

        # 在新线程中执行识别
        thread = threading.Thread(target=self.recognize_files)
        thread.daemon = True
        thread.start()

    def recognize_files(self):
        """识别文件"""
        self.recognize_button.config(state='disabled')
        self.progress.start(10)

        # 清空结果
        self.result_text.configure(state='normal')
        self.result_text.delete('1.0', tk.END)

        mode = self.mode_var.get()
        resolution = int(self.resolution_var.get().split()[0])

        all_results = []

        try:
            for i, file_path in enumerate(self.file_paths):
                self.update_info(f"处理 {i+1}/{len(self.file_paths)}: {os.path.basename(file_path)}")

                # 构建提示词
                if mode == 'doc2md':
                    prompt = "<image>\n<|grounding|>Convert the document to markdown."
                elif mode == 'figure':
                    prompt = "<image>\n<|grounding|>Parse this figure/chart."
                else:
                    prompt = "<image>\nExtract all text from this image."

                # 执行识别
                result = self.model.infer(
                    self.tokenizer,
                    prompt=prompt,
                    image_file=file_path,
                    base_size=resolution,
                    image_size=640,
                    crop_mode=True
                )

                # 显示结果
                result_text = f"\n{'='*60}\n"
                result_text += f"文件: {os.path.basename(file_path)}\n"
                result_text += f"{'='*60}\n\n"
                result_text += result + "\n\n"

                all_results.append(result_text)

                self.result_text.insert(tk.END, result_text)
                self.result_text.see(tk.END)

            self.update_info(f"✅ 识别完成！共处理 {len(self.file_paths)} 个文件")
            messagebox.showinfo("完成", f"成功识别 {len(self.file_paths)} 个文件！")

        except Exception as e:
            error_msg = f"识别失败: {str(e)}"
            self.update_info(error_msg)
            messagebox.showerror("错误", error_msg)

        finally:
            self.recognize_button.config(state='normal')
            self.progress.stop()
            self.result_text.configure(state='disabled')

    def save_result(self):
        """保存识别结果"""
        content = self.result_text.get('1.0', tk.END)

        if not content.strip():
            messagebox.showwarning("警告", "没有可保存的内容！")
            return

        file_path = filedialog.asksaveasfilename(
            title="保存识别结果",
            defaultextension=".txt",
            filetypes=[
                ("文本文件", "*.txt"),
                ("Markdown 文件", "*.md"),
                ("所有文件", "*.*")
            ]
        )

        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.update_info(f"✅ 结果已保存到: {os.path.basename(file_path)}")
                messagebox.showinfo("成功", "结果保存成功！")
            except Exception as e:
                messagebox.showerror("错误", f"保存失败: {str(e)}")


def main():
    """主函数"""
    root = tk.Tk()

    # macOS 特定设置
    if IS_MACOS:
        # 设置应用名称
        root.createcommand('tk::mac::ShowPreferences', lambda: None)

    app = XiaomoOCRApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
