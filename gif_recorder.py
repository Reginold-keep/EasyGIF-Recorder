# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox, font, ttk
import threading
import time
import datetime
from PIL import ImageGrab
import imageio
import os
import ctypes

# --- DPI 感知 ---
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    ctypes.windll.user32.SetProcessDPIAware()

# --- 多语言配置 ---
LANG_CONFIG = {
    'zh': {
        'window_title': "GIF 录制工具 V5.0",
        'header_title': "屏幕 GIF 录制",
        'btn_lang': "English",
        'lbl_mode': "录制模式:",
        'modes': ["自由选区 (Free)", "16:9 (宽屏)", "4:3 (标准)", "1:1 (正方)", "自定义比例 (Custom)"],
        'lbl_custom': "输入比例 (如 21:9):",
        'btn_start': "开始选取",
        'btn_stop': "停止录制",
        'btn_folder': "📂 打开文件夹",
        'status_ready': "准备就绪",
        'status_recording': "🔴 录制中...",
        'status_processing': "⏳ 处理中...",
        'status_saved': "✅ 保存成功",
        'guide_free': "按住鼠标左键拖拽选区",
        'guide_fixed': "移动定位，滚轮缩放，左键确认",
        'msg_saved': "GIF 已保存至:\n{path}",
        'err_ratio': "比例格式错误！\n请使用 '宽:高' 格式，例如: 21:9"
    },
    'en': {
        'window_title': "GIF Recorder V5.0",
        'header_title': "Screen GIF Recorder",
        'btn_lang': "中文",
        'lbl_mode': "Mode:",
        'modes': ["Free Select", "16:9 (Wide)", "4:3 (Standard)", "1:1 (Square)", "Custom Ratio"],
        'lbl_custom': "Ratio (e.g. 21:9):",
        'btn_start': "Start Selection",
        'btn_stop': "Stop Recording",
        'btn_folder': "📂 Open Folder",
        'status_ready': "Ready",
        'status_recording': "🔴 Recording...",
        'status_processing': "⏳ Processing...",
        'status_saved': "✅ Saved",
        'guide_free': "Drag mouse to select area",
        'guide_fixed': "Move to position, Scroll to resize, Click to confirm",
        'msg_saved': "GIF saved at:\n{path}",
        'err_ratio': "Invalid Ratio Format!\nPlease use 'W:H', e.g., 21:9"
    }
}

class GifRecorder:
    def __init__(self):
        self.root = tk.Tk()
        self.current_lang = 'zh'
        self.recording = False
        self.frames = []
        self.rect = None
        self.mode_var = tk.StringVar()
        self.ratio_var = tk.StringVar(value="21:9") # 默认自定义比例
        
        self.fixed_width = 400 

        self.output_folder = os.path.join(os.getcwd(), "output_gifs")
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        self.setup_ui()
        self.update_texts()
        self.on_mode_change(None) # 初始化输入框状态
        self.root.mainloop()

    def setup_ui(self):
        w, h = 500, 480 #稍微加高一点以容纳新控件
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f'{w}x{h}+{(screen_width-w)//2}+{(screen_height-h)//2}')
        
        self.font_title = font.Font(family="微软雅黑", size=16, weight="bold")
        self.font_ui = font.Font(family="微软雅黑", size=10)

        # 1. 顶部栏
        top_bar = tk.Frame(self.root)
        top_bar.pack(fill='x', padx=15, pady=10)
        self.btn_lang = tk.Button(top_bar, command=self.toggle_language, bd=1)
        self.btn_lang.pack(side='right')

        # 2. 标题
        self.lbl_title = tk.Label(self.root, font=self.font_title, fg="#333")
        self.lbl_title.pack(pady=5)
        self.lbl_status = tk.Label(self.root, font=self.font_ui, fg="gray")
        self.lbl_status.pack()

        # 3. 模式选择区 (使用 Grid 布局更整齐)
        mode_frame = tk.Frame(self.root)
        mode_frame.pack(pady=15)

        # 第一行：下拉菜单
        self.lbl_mode_title = tk.Label(mode_frame, font=self.font_ui)
        self.lbl_mode_title.grid(row=0, column=0, padx=5, sticky='e')
        
        self.combo_mode = ttk.Combobox(mode_frame, textvariable=self.mode_var, state="readonly", width=18)
        self.combo_mode.bind("<<ComboboxSelected>>", self.on_mode_change)
        self.combo_mode.grid(row=0, column=1, padx=5, sticky='w')

        # 第二行：自定义输入框 (默认隐藏或禁用，视情况而定)
        self.lbl_custom_title = tk.Label(mode_frame, font=self.font_ui, fg="gray")
        self.lbl_custom_title.grid(row=1, column=0, padx=5, pady=10, sticky='e')

        self.entry_ratio = tk.Entry(mode_frame, textvariable=self.ratio_var, width=15, font=("Arial", 10))
        self.entry_ratio.grid(row=1, column=1, padx=5, pady=10, sticky='w')

        # 4. 操作按钮
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(fill='x', padx=50, pady=5)
        
        self.btn_record = tk.Button(btn_frame, command=self.on_record_click, 
                                    font=("微软雅黑", 12), height=2, bg="#f0f0f0")
        self.btn_record.pack(fill='x')

        self.btn_open = tk.Button(self.root, command=self.open_output_folder, bg="#e1e1e1")
        self.btn_open.pack(fill='x', padx=50, pady=15, side='bottom')

    def toggle_language(self):
        self.current_lang = 'en' if self.current_lang == 'zh' else 'zh'
        self.update_texts()

    def get_text(self, key):
        return LANG_CONFIG[self.current_lang][key]

    def update_texts(self):
        self.root.title(self.get_text('window_title'))
        self.lbl_title.config(text=self.get_text('header_title'))
        self.btn_lang.config(text=self.get_text('btn_lang'))
        self.lbl_mode_title.config(text=self.get_text('lbl_mode'))
        self.lbl_custom_title.config(text=self.get_text('lbl_custom'))
        self.btn_open.config(text=self.get_text('btn_folder'))
        
        # 刷新下拉列表，保持当前选中项不变
        current_idx = self.combo_mode.current()
        self.combo_mode['values'] = self.get_text('modes')
        if current_idx == -1: current_idx = 0
        self.combo_mode.current(current_idx)
        
        if not self.recording:
            self.btn_record.config(text=self.get_text('btn_start'))
            self.lbl_status.config(text=self.get_text('status_ready'))
        else:
            self.btn_record.config(text=self.get_text('btn_stop'))
            self.lbl_status.config(text=self.get_text('status_recording'))

    def on_mode_change(self, event):
        # 只有选了最后一项(自定义)，才启用输入框
        idx = self.combo_mode.current()
        if idx == 4: # 自定义
            self.entry_ratio.config(state='normal', bg='white')
            self.lbl_custom_title.config(fg='#333')
        else:
            self.entry_ratio.config(state='disabled', bg='#f0f0f0')
            self.lbl_custom_title.config(fg='#ccc')
        self.root.focus()

    def on_record_click(self):
        if not self.recording:
            self.start_selection_mode()
        else:
            self.stop_recording()

    # --- 核心选区逻辑 ---
    def start_selection_mode(self):
        mode_idx = self.combo_mode.current()
        
        # 1. 预计算比例
        self.target_ratio = 1.0
        if mode_idx == 1: self.target_ratio = 16/9
        elif mode_idx == 2: self.target_ratio = 4/3
        elif mode_idx == 3: self.target_ratio = 1.0
        elif mode_idx == 4: # 自定义
            try:
                # 解析用户输入，支持中英文冒号
                txt = self.ratio_var.get().replace('：', ':')
                w, h = map(float, txt.split(':'))
                if h == 0: raise ValueError
                self.target_ratio = w / h
            except:
                messagebox.showerror("Error", self.get_text('err_ratio'))
                return

        # 2. 开启遮罩窗口
        self.root.withdraw()
        self.sel_win = tk.Toplevel()
        self.sel_win.attributes('-alpha', 0.4)
        self.sel_win.attributes('-fullscreen', True)
        self.sel_win.configure(bg='black')
        self.sel_win.attributes('-topmost', True)
        
        self.canvas = tk.Canvas(self.sel_win, cursor="cross", bg="grey10")
        self.canvas.pack(fill="both", expand=True)

        guide_text = self.get_text('guide_free') if mode_idx == 0 else self.get_text('guide_fixed')
        self.txt_guide = self.canvas.create_text(
            self.root.winfo_screenwidth()//2, 50, 
            text=guide_text, fill="white", font=("微软雅黑", 14, "bold")
        )

        if mode_idx == 0:
            # 自由模式
            self.sel_win.bind('<Button-1>', self.on_free_down)
            self.sel_win.bind('<B1-Motion>', self.on_free_drag)
            self.sel_win.bind('<ButtonRelease-1>', self.on_free_up)
            self.cur_rect_id = None
            self.cur_text_id = None
        else:
            # 固定比例模式
            self.sel_win.bind('<Motion>', self.on_fixed_move)
            self.sel_win.bind('<Button-1>', self.on_fixed_click)
            self.sel_win.bind('<MouseWheel>', self.on_fixed_wheel)
            cx, cy = self.root.winfo_screenwidth()//2, self.root.winfo_screenheight()//2
            self.update_fixed_rect(cx, cy)

    # --- 自由模式事件 ---
    def on_free_down(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def on_free_drag(self, event):
        if self.cur_rect_id: self.canvas.delete(self.cur_rect_id)
        if self.cur_text_id: self.canvas.delete(self.cur_text_id)
        
        self.cur_rect_id = self.canvas.create_rectangle(
            self.start_x, self.start_y, event.x, event.y, outline='red', width=3
        )
        w = abs(event.x - self.start_x)
        h = abs(event.y - self.start_y)
        self.cur_text_id = self.canvas.create_text(
            event.x + 10, event.y - 10, text=f"{w} x {h}", fill="#00FF00", font=("Arial", 12, "bold"), anchor="w"
        )

    def on_free_up(self, event):
        x1, x2 = sorted([self.start_x, event.x])
        y1, y2 = sorted([self.start_y, event.y])
        if (x2 - x1) < 10 or (y2 - y1) < 10: return
        self.rect = (x1, y1, x2, y2)
        self.finish_selection()

    # --- 固定比例事件 ---
    def on_fixed_move(self, event):
        self.update_fixed_rect(event.x, event.y)

    def on_fixed_wheel(self, event):
        scale = 1.1 if event.delta > 0 else 0.9
        self.fixed_width = max(50, min(self.root.winfo_screenwidth(), self.fixed_width * scale))
        self.update_fixed_rect(event.x, event.y)

    def update_fixed_rect(self, cx, cy):
        self.canvas.delete("fixed_rect")
        self.canvas.delete("fixed_text")
        
        w = self.fixed_width
        h = w / self.target_ratio
        
        x1 = cx - w/2
        y1 = cy - h/2
        x2 = cx + w/2
        y2 = cy + h/2
        
        self.canvas.create_rectangle(x1, y1, x2, y2, outline='red', width=3, tags="fixed_rect")
        self.canvas.create_text(cx, y1 - 15, text=f"{int(w)} x {int(h)}", fill="#00FF00", font=("Arial", 12, "bold"), tags="fixed_text")
        self.temp_rect = (int(x1), int(y1), int(x2), int(y2))

    def on_fixed_click(self, event):
        self.rect = self.temp_rect
        self.finish_selection()

    # --- 通用结束逻辑 ---
    def finish_selection(self):
        self.sel_win.destroy()
        self.root.deiconify()
        self.start_recording_process()

    def start_recording_process(self):
        self.recording = True
        self.frames = []
        self.btn_record.config(text=self.get_text('btn_stop'), bg="#ffdddd", fg="red")
        self.lbl_status.config(text=self.get_text('status_recording'), fg="red")
        self.combo_mode.config(state="disabled")
        self.entry_ratio.config(state="disabled")
        
        threading.Thread(target=self.record_loop, daemon=True).start()

    def record_loop(self):
        while self.recording:
            try:
                img = ImageGrab.grab(bbox=self.rect)
                self.frames.append(img)
                time.sleep(0.05)
            except: pass

    def stop_recording(self):
        self.recording = False
        self.btn_record.config(state="disabled", text=self.get_text('status_processing'))
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
        except:
            self.root.after(0, lambda: self.reset_ui(None))

    def reset_ui(self, filepath):
        self.btn_record.config(state="normal", bg="#f0f0f0", fg="black")
        self.combo_mode.config(state="readonly")
        self.update_texts()
        # 恢复自定义输入框状态
        self.on_mode_change(None)
        
        if filepath:
            messagebox.showinfo(self.get_text('msg_saved').split('\n')[0], 
                              self.get_text('msg_saved').format(path=os.path.basename(filepath)))
            self.lbl_status.config(text=self.get_text('status_saved'), fg="green")

    def open_output_folder(self):
        try: os.startfile(self.output_folder)
        except: pass

if __name__ == "__main__":
    app = GifRecorder()