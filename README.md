#  EasyGIF Recorder | 简易屏幕录制工具

> 一个轻量级、无需安装的 Windows 屏幕 GIF 录制工具。
> A lightweight, portable screen to GIF recorder for Windows.

[中文介绍](#-中文介绍) | [English](#-english-introduction)

---

##  中文介绍

**EasyGIF** 是一个完全基于 Python 开发的开源工具，旨在解决“为了录个 GIF 还要下载巨大软件”的烦恼。它体积小巧，操作直观，生成的 GIF 清晰度高且体积适中。

###  核心功能
* **自由选区**：支持鼠标拖拽，精确选择屏幕上的任意区域进行录制。
* **双语界面**：内置中文/英文一键切换，国际化体验。
* **极简操作**：选区 -> 录制 -> 自动保存，三步搞定。
* **一键直达**：录制完成后，可直接打开文件所在文件夹， 方便快捷。
* **高分屏支持**：自动适配 Windows 缩放（DPI Awareness），选区不偏移。

###  下载与使用

**1. 直接使用（推荐普通用户）**
- 从 GitHub Releases 页面下载最新的 `.exe` 文件
- 无需安装 Python，下载即用
- 文件体积仅约 30MB

**2. 源码运行（开发者）**
如果你想修改代码或从源码运行：
```bash
# 1. 克隆仓库
git clone https://github.com/Reginold-keep/EasyGIF-Recorder.git

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行
python gif_recorder.py
```

**3. 自行打包**
```bash
# 使用 PyInstaller 打包为单个可执行文件
pyinstaller -F EasyGIF_Lite.spec
```

### 技术栈
* **语言**: Python 3.x
* **GUI**: Tkinter (原生库)
* **图像处理**: Pillow (PIL), Imageio
* **打包**: PyInstaller

### 使用说明
1. 打开 EasyGIF Recorder 应用程序
2. 点击「选择区域」按钮，或直接拖拽鼠标选择要录制的屏幕区域
3. 点击「开始录制」按钮开始录制
4. 点击「停止录制」按钮结束录制
5. 录制完成后，GIF 文件将自动保存到 `output_gifs` 文件夹

---

##  English Introduction

**EasyGIF** is an open-source tool developed entirely based on Python, designed to solve the trouble of "downloading huge software just to record a GIF". It is small in size, intuitive to operate, and generates high-quality GIFs with moderate file size.

###  Core Features
* **Free Selection**: Support mouse drag to precisely select any area on the screen for recording.
* **Bilingual Interface**: Built-in Chinese/English one-click switching for international experience.
* **Minimalist Operation**: Selection -> Recording -> Auto-save, three steps to get it done.
* **One-click Access**: After recording, you can directly open the folder where the file is located, convenient and fast.
* **High DPI Support**: Automatically adapt to Windows scaling (DPI Awareness), no selection offset.

### Download and Use

**1. Direct Use (Recommended for general users)**
- Download the latest `.exe` file from GitHub Releases page
- No need to install Python, ready to use after download
- File size is only about 30MB

**2. Run from Source (For developers)**
If you want to modify the code or run from source:
```bash
# 1. Clone the repository
git clone https://github.com/Reginold-keep/EasyGIF-Recorder.git

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run
python gif_recorder.py
```

**3. Package by Yourself**
```bash
# Package as a single executable file using PyInstaller
pyinstaller -F EasyGIF.spec
```

### Technology Stack
* **Language**: Python 3.x
* **GUI**: Tkinter (native library)
* **Image Processing**: Pillow (PIL), Imageio
* **Packaging**: PyInstaller

### Usage Instructions
1. Open EasyGIF Recorder application
2. Click the "Select Area" button, or directly drag the mouse to select the screen area you want to record
3. Click the "Start Recording" button to start recording
4. Click the "Stop Recording" button to end recording
5. After recording, the GIF file will be automatically saved to the `output_gifs` folder

---

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

---

##  问题反馈

如果您在使用过程中遇到问题，欢迎通过以下方式反馈：

- [GitHub Issues](https://github.com/Reginold-keep/EasyGIF-Recorder/issues)
- 邮箱：yex8605@gmail.com

---

## 作者

**Reginold-keep**
- GitHub: [@Reginold-keep](https://github.com/Reginold-keep)
- 邮箱：yex8605@gmail.com

---

## 支持项目

如果您觉得这个项目对您有帮助，请给它一个 Star ?！

---

## 项目结构

```
EasyGIF-Recorder/
│
├── gif_recorder.py        # 主程序
├── requirements.txt       # 依赖库
├── EasyGIF_V5.spec      # PyInstaller 打包配置
├── output_gifs/           # 输出的 GIF 文件夹
├── README.md              # 项目说明文档
└── LICENSE                # MIT 许可证
```
