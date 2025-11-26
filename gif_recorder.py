# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox
from tkinter import font
import threading
import time
import datetime
from PIL import ImageGrab
import imageio
import os
import ctypes
import subprocess

# --- 1. 全局配置与多语言字典 ---
# 解决高分屏模糊问题
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    ctypes.windll.user32.SetProcessDPIAware()

# 多语言文案配置
LANG_CONFIG = {
    'zh': {
        'window_title': "简易屏幕 GIF 录制",
        'header_title': "屏幕 GIF 录制工具",
        'btn_lang': "English",
        'status_ready': "准备就绪 - 请点击开始",
        'status_recording': "🔴 正在录制... (点击停止)",
        'status_processing': "⏳ 正在合成 GIF，请稍候...",
        'status_saved': "✅ 保存成功！",
        'status_error': "❌ 保存失败",
        'btn_start': "开始录制 (选区)",
        'btn_stop': "停止录制并保存",
        'btn_folder': "📂 打开保存文件夹",
        'msg_box_title': "完成",
        'msg_box_content': "GIF 已保存至:\n{path}"
    },
    'en': {
        'window_title': "Simple Screen GIF Recorder",
        'header_title': "Screen GIF Recorder",
        'btn_lang': "中文",
        'status_ready': "Ready - Click Start to Select",
        'status_recording': "🔴 Recording... (Click to Stop)",
        'status_processing': "⏳ Processing GIF, please wait...",
        'status_saved': "✅ Saved Successfully!",
        'status_error': "❌ Save Failed",
        'btn_start': "Start Recording (Select Area)",
        'btn_stop': "Stop & Save",
        'btn_folder': "📂 Open Output Folder",
        'msg_box_title': "Done",
        'msg_box_content': "GIF saved at:\n{path}"
    }
}

class GifRecorder:
    def __init__(self):
        self.root = tk.Tk()
        self.current_lang = 'zh' # 默认语言
        self.frames = []
        self.recording = False
        self.rect = None
        
        # 初始化输出目录
        self.output_folder = os.path.join(os.getcwd(), "output_gifs")
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        self.setup_ui()
        self.update_texts() # 初始化文字
        self.root.mainloop()

    def setup_ui(self):
        """UI 布局初始化"""
        # 设置窗口大小并居中
        w, h = 500, 380
        self.center_window(w, h)
        
        # 定义字体
        self.font_title = font.Font(family="微软雅黑", size=16, weight="bold")
        self.font_btn = font.Font(family="微软雅黑", size=11)
        self.font_status = font.Font(family="微软雅黑", size=10)

        # --- 1. 顶部栏 (语言切换) ---
        top_bar = tk.Frame(self.root)
        top_bar.pack(fill='x', padx=10, pady=5)
        
        # 语言按钮放在右上角
        self.btn_lang = tk.Button(top_bar, command=self.toggle_language, bd=1, relief="groove")
        self.btn_lang.pack(side='right')

        # --- 2. 标题与状态区 ---
        header_frame = tk.Frame(self.root)
        header_frame.pack(pady=5)
        
        self.lbl_title = tk.Label(header_frame, font=self.font_title, fg="#333")
        self.lbl_title.pack()
        
        self.lbl_status = tk.Label(header_frame, font=self.font_status, fg="gray")
        self.lbl_status.pack(pady=5)

        # --- 3. 核心操作区 (大按钮) ---
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=15, padx=40, fill='x')

        self.btn_record = tk.Button(control_frame, command=self.on_record_click, 
                                    font=self.font_btn, height=2, bg="#f0f0f0", cursor="hand2")
        self.btn_record.pack(fill='x') # 填满横向区域

        # --- 4. 底部功能区 ---
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(side='bottom', pady=20, padx=40, fill='x')

        self.btn_open = tk.Button(bottom_frame, command=self.open_output_folder,
                                  font=self.font_btn, height=2, bg="#e1e1e1")
        self.btn_open.pack(fill='x') # 填满横向区域

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def toggle_language(self):
        """切换语言状态并刷新UI"""
        self.current_lang = 'en' if self.current_lang == 'zh' else 'zh'
        self.update_texts()

    def get_text(self, key):
        """获取当前语言对应的文本"""
        return LANG_CONFIG[self.current_lang][key]

    def update_texts(self):
        """刷新界面所有文字"""
        self.root.title(self.get_text('window_title'))
        self.lbl_title.config(text=self.get_text('header_title'))
        self.btn_lang.config(text=self.get_text('btn_lang'))
        self.btn_open.config(text=self.get_text('btn_folder'))
        
        # 根据当前状态更新录制按钮文字
        if not self.recording:
            self.btn_record.config(text=self.get_text('btn_start'))
            self.lbl_status.config(text=self.get_text('status_ready'), fg="gray")
        else:
            self.btn_record.config(text=self.get_text('btn_stop'))
            self.lbl_status.config(text=self.get_text('status_recording'), fg="red")

    def on_record_click(self):
        """点击录制按钮的逻辑分发"""
        if not self.recording:
            self.start_selection_mode()
        else:
            self.stop_recording()

    # --- 选区逻辑 ---
    def start_selection_mode(self):
        self.root.withdraw()
        self.sel_win = tk.Toplevel()
        self.sel_win.attributes('-alpha', 0.3)
        self.sel_win.attributes('-fullscreen', True)
        self.sel_win.configure(bg='black')
        self.sel_win.attributes('-topmost', True)
        
        self.sel_win.bind('<Button-1>', self.on_mouse_down)
        self.sel_win.bind('<B1-Motion>', self.on_mouse_drag)
        self.sel_win.bind('<ButtonRelease-1>', self.on_mouse_up)
        
        self.start_x = 0
        self.start_y = 0
        self.cur_rect_id = None
        self.canvas = tk.Canvas(self.sel_win, cursor="cross", bg="grey10")
        self.canvas.pack(fill="both", expand=True)

    def on_mouse_down(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def on_mouse_drag(self, event):
        if self.cur_rect_id:
            self.canvas.delete(self.cur_rect_id)
        self.cur_rect_id = self.canvas.create_rectangle(
            self.start_x, self.start_y, event.x, event.y, outline='red', width=3
        )

    def on_mouse_up(self, event):
        x1, x2 = sorted([self.start_x, event.x])
        y1, y2 = sorted([self.start_y, event.y])
        if (x2 - x1) < 10 or (y2 - y1) < 10: return

        self.rect = (x1, y1, x2, y2)
        self.sel_win.destroy()
        self.root.deiconify()
        self.start_recording_process()

    # --- 录制逻辑 ---
    def start_recording_process(self):
        self.recording = True
        self.frames = []
        
        # 更新UI状态
        self.btn_record.config(text=self.get_text('btn_stop'), bg="#ffdddd", fg="red")
        self.lbl_status.config(text=self.get_text('status_recording'), fg="red")
        self.btn_lang.config(state="disabled") # 录制时禁止切换语言
        self.btn_open.config(state="disabled")
        
        self.record_thread = threading.Thread(target=self.record_loop)
        self.record_thread.daemon = True
        self.record_thread.start()

    def record_loop(self):
        while self.recording:
            try:
                img = ImageGrab.grab(bbox=self.rect)
                self.frames.append(img)
                time.sleep(0.05)
            except Exception as e:
                print(e)

    def stop_recording(self):
        self.recording = False
        self.btn_record.config(text=self.get_text('status_processing'), state="disabled", bg="#eeeeee", fg="black")
        self.lbl_status.config(text=self.get_text('status_processing'), fg="blue")
        
        threading.Thread(target=self.save_gif).start()

    def save_gif(self):
        if not self.frames:
            self.root.after(0, lambda: self.reset_ui(None))
            return

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"GIF_{timestamp}.gif"
        filepath = os.path.join(self.output_folder, filename)
        
        try:
            imageio.mimsave(filepath, self.frames, duration=0.05, loop=0)
            self.root.after(0, lambda: self.reset_ui(filepath))
        except Exception:
            self.root.after(0, lambda: self.reset_ui(None))

    def reset_ui(self, filepath):
        self.btn_lang.config(state="normal")
        self.btn_open.config(state="normal")
        self.btn_record.config(state="normal", bg="#f0f0f0", fg="black")
        
        # 恢复文字显示（调用update_texts会自动根据当前语言重置按钮文字）
        self.update_texts()
        
        if filepath:
            self.lbl_status.config(text=self.get_text('status_saved'), fg="green")
            # 弹窗内容也需要多语言
            title = self.get_text('msg_box_title')
            content = self.get_text('msg_box_content').format(path=os.path.basename(filepath))
            messagebox.showinfo(title, content)
        else:
            self.lbl_status.config(text=self.get_text('status_error'), fg="red")

    def open_output_folder(self):
        try:
            os.startfile(self.output_folder)
        except Exception:
            pass

if __name__ == "__main__":
    app = GifRecorder()