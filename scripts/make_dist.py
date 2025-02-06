#!/usr/bin/env python3
import os
import shutil
from pathlib import Path
import zipfile
import tempfile

def clean_dist():
    dist_dir = Path("dist")
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    dist_dir.mkdir()

def create_extension_xpi(temp_dir):
    print("Creating extension xpi...")
    root_dir = Path(__file__).parent.parent
    src_dir = root_dir / "src"
    xpi_path = temp_dir / "bilibili-mpv-opener.xpi"
    
    # Create extension xpi (only extension files)
    with zipfile.ZipFile(xpi_path, "w", zipfile.ZIP_DEFLATED) as zf:
        # Add only extension source files
        for file in ["manifest.json", "content.js", "background.js"]:
            zf.write(src_dir / file, file)  # Write directly in root of xpi
    
    return xpi_path

def create_distribution_package():
    print("Creating distribution package...")
    root_dir = Path(__file__).parent.parent
    
    # Create temporary directory for build artifacts
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        xpi_path = create_extension_xpi(temp_path)
        
        # Create distribution package
        with zipfile.ZipFile("dist/bilibili-mpv-opener-release.zip", "w", zipfile.ZIP_DEFLATED) as zf:
            # Add the xpi
            zf.write(xpi_path, "bilibili-mpv-opener.xpi")
            
            # Add native messaging host
            zf.write(root_dir / "native" / "open_in_mpv.py", "native/open_in_mpv.py")
                
            # Add setup script
            zf.write(root_dir / "scripts" / "setup_native_host.py", "scripts/setup_native_host.py")
                
            # Add documentation
            zf.write(root_dir / "README.md", "README.md")
    
    print("Distribution package created at dist/bilibili-mpv-opener-release.zip")

def main():
    # Ensure we're in the project root
    os.chdir(Path(__file__).parent.parent)
    
    # Clean and create dist directory
    clean_dist()
    
    # Create distribution package (includes temporary xpi)
    create_distribution_package()

if __name__ == "__main__":
    main()
