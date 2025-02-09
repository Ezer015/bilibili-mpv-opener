#!/usr/bin/env python3
import json
import sys
from pathlib import Path


def get_browser_choice():
    print("\nWhich browser would you like to configure for development?")
    print("1) Firefox")
    print("2) Chrome")
    while True:
        choice = input("Enter your choice (1-2): ").strip()
        if choice == "1":
            return "firefox"
        elif choice == "2":
            return "chrome"
        print("Invalid choice. Please enter 1 or 2.")


def setup_manifest(browser):
    src_dir = Path(__file__).parent.parent / "src"
    manifest_path = src_dir / "manifest.json"
    base_manifest_path = src_dir / "manifest.base.json"

    # Read base manifest
    print("\nReading base manifest...")
    with open(base_manifest_path, "r") as f:
        manifest = json.load(f)

    # Configure for specified browser
    print(f"Configuring for {browser.title()}...")
    if browser == "firefox":
        manifest["background"] = {"scripts": ["background.js"]}
        manifest["browser_specific_settings"] = {
            "gecko": {"id": "bilibili_mpv_opener@example.com"}
        }
    else:  # chrome
        manifest["background"] = {"service_worker": "background.js"}

    # Write updated manifest
    print("Creating development manifest.json...")
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)

    print("\n✅ Development manifest created successfully!")
    print("\nNext steps:")
    if browser == "firefox":
        print("1. Go to about:debugging")
        print("2. Click 'This Firefox'")
        print("3. Click 'Load Temporary Add-on'")
        print("4. Select src/manifest.json")
    else:
        print("1. Go to chrome://extensions")
        print("2. Enable 'Developer mode'")
        print("3. Click 'Load unpacked'")
        print("4. Select the src folder")

    print("\nNote: Run setup.py after loading the extension if you haven't already.")


def main():
    try:
        print("Bilibili MPV Opener - Development Setup")
        print("======================================")

        browser = get_browser_choice()
        setup_manifest(browser)

    except KeyboardInterrupt:
        print("\nSetup cancelled.")
        sys.exit(1)
    except Exception as e:
        print(f"\nError during setup: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
