<div align="center">

# 🎬 Bilibili MPV Opener

一个 Firefox 扩展，通过添加在 MPV 播放器中直接打开视频的功能，增强你的 Bilibili 观看体验。

[English](../README.md) | **简体中文**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Firefox](https://img.shields.io/badge/Firefox-109%2B-FF7139)](https://www.mozilla.org/firefox/new/)
[![MPV](https://img.shields.io/badge/MPV-Latest-7B68EE)](https://mpv.io)

![截图](../docs/images/screenshot.png)

> 适合喜欢 MPV 高级播放功能、更好性能和键盘驱动控制的用户。

</div>

## ✨ 特性

- 🎮 **原生 MPV 集成** - 卓越的播放性能和功能
- 🎯 **通用支持** - 适用于大多数 Bilibili 视频页面
- ⚡ **轻量级** - 最小的资源占用
- 🔄 **Shadow DOM 兼容** - 支持 [bewlybewly](https://github.com/BewlyBewly/BewlyBewly) 扩展的自定义界面

## 🚀 快速开始

1. **安装 MPV 播放器**

   ```bash
   # Ubuntu/Debian
   sudo apt install mpv
   
   # macOS
   brew install mpv
   
   # Windows
   winget install mpv
   ```

2. **获取扩展**
   - 从 [Releases](https://github.com/Ezer015/bilibili-mpv-opener/releases) 下载最新的 `bilibili-mpv-opener-release.zip`
   - 解压缩文件

3. **设置与安装**

   ```bash
   python3 scripts/setup_native_host.py
   ```

   然后在 Firefox 中双击 `bilibili-mpv-opener.xpi`

## 📖 使用方法

1. 访问任意 Bilibili 视频页面
2. 将鼠标悬停在视频封面上并点击 MPV 按钮
3. 视频将自动在 MPV 播放器中打开

## 🛠️ 开发

### 前提条件

- Firefox 109+
- Python 3.x
- MPV 播放器

### 本地测试

```bash
# 安装本地主机
python3 scripts/setup_native_host.py

# 在 Firefox 中加载
about:debugging > 此 Firefox > 临时载入附加组件 > src/manifest.json
```

### 项目结构

```
bilibili-mpv-opener/
├── src/                  # 扩展源码
│   ├── manifest.json     # 扩展清单
│   ├── content.js        # 内容脚本
│   └── background.js     # 后台脚本
├── native/              # 本地消息传递
│   └── open_in_mpv.py   # MPV 集成
├── scripts/             # 实用工具
│   ├── setup_native_host.py
│   └── make_dist.py
└── docs/               # 文档
```

### 发布流程

1. 更新 `src/manifest.json` 中的版本
2. 推送到主分支
3. GitHub Actions 自动：
   - 验证版本更新
   - 构建发行版
   - 创建发布

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](../LICENSE) 文件。
