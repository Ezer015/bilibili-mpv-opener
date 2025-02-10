<div align="center">

# 🎬 Bilibili MPV Opener

A browser extension that enhances your Bilibili viewing experience by adding the ability to open videos directly in MPV player.

**English** | [简体中文](docs/README.zh.md)

[![Version](https://img.shields.io/github/v/release/Ezer015/bilibili-mpv-opener?color=brightgreen&label=Release&style=flat-square)](https://github.com/Ezer015/bilibili-mpv-opener/releases)
[![License](https://img.shields.io/badge/License-MIT-blue?style=flat-square)](https://opensource.org/licenses/MIT)
[![Firefox](https://img.shields.io/badge/Firefox-Support-FF7139?style=flat-square&logo=firefox)](https://www.mozilla.org/firefox/new/)
[![Chrome](https://img.shields.io/badge/Chrome-Support-4285F4?style=flat-square&logo=googlechrome)](https://www.google.com/chrome/)

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

   1. Install the extension for your browser:

      **Firefox**:
      - Double-click `firefox/bilibili-mpv-opener.xpi`

      **Chrome**:
      1. Extract `chrome/bilibili-mpv-opener.zip`
      2. Go to `chrome://extensions/`
      3. Enable "Developer mode" in the top-right
      4. Click "Load unpacked" and select the extracted folder
      5. Copy your extension ID from the extension card

   2. Run the setup script:

      ```bash
      # Linux/macOS:
      python3 scripts/setup.py

      # Windows:
      python scripts\setup.py
      ```

      Then follow the prompts to:
      - Choose which browser(s) to configure
      - For Chrome, provide your extension ID when prompted

## 📖 Usage

1. Visit any Bilibili video page
2. Hover over the video cover and click the MPV button
3. Video opens automatically in MPV player

## 🛠️ Development

### Prerequisites

- Firefox / Chrome
- Python 3.x
- MPV player

### Local Testing

1. Run development setup:

   ```bash
   python3 scripts/dev_setup.py
   ```

   Follow the prompts to select your browser. This will create manifest.json with the appropriate settings.

2. Load the extension:
   - The script will display browser-specific loading instructions

3. Run setup script:

   ```bash
   python3 scripts/setup.py
   ```

The release build process uses manifest.base.json to create appropriate manifests for each browser.

### Release Process

1. Update version in `src/manifest.base.json`
2. Push to main branch
3. GitHub Actions automatically:
   - Verifies version update
   - Builds distribution
   - Creates release

## 📄 License

This project is MIT licensed - see [LICENSE](LICENSE) file.
