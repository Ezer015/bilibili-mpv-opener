# Bilibili MPV Opener

A Firefox extension that opens Bilibili videos in MPV player.

## Project Structure

```
bilibili-mpv-opener/
├── src/                  # Extension source code
│   ├── manifest.json     # Extension manifest
│   ├── content.js        # Content script
│   └── background.js     # Background script
├── native/              # Native messaging host
│   └── open_in_mpv.py   # Native messaging implementation
├── scripts/             # Installation scripts
│   ├── setup_native_host.py  # Native host setup script
│   └── make_dist.py     # Distribution package creation script
├── dist/               # Distribution packages
│   └── bilibili-mpv-opener-release.zip  # Complete distribution package
└── README.md            # Documentation
```

## Requirements

- MPV player installed on your system
- Python 3.x
- Firefox browser

## Development

### Building a Release

1. Make sure all your changes are committed
2. Update version number in `src/manifest.json` if needed
3. Build the distribution package:
   ```bash
   python3 scripts/make_dist.py
   ```
4. The release package will be created at `dist/bilibili-mpv-opener-full.zip`

### Testing Locally

1. Run `python3 scripts/setup_native_host.py` to install the native messaging host
2. In Firefox:
   - Go to about:debugging
   - Click "This Firefox"
   - Click "Load Temporary Add-on"
   - Navigate to the `src/` directory
   - Select manifest.json

## Installation (For Users)

1. Download and extract bilibili-mpv-opener-full.zip
2. Run the setup script to install native messaging host:
   ```bash
   python3 scripts/setup_native_host.py
   ```
3. Install the extension in Firefox:
   - Double-click `bilibili-mpv-opener.xpi` from the extracted files
   - Click "Install" when Firefox prompts
   - Click "Add" when prompted for permissions

## How it works

This extension adds a button to Bilibili video pages that allows you to open the video in MPV player instead of watching in the browser. It uses Firefox's native messaging to communicate with MPV on your system.
