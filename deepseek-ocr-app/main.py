#!/usr/bin/env python3
"""
DeepSeek OCR - 开源 OCR 桌面应用
"""
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
from PIL import Image, ImageTk
import threading
import json
from pathlib import Path
import os
import sys

import config
from ocr_engine import DeepSeekOCR


class DeepSeekOCRApp:
    """DeepSeek OCR 应用主窗口"""

    def __init__(self, root):
        """初始化应用"""
        self.root = root
        self.root.title(f"{config.APP_NAME} v{config.APP_VERSION}")
        self.root.geometry(f"{config.WINDOW_WIDTH}x{config.WINDOW_HEIGHT}")

        # 应用状态
        self.current_image_path = None
        self.ocr_engine = None
        self.api_key = self.load_api_key()

        # 设置样式
        self.setup_styles()

        # 创建界面
        self.create_widgets()

        # 初始化 OCR 引擎
        if self.api_key:
            self.ocr_engine = DeepSeekOCR(self.api_key)
            self.status_label.config(text="✓ 已连接到 DeepSeek API")
        else:
            self.status_label.config(text="⚠ 请设置 API Key")

    def setup_styles(self):
        """设置样式"""
        style = ttk.Style()
        style.theme_use('clam')

    def load_api_key(self) -> str:
        """加载 API Key"""
        # 优先从环境变量加载
        api_key = os.getenv("DEEPSEEK_API_KEY", "")
        if api_key:
            return api_key

        # 从配置文件加载
        if config.CONFIG_FILE.exists():
            try:
                with open(config.CONFIG_FILE, 'r') as f:
                    data = json.load(f)
                    return data.get('api_key', '')
            except:
                pass

        return ""

    def save_api_key(self, api_key: str):
        """保存 API Key"""
        try:
            with open(config.CONFIG_FILE, 'w') as f:
                json.dump({'api_key': api_key}, f)
        except Exception as e:
            messagebox.showerror("错误", f"保存配置失败: {str(e)}")

    def create_widgets(self):
        """创建界面组件"""
        # 顶部工具栏
        toolbar = tk.Frame(self.root, bg='#f0f0f0', height=50)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        # API Key 设置按钮
        ttk.Button(
            toolbar,
            text="⚙ 设置 API Key",
            command=self.show_api_key_dialog
        ).pack(side=tk.LEFT, padx=5)

        # 选择图片按钮
        ttk.Button(
            toolbar,
            text="📁 选择图片",
            command=self.select_image
        ).pack(side=tk.LEFT, padx=5)

        # 开始识别按钮
        self.recognize_btn = ttk.Button(
            toolbar,
            text="🔍 开始识别",
            command=self.start_recognition,
            state=tk.DISABLED
        )
        self.recognize_btn.pack(side=tk.LEFT, padx=5)

        # 复制文本按钮
        self.copy_btn = ttk.Button(
            toolbar,
            text="📋 复制文本",
            command=self.copy_text,
            state=tk.DISABLED
        )
        self.copy_btn.pack(side=tk.LEFT, padx=5)

        # 保存文本按钮
        self.save_btn = ttk.Button(
            toolbar,
            text="💾 保存文本",
            command=self.save_text,
            state=tk.DISABLED
        )
        self.save_btn.pack(side=tk.LEFT, padx=5)

        # 状态标签
        self.status_label = tk.Label(
            toolbar,
            text="准备就绪",
            bg='#f0f0f0',
            font=(config.FONT_FAMILY, 9)
        )
        self.status_label.pack(side=tk.RIGHT, padx=10)

        # 主内容区域 - 使用 PanedWindow 分割
        paned_window = ttk.PanedWindow(self.root, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # 左侧 - 图片预览区
        left_frame = ttk.LabelFrame(paned_window, text="图片预览", padding=10)
        paned_window.add(left_frame, weight=1)

        # 图片显示画布
        self.image_canvas = tk.Canvas(left_frame, bg='white', relief=tk.SUNKEN, borderwidth=2)
        self.image_canvas.pack(fill=tk.BOTH, expand=True)

        # 在画布中显示提示文字
        self.image_canvas.create_text(
            250, 300,
            text="点击「选择图片」开始",
            font=(config.FONT_FAMILY, 14),
            fill='gray',
            tags="placeholder"
        )

        # 右侧 - 识别结果区
        right_frame = ttk.LabelFrame(paned_window, text="识别结果", padding=10)
        paned_window.add(right_frame, weight=1)

        # 提示词输入框
        prompt_frame = tk.Frame(right_frame)
        prompt_frame.pack(fill=tk.X, pady=(0, 10))

        tk.Label(
            prompt_frame,
            text="提示词:",
            font=(config.FONT_FAMILY, config.FONT_SIZE)
        ).pack(side=tk.LEFT)

        self.prompt_entry = tk.Entry(
            prompt_frame,
            font=(config.FONT_FAMILY, config.FONT_SIZE)
        )
        self.prompt_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        self.prompt_entry.insert(0, "请识别图片中的所有文字内容，保持原有格式和布局。")

        # 结果文本框
        self.result_text = scrolledtext.ScrolledText(
            right_frame,
            wrap=tk.WORD,
            font=(config.FONT_FAMILY, config.FONT_SIZE),
            relief=tk.SUNKEN,
            borderwidth=2
        )
        self.result_text.pack(fill=tk.BOTH, expand=True)

        # 底部信息栏
        info_frame = tk.Frame(right_frame)
        info_frame.pack(fill=tk.X, pady=(10, 0))

        self.info_label = tk.Label(
            info_frame,
            text="",
            font=(config.FONT_FAMILY, 9),
            fg='gray'
        )
        self.info_label.pack(side=tk.LEFT)

    def show_api_key_dialog(self):
        """显示 API Key 设置对话框"""
        dialog = tk.Toplevel(self.root)
        dialog.title("设置 DeepSeek API Key")
        dialog.geometry("500x200")
        dialog.resizable(False, False)

        # 使对话框模态
        dialog.transient(self.root)
        dialog.grab_set()

        # 说明文字
        tk.Label(
            dialog,
            text="请输入您的 DeepSeek API Key:",
            font=(config.FONT_FAMILY, 10)
        ).pack(pady=20, padx=20)

        # API Key 输入框
        api_key_var = tk.StringVar(value=self.api_key)
        entry = tk.Entry(
            dialog,
            textvariable=api_key_var,
            font=(config.FONT_FAMILY, 10),
            width=50,
            show="*"
        )
        entry.pack(pady=10, padx=20)

        # 提示文字
        tk.Label(
            dialog,
            text="获取 API Key: https://platform.deepseek.com/api_keys",
            font=(config.FONT_FAMILY, 9),
            fg='blue',
            cursor='hand2'
        ).pack(pady=5)

        # 按钮框架
        btn_frame = tk.Frame(dialog)
        btn_frame.pack(pady=20)

        def save_and_close():
            new_api_key = api_key_var.get().strip()
            if new_api_key:
                self.api_key = new_api_key
                self.save_api_key(new_api_key)
                self.ocr_engine = DeepSeekOCR(new_api_key)
                self.status_label.config(text="✓ 已连接到 DeepSeek API")
                messagebox.showinfo("成功", "API Key 设置成功！")
                dialog.destroy()
            else:
                messagebox.showwarning("警告", "请输入有效的 API Key")

        ttk.Button(btn_frame, text="保存", command=save_and_close).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="取消", command=dialog.destroy).pack(side=tk.LEFT, padx=5)

        # 聚焦到输入框
        entry.focus_set()
        entry.select_range(0, tk.END)

    def select_image(self):
        """选择图片"""
        file_path = filedialog.askopenfilename(
            title="选择图片",
            filetypes=config.SUPPORTED_IMAGE_FORMATS
        )

        if file_path:
            self.current_image_path = file_path
            self.display_image(file_path)
            self.recognize_btn.config(state=tk.NORMAL)
            self.status_label.config(text=f"已加载: {Path(file_path).name}")

    def display_image(self, image_path: str):
        """显示图片"""
        try:
            # 加载图片
            image = Image.open(image_path)

            # 获取画布尺寸
            self.image_canvas.update()
            canvas_width = self.image_canvas.winfo_width()
            canvas_height = self.image_canvas.winfo_height()

            # 计算缩放比例
            img_width, img_height = image.size
            scale = min(canvas_width / img_width, canvas_height / img_height, 1.0)

            # 缩放图片
            new_width = int(img_width * scale * 0.95)
            new_height = int(img_height * scale * 0.95)
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

            # 转换为 PhotoImage
            self.photo = ImageTk.PhotoImage(image)

            # 清空画布
            self.image_canvas.delete("all")

            # 居中显示图片
            x = (canvas_width - new_width) // 2
            y = (canvas_height - new_height) // 2
            self.image_canvas.create_image(x, y, image=self.photo, anchor=tk.NW)

        except Exception as e:
            messagebox.showerror("错误", f"无法加载图片: {str(e)}")

    def start_recognition(self):
        """开始识别"""
        if not self.ocr_engine:
            messagebox.showwarning("警告", "请先设置 API Key")
            self.show_api_key_dialog()
            return

        if not self.current_image_path:
            messagebox.showwarning("警告", "请先选择图片")
            return

        # 禁用按钮
        self.recognize_btn.config(state=tk.DISABLED)
        self.status_label.config(text="正在识别...")
        self.result_text.delete(1.0, tk.END)
        self.info_label.config(text="")

        # 获取提示词
        prompt = self.prompt_entry.get().strip()
        if not prompt:
            prompt = "请识别图片中的所有文字内容，保持原有格式和布局。"

        # 在新线程中执行识别
        thread = threading.Thread(
            target=self._do_recognition,
            args=(self.current_image_path, prompt)
        )
        thread.daemon = True
        thread.start()

    def _do_recognition(self, image_path: str, prompt: str):
        """执行识别（在后台线程中）"""
        result = self.ocr_engine.ocr_from_path(image_path, prompt)

        # 在主线程中更新 UI
        self.root.after(0, lambda: self._update_result(result))

    def _update_result(self, result: dict):
        """更新识别结果"""
        self.recognize_btn.config(state=tk.NORMAL)

        if result['success']:
            # 显示识别结果
            text = result['text']
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(1.0, text)

            # 启用按钮
            self.copy_btn.config(state=tk.NORMAL)
            self.save_btn.config(state=tk.NORMAL)

            # 显示 token 使用情况
            tokens_used = result.get('tokens_used', {})
            info_text = f"模型: {result.get('model', 'N/A')} | " \
                       f"Token 使用: {tokens_used.get('total_tokens', 'N/A')}"
            self.info_label.config(text=info_text)

            self.status_label.config(text="✓ 识别完成")
        else:
            # 显示错误
            error_msg = result.get('error', '未知错误')
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(1.0, f"识别失败:\n{error_msg}")
            self.status_label.config(text="✗ 识别失败")
            messagebox.showerror("识别失败", error_msg)

    def copy_text(self):
        """复制文本到剪贴板"""
        text = self.result_text.get(1.0, tk.END).strip()
        if text:
            self.root.clipboard_clear()
            self.root.clipboard_append(text)
            self.status_label.config(text="✓ 已复制到剪贴板")
            messagebox.showinfo("成功", "文本已复制到剪贴板")

    def save_text(self):
        """保存文本到文件"""
        text = self.result_text.get(1.0, tk.END).strip()
        if not text:
            messagebox.showwarning("警告", "没有可保存的内容")
            return

        file_path = filedialog.asksaveasfilename(
            title="保存文本",
            defaultextension=".txt",
            filetypes=[("文本文件", "*.txt"), ("所有文件", "*.*")]
        )

        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                self.status_label.config(text=f"✓ 已保存: {Path(file_path).name}")
                messagebox.showinfo("成功", f"文本已保存到:\n{file_path}")
            except Exception as e:
                messagebox.showerror("错误", f"保存失败: {str(e)}")


def main():
    """主函数"""
    root = tk.Tk()
    app = DeepSeekOCRApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
