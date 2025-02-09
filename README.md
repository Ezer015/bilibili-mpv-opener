<div align="center">

# 🎬 Bilibili MPV Opener

A Firefox extension that enhances your Bilibili viewing experience by adding the ability to open videos directly in MPV player.

**English** | [简体中文](docs/README.zh.md)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Firefox](https://img.shields.io/badge/Firefox-109%2B-FF7139)](https://www.mozilla.org/firefox/new/)
[![MPV](https://img.shields.io/badge/MPV-Latest-7B68EE)](https://mpv.io)

![Screenshot](docs/images/screenshot.png)

> Perfect for users who prefer MPV's advanced playback features, better performance, and keyboard-driven controls.

</div>

## ✨ Features

- 🎮 **Native MPV Integration** - Superior playback performance and features
- 🎯 **Universal Support** - Works on most Bilibili video pages
- ⚡ **Lightweight** - Minimal resource usage
- 🔄 **Shadow DOM Compatible** - Support for [bewlybewly](https://github.com/BewlyBewly/BewlyBewly) extension's custom UI

## 🚀 Quick Start

1. **Install MPV Player**

   ```bash
   # Ubuntu/Debian
   sudo apt install mpv
   
   # macOS
   brew install mpv
   
   # Windows
   winget install mpv
   ```

2. **Get the Extension**
   - Download latest `bilibili-mpv-opener-release.zip` from [Releases](https://github.com/Ezer015/bilibili-mpv-opener/releases)
   - Extract the archive

3. **Setup & Install**

   ```bash
   python3 scripts/setup_native_host.py
   ```

   Then double-click `bilibili-mpv-opener.xpi` in Firefox

## 📖 Usage

1. Visit any Bilibili video page
2. Hover over the video cover and click the MPV button
3. Video opens automatically in MPV player

## 🛠️ Development

### Prerequisites

- Firefox 109+
- Python 3.x
- MPV player

### Local Testing

```bash
# Install native host
python3 scripts/setup_native_host.py

# Load in Firefox
about:debugging > This Firefox > Load Temporary Add-on > src/manifest.json
```

### Project Structure

```
bilibili-mpv-opener/
├── src/                  # Extension source
│   ├── manifest.json     # Extension manifest
│   ├── content.js        # Content script
│   └── background.js     # Background script
├── native/              # Native messaging
│   └── open_in_mpv.py   # MPV integration
├── scripts/             # Utilities
│   ├── setup_native_host.py
│   └── make_dist.py
└── docs/               # Documentation
```

### Release Process

1. Update version in `src/manifest.json`
2. Push to main branch
3. GitHub Actions automatically:
   - Verifies version update
   - Builds distribution
   - Creates release

## 📄 License

This project is MIT licensed - see [LICENSE](LICENSE) file.
