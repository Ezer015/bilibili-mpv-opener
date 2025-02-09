#!/usr/bin/env python
import os
import sys
import json
import shutil
from pathlib import Path


def get_native_messaging_paths():
    paths = []

    # Firefox paths
    if sys.platform == "linux" or sys.platform == "linux2":
        paths.append(Path.home() / ".mozilla" / "native-messaging-hosts")
    elif sys.platform == "darwin":
        paths.append(
            Path.home()
            / "Library"
            / "Application Support"
            / "Mozilla"
            / "NativeMessagingHosts"
        )
    elif sys.platform == "win32":
        paths.append(Path(os.getenv("APPDATA")) / "Mozilla" / "NativeMessagingHosts")

    # Chrome paths
    if sys.platform == "linux" or sys.platform == "linux2":
        paths.append(Path.home() / ".config" / "google-chrome" / "NativeMessagingHosts")
    elif sys.platform == "darwin":
        paths.append(
            Path.home()
            / "Library"
            / "Application Support"
            / "Google"
            / "Chrome"
            / "NativeMessagingHosts"
        )
    elif sys.platform == "win32":
        paths.append(
            Path(os.getenv("LOCALAPPDATA"))
            / "Google"
            / "Chrome"
            / "User Data"
            / "NativeMessagingHosts"
        )

    if not paths:
        raise OSError(f"Unsupported platform: {sys.platform}")

    return paths


def get_user_choices():
    print("\nWhich browsers would you like to configure?")
    print("1) Firefox")
    print("2) Chrome")
    print("3) Both")
    while True:
        choice = input("Enter your choice (1-3): ").strip()
        if choice in ["1", "2", "3"]:
            return {"firefox": choice in ["1", "3"], "chrome": choice in ["2", "3"]}
        print("Invalid choice. Please enter 1, 2, or 3.")


def get_chrome_extension_id():
    print("\nChrome extension ID is required.")
    print("1. Go to chrome://extensions/")
    print("2. Enable 'Developer mode'")
    print("3. Look for 'ID' in the extension card")
    while True:
        ext_id = input(
            "Enter Chrome extension ID (or press Enter to skip Chrome setup): "
        ).strip()
        if not ext_id:
            return None
        if not ext_id.startswith("chrome-extension://"):
            ext_id = f"chrome-extension://{ext_id}/"
        return ext_id


def setup_browser(native_path, script_dest, is_chrome, chrome_id=None):
    # Create native messaging directory if it doesn't exist
    native_path.mkdir(parents=True, exist_ok=True)

    # Copy Python script
    shutil.copy2(script_dest, native_path / "open_in_mpv.py")
    (native_path / "open_in_mpv.py").chmod(0o755)  # Make executable

    # Create manifest
    manifest = {
        "name": "open_in_mpv",
        "description": "Native messaging host to open videos in MPV",
        "path": str(native_path / "open_in_mpv.py"),
        "type": "stdio",
        "allowed_origins": (
            [chrome_id]
            if (is_chrome and chrome_id)
            else ["chrome-extension://*/"] if is_chrome else None
        ),
        "allowed_extensions": (
            None if is_chrome else ["bilibili_mpv_opener@example.com"]
        ),
    }

    # Remove None values
    manifest = {k: v for k, v in manifest.items() if v is not None}

    # Save manifest
    manifest_path = native_path / "open_in_mpv.json"
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"\nConfigured for {'Chrome' if is_chrome else 'Firefox'}:")
    print(f"Manifest: {manifest_path}")
    print(f"Script: {native_path}/open_in_mpv.py")


def main():
    try:
        # Get the project root directory
        root_dir = Path(__file__).parent.parent.resolve()
        native_dir = root_dir / "native"
        script_src = native_dir / "open_in_mpv.py"

        print("Bilibili MPV Opener - Native Host Setup")
        print("=======================================")

        # Get user's browser choices
        choices = get_user_choices()

        # Get Chrome extension ID if needed
        chrome_id = None
        if choices["chrome"]:
            chrome_id = get_chrome_extension_id()
            if not chrome_id:
                choices["chrome"] = False
                print("\nSkipping Chrome setup.")

        # Get native messaging paths
        paths = get_native_messaging_paths()

        # Setup for selected browsers
        for path in paths:
            is_chrome = "chrome" in str(path).lower() or "google" in str(path).lower()

            if (is_chrome and choices["chrome"]) or (
                not is_chrome and choices["firefox"]
            ):
                setup_browser(path, script_src, is_chrome, chrome_id)

        print("\nSetup completed successfully!")
        print("\nYou can now use the extension in your configured browser(s).")

    except KeyboardInterrupt:
        print("\nSetup cancelled.")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
        print("\nSetup completed successfully!")
    except Exception as e:
        print(f"\nError during setup: {e}", file=sys.stderr)
        sys.exit(1)
