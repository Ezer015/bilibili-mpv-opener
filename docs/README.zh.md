<div align="center">

# 🎬 Bilibili MPV Opener

一个浏览器扩展，通过添加在 MPV 播放器中直接打开视频的功能，增强你的 Bilibili 观看体验。

[English](../README.md) | **简体中文**

[![Version](https://img.shields.io/github/v/release/Ezer015/bilibili-mpv-opener?color=brightgreen&label=Release&style=flat-square)](https://github.com/Ezer015/bilibili-mpv-opener/releases)
[![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)](https://opensource.org/licenses/MIT)
[![Firefox](https://img.shields.io/badge/Firefox-Support-FF7139?style=flat-square&logo=firefox)](https://www.mozilla.org/firefox/new/)
[![Chrome](https://img.shields.io/badge/Chrome-Support-4285F4?style=flat-square&logo=googlechrome)](https://www.google.com/chrome/)

![截图](../docs/images/screenshot.png)

> 适合喜欢 MPV 高级播放功能、更好性能和键盘驱动控制的用户。

</div>

## ✨ 特性

- 🎮 **原生 MPV 集成** - 卓越的播放性能和功能
- 🎯 **通用支持** - 适用于大多数 Bilibili 视频页面
- ⚡ **轻量级** - 最小的资源占用
- 🔄 **Shadow DOM 兼容** - 支持 [bewlybewly](https://github.com/BewlyBewly/BewlyBewly) 扩展的自定义界面

## 🚀 快速开始

1. **安装 MPV 播放器和 yt-dlp**

   ```bash
   # Ubuntu/Debian
   sudo apt install mpv yt-dlp
   
   # macOS
   brew install mpv yt-dlp
   
   # Windows
   winget install mpv yt-dlp
   ```

2. **获取扩展**
   - 从 [Releases](https://github.com/Ezer015/bilibili-mpv-opener/releases) 下载最新的 `bilibili-mpv-opener-release.zip`
   - 解压缩文件

3. **设置与安装**

   1. 根据你的浏览器安装扩展：

      **Firefox**：
      - 双击 `firefox/bilibili-mpv-opener.xpi`

      **Chrome**：
      1. 解压 `chrome/bilibili-mpv-opener.zip`
      2. 访问 `chrome://extensions/`
      3. 打开右上角的"开发者模式"
      4. 点击"加载已解压的扩展程序"并选择解压后的文件夹
      5. 从扩展卡片中复制你的扩展ID

   2. 运行安装脚本：

      ```bash
      # Linux/macOS：
      python3 scripts/setup.py

      # Windows：
      python scripts\setup.py
      ```

      然后根据提示：
      - 选择需要配置的浏览器
      - 如果选择 Chrome，需要提供扩展ID

## 📖 使用方法

1. 访问任意 Bilibili 视频页面
2. 将鼠标悬停在视频封面上并点击 MPV 按钮
3. 视频将自动在 MPV 播放器中打开

## 🛠️ 开发

### 前提条件

- Firefox / Chrome
- Python 3.x
- MPV 播放器
- yt-dlp

### 本地测试

1. 运行开发配置：

   ```bash
   python3 scripts/dev_setup.py
   ```

   按照提示选择你的浏览器。脚本会创建相应配置的 manifest.json。

2. 加载扩展：
   - 脚本会显示特定浏览器的加载说明

3. 运行安装脚本：

   ```bash
   python3 scripts/setup.py
   ```

发行版构建过程使用 manifest.base.json 为每个浏览器创建适当的清单文件。

### 发布流程

1. 更新 `src/manifest.base.json` 中的版本
2. 推送到主分支
3. GitHub Actions 自动：
   - 验证版本更新
   - 构建发行版
   - 创建发布

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](../LICENSE) 文件。
