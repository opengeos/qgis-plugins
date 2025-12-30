#!/usr/bin/env python3
"""
Install all QGIS plugins from this repository.

This script automatically discovers and installs all plugin .zip files
from the plugins/ directory to the QGIS plugins folder.
"""

import os
import platform
import zipfile
from pathlib import Path
import shutil
import sys


def get_qgis_plugins_dir():
    """Get the QGIS plugins directory based on the operating system."""
    system = platform.system()
    home = Path.home()

    if system == "Linux":
        plugins_dir = home / ".local/share/QGIS/QGIS3/profiles/default/python/plugins"
    elif system == "Darwin":  # macOS
        plugins_dir = (
            home
            / "Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins"
        )
    elif system == "Windows":
        appdata = os.getenv("APPDATA")
        if not appdata:
            raise RuntimeError("APPDATA environment variable not found")
        plugins_dir = Path(appdata) / "QGIS/QGIS3/profiles/default/python/plugins"
    else:
        raise RuntimeError(f"Unsupported operating system: {system}")

    return plugins_dir


def find_plugin_zips(repo_dir):
    """Find all plugin .zip files in the plugins directory."""
    plugins_dir = repo_dir / "plugins"

    if not plugins_dir.exists():
        raise RuntimeError(f"Plugins directory not found: {plugins_dir}")

    zip_files = list(plugins_dir.glob("*.zip"))

    if not zip_files:
        raise RuntimeError(f"No .zip files found in {plugins_dir}")

    return zip_files


def install_plugin(zip_path, target_dir):
    """Install a single plugin from a .zip file."""
    plugin_name = zip_path.stem

    print(f"Installing {plugin_name}...")

    # Create a temporary directory for extraction
    temp_dir = target_dir / f"_temp_{plugin_name}"

    try:
        # Extract the zip file
        with zipfile.ZipFile(zip_path, "r") as zip_ref:
            zip_ref.extractall(temp_dir)

        # Find the plugin directory (should be the only subdirectory)
        subdirs = [d for d in temp_dir.iterdir() if d.is_dir()]

        if len(subdirs) == 1:
            # Move the plugin directory to the target location
            plugin_dir = subdirs[0]
            final_dir = target_dir / plugin_dir.name

            # Remove existing plugin directory if it exists
            if final_dir.exists():
                shutil.rmtree(final_dir)

            shutil.move(str(plugin_dir), str(final_dir))
            print(f"  ✓ {plugin_name} installed successfully")
        else:
            # If there are multiple directories or files at root, move everything
            final_dir = target_dir / plugin_name

            if final_dir.exists():
                shutil.rmtree(final_dir)

            shutil.move(str(temp_dir), str(final_dir))
            print(f"  ✓ {plugin_name} installed successfully")
            temp_dir = None  # Prevent cleanup since we moved the whole directory

    finally:
        # Clean up temporary directory if it still exists
        if temp_dir and temp_dir.exists():
            shutil.rmtree(temp_dir)


def main():
    """Main installation function."""
    print("QGIS Plugin Installer")
    print("=" * 50)

    # Get repository directory (where this script is located)
    repo_dir = Path(__file__).parent.absolute()
    print(f"Repository: {repo_dir}")

    # Get QGIS plugins directory
    try:
        qgis_plugins_dir = get_qgis_plugins_dir()
    except RuntimeError as e:
        print(f"Error: {e}")
        sys.exit(1)

    print(f"QGIS plugins directory: {qgis_plugins_dir}")

    # Create QGIS plugins directory if it doesn't exist
    if not qgis_plugins_dir.exists():
        print(f"Creating QGIS plugins directory: {qgis_plugins_dir}")
        qgis_plugins_dir.mkdir(parents=True, exist_ok=True)

    # Find all plugin .zip files
    try:
        plugin_zips = find_plugin_zips(repo_dir)
    except RuntimeError as e:
        print(f"Error: {e}")
        sys.exit(1)

    print(f"\nFound {len(plugin_zips)} plugin(s) to install:")
    for zip_file in plugin_zips:
        print(f"  - {zip_file.stem}")

    print("\nInstalling plugins...")
    print("-" * 50)

    # Install each plugin
    installed = 0
    failed = 0

    for zip_file in plugin_zips:
        try:
            install_plugin(zip_file, qgis_plugins_dir)
            installed += 1
        except Exception as e:
            print(f"  ✗ Error installing {zip_file.stem}: {e}")
            failed += 1

    print("-" * 50)
    print(f"\nInstallation complete!")
    print(f"  Successfully installed: {installed}")
    if failed > 0:
        print(f"  Failed: {failed}")

    print("\nPlease restart QGIS and enable the plugins from:")
    print("  Plugins → Manage and Install Plugins → Installed")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
