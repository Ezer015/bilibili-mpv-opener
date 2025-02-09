#!/usr/bin/env python3
import json
import shutil
from pathlib import Path
import zipfile
import tempfile


def clean_dist():
    dist_dir = Path("dist")
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    dist_dir.mkdir()


def create_browser_manifest(base_manifest_path, is_chrome):
    with open(base_manifest_path, "r") as f:
        manifest = json.load(f)

    if is_chrome:
        manifest["background"] = {"service_worker": "background.js"}
    else:  # Firefox
        manifest["background"] = {"scripts": ["background.js"]}
        manifest["browser_specific_settings"] = {
            "gecko": {"id": "bilibili_mpv_opener@example.com"}
        }

    return manifest


def create_extension_xpi(temp_dir, root_dir, src_dir):
    print("Creating Firefox extension package (xpi)...")
    firefox_dir = temp_dir / "firefox"
    firefox_dir.mkdir()

    # Copy extension files
    for file in ["content.js", "background.js"]:
        shutil.copy2(src_dir / file, firefox_dir / file)

    # Create Firefox-specific manifest
    manifest = create_browser_manifest(src_dir / "manifest.base.json", is_chrome=False)
    manifest_path = firefox_dir / "manifest.json"
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)

    # Create xpi package
    xpi_path = temp_dir / "bilibili-mpv-opener.xpi"
    with zipfile.ZipFile(xpi_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for file in ["manifest.json", "content.js", "background.js"]:
            zf.write(firefox_dir / file, file)

    return xpi_path


def create_chrome_package(temp_dir, root_dir, src_dir):
    print("Creating Chrome extension package...")
    chrome_dir = temp_dir / "chrome"
    chrome_dir.mkdir()

    # Copy extension files
    for file in ["content.js", "background.js"]:
        shutil.copy2(src_dir / file, chrome_dir / file)

    # Create Chrome-specific manifest
    manifest = create_browser_manifest(src_dir / "manifest.base.json", is_chrome=True)
    manifest_path = chrome_dir / "manifest.json"
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)

    # Create zip for unpacked extension
    chrome_zip = temp_dir / "bilibili-mpv-opener.zip"
    with zipfile.ZipFile(chrome_zip, "w", zipfile.ZIP_DEFLATED) as zf:
        for file in ["manifest.json", "content.js", "background.js"]:
            zf.write(chrome_dir / file, file)

    return chrome_zip


def create_distribution_package():
    print("Creating distribution package...")
    root_dir = Path(__file__).parent.parent
    src_dir = root_dir / "src"

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        xpi_path = create_extension_xpi(temp_path, root_dir, src_dir)
        chrome_zip = create_chrome_package(temp_path, root_dir, src_dir)

        with zipfile.ZipFile(
            "dist/bilibili-mpv-opener-release.zip", "w", zipfile.ZIP_DEFLATED
        ) as zf:
            # Add browser extensions
            zf.write(xpi_path, "firefox/bilibili-mpv-opener.xpi")
            zf.write(chrome_zip, "chrome/bilibili-mpv-opener.zip")

            # Add Python scripts
            zf.write(root_dir / "native" / "open_in_mpv.py", "native/open_in_mpv.py")
            zf.write(root_dir / "scripts" / "setup.py", "scripts/setup.py")

    print("Distribution package created at dist/bilibili-mpv-opener-release.zip")


def main():
    clean_dist()
    create_distribution_package()


if __name__ == "__main__":
    main()
