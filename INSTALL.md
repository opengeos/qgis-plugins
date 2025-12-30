# Plugin Installation Guide

This repository includes automated scripts to install all QGIS plugins at once.

## Quick Start

### One-Line Install (Recommended)

Install all plugins with a single command - no need to clone the repository:

**Linux/macOS:**
```bash
curl -LsSf https://qgis.gishub.org/install.sh | sh
```

**Windows (PowerShell):**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://qgis.gishub.org/install.ps1 | iex"
```

### Local Installation Scripts

If you've cloned this repository, you can use the local scripts:

**Python Script:**
```bash
python3 install_plugins.py
```

**Shell Script:**
```bash
./install_plugins.sh
```

## Features

Both scripts provide the same functionality:

- **Cross-platform support**: Automatically detects Linux, macOS, and Windows
- **Dynamic plugin discovery**: Finds all `.zip` files in the `plugins/` directory
- **Automatic updates**: Works seamlessly when new plugins are added to the repository
- **Safe installation**: Removes old versions before installing new ones
- **Detailed output**: Shows progress for each plugin installation
- **Error handling**: Reports failures while continuing with other plugins

## Platform-Specific Paths

The scripts automatically install plugins to the correct location based on your OS:

| OS | Plugin Directory |
|---------|------------------|
| Linux | `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins` |
| macOS | `~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins` |
| Windows | `%APPDATA%/QGIS/QGIS3/profiles/default/python/plugins` |

## Requirements

### Python Script
- Python 3.10 or higher
- Standard library modules (zipfile, pathlib, platform)

### Shell Script
- Bash shell
- `unzip` command (pre-installed on most systems)

## After Installation

1. Restart QGIS
2. Go to **Plugins** → **Manage and Install Plugins**
3. Click the **Installed** tab
4. Enable the plugins you want to use

## Updating Plugins

To update all plugins to the latest version:

1. Pull the latest changes from this repository:
   ```bash
   git pull
   ```

2. Run the installation script again:
   ```bash
   python3 install_plugins.py
   # or
   ./install_plugins.sh
   ```

The scripts will automatically replace old versions with new ones.

## Uninstalling Plugins

To uninstall plugins, you can either:

1. **Using QGIS GUI**:
   - Go to **Plugins** → **Manage and Install Plugins**
   - Click **Installed** tab
   - Select the plugin and click **Uninstall Plugin**

2. **Manual removal**:
   - Navigate to the plugins directory for your OS (see table above)
   - Delete the plugin folder(s)

## Troubleshooting

### "Permission denied" error

Make sure the scripts are executable:
```bash
chmod +x install_plugins.py install_plugins.sh
```

### "No .zip files found" error

Ensure you're running the script from the repository root directory:
```bash
cd /path/to/qgis-plugins
python3 install_plugins.py
```

### Plugins don't appear in QGIS

1. Verify the plugins were installed:
   - Check the plugins directory for your OS
   - Look for the plugin folders

2. Restart QGIS completely (close all windows)

3. Enable the plugins:
   - **Plugins** → **Manage and Install Plugins** → **Installed**

4. Enable experimental plugins if needed:
   - **Plugins** → **Manage and Install Plugins** → **Settings**
   - Check **Show also experimental plugins**

### Individual plugin fails to install

- Check if the .zip file is corrupted
- Ensure you have write permissions to the QGIS plugins directory
- Check QGIS logs for specific error messages

## Adding New Plugins

When a new plugin is added to this repository:

1. Simply run the installation script again
2. No modifications to the scripts are needed
3. The new plugin will be automatically detected and installed

## Support

For issues specific to:
- **Installation scripts**: Open an issue in this repository
- **Individual plugins**: See the plugin's homepage or issue tracker (listed in README.md)
