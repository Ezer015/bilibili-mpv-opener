#!/usr/bin/env python3
import os
import sys
import json
import shutil
from pathlib import Path

def get_native_messaging_path():
    if sys.platform == "linux" or sys.platform == "linux2":
        return Path.home() / ".mozilla" / "native-messaging-hosts"
    elif sys.platform == "darwin":
        return Path.home() / "Library" / "Application Support" / "Mozilla" / "NativeMessagingHosts"
    elif sys.platform == "win32":
        return Path(os.getenv('APPDATA')) / "Mozilla" / "NativeMessagingHosts"
    else:
        raise OSError(f"Unsupported platform: {sys.platform}")

def main():
    # Get the project root directory (parent of scripts/)
    root_dir = Path(__file__).parent.parent.absolute()
    native_dir = root_dir / "native"
    
    # Create native messaging directory if it doesn't exist
    native_path = get_native_messaging_path()
    native_path.mkdir(parents=True, exist_ok=True)
    
    # Copy Python script from native directory
    script_dest = native_path / "open_in_mpv.py"
    shutil.copy2(native_dir / "open_in_mpv.py", script_dest)
    script_dest.chmod(0o755)  # Make executable
    
    # Create and save manifest with correct path
    manifest = {
        "name": "open_in_mpv",
        "description": "Native messaging host to open videos in MPV",
        "path": str(script_dest),
        "type": "stdio",
        "allowed_extensions": ["bilibili_mpv_opener@example.com"]
    }
    
    manifest_path = native_path / "open_in_mpv.json"
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)
    
    print("Native messaging host installation complete!")
    print(f"Manifest installed at: {manifest_path}")
    print(f"Python script installed at: {script_dest}")

if __name__ == "__main__":
    try:
        main()
        print("\nSetup completed successfully!")
    except Exception as e:
        print(f"Error during setup: {e}", file=sys.stderr)
        sys.exit(1)
