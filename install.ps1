# QGIS Plugins One-Line Installer for Windows
# Usage: powershell -ExecutionPolicy ByPass -c "irm https://qgis.gishub.org/install.ps1 | iex"

$ErrorActionPreference = "Stop"

# Function to write colored output
function Write-Info {
    param([string]$Message)
    Write-Host $Message -ForegroundColor Cyan
}

function Write-Success {
    param([string]$Message)
    Write-Host $Message -ForegroundColor Green
}

function Write-Error {
    param([string]$Message)
    Write-Host $Message -ForegroundColor Red
}

function Write-Warning {
    param([string]$Message)
    Write-Host $Message -ForegroundColor Yellow
}

# Function to get QGIS plugins directory
function Get-QGISPluginsDir {
    $appData = [Environment]::GetFolderPath('ApplicationData')
    return Join-Path $appData "QGIS\QGIS3\profiles\default\python\plugins"
}

# Function to download and install a plugin
function Install-Plugin {
    param(
        [string]$PluginName,
        [string]$BaseUrl,
        [string]$TargetDir
    )

    Write-Info "Installing $PluginName..."

    $tempZip = Join-Path $env:TEMP "$PluginName.zip"
    $tempDir = Join-Path $env:TEMP "_qgis_${PluginName}_$(Get-Random)"

    try {
        # Download plugin
        $downloadUrl = "$BaseUrl/plugins/$PluginName.zip"
        Invoke-WebRequest -Uri $downloadUrl -OutFile $tempZip -UseBasicParsing

        # Extract plugin
        Expand-Archive -Path $tempZip -DestinationPath $tempDir -Force

        # Find plugin directory (should be the only subdirectory)
        $pluginDir = Get-ChildItem -Path $tempDir -Directory | Select-Object -First 1

        if ($pluginDir) {
            $finalDir = Join-Path $TargetDir $pluginDir.Name

            # Remove existing plugin if it exists
            if (Test-Path $finalDir) {
                Remove-Item $finalDir -Recurse -Force
            }

            # Move plugin to final location
            Move-Item -Path $pluginDir.FullName -Destination $finalDir
            Write-Success "  ✓ $PluginName installed"
            return $true
        }
        else {
            Write-Error "  ✗ Failed to find plugin directory for $PluginName"
            return $false
        }
    }
    catch {
        Write-Error "  ✗ Failed to install $PluginName : $_"
        return $false
    }
    finally {
        # Cleanup
        if (Test-Path $tempZip) { Remove-Item $tempZip -Force }
        if (Test-Path $tempDir) { Remove-Item $tempDir -Recurse -Force }
    }
}

# Main installation function
function Main {
    Write-Host ""
    Write-Info "╔════════════════════════════════════════╗"
    Write-Info "║   QGIS Plugins Installer (OpenGeos)   ║"
    Write-Info "╔════════════════════════════════════════╗"
    Write-Host ""

    # Get QGIS plugins directory
    $qgisPluginsDir = Get-QGISPluginsDir
    Write-Info "Target directory: $qgisPluginsDir"

    # Create directory if needed
    if (-not (Test-Path $qgisPluginsDir)) {
        Write-Info "Creating QGIS plugins directory..."
        New-Item -ItemType Directory -Path $qgisPluginsDir -Force | Out-Null
    }

    # Base URL for plugins
    $baseUrl = "https://qgis.gishub.org"

    # List of all plugins
    $plugins = @(
        "geoai",
        "samgeo",
        "whitebox_agent",
        "hypercoast",
        "maxar_open_data",
        "nasa_earthdata",
        "nasa_opera",
        "qgis_geemap",
        "gee_data_catalogs",
        "timelapse",
        "qgis_leafmap",
        "qgis_notebook",
        "plugin_template"
    )

    Write-Host ""
    Write-Info "Installing $($plugins.Count) plugins..."
    Write-Host ""

    $installed = 0
    $failed = 0

    foreach ($plugin in $plugins) {
        if (Install-Plugin -PluginName $plugin -BaseUrl $baseUrl -TargetDir $qgisPluginsDir) {
            $installed++
        }
        else {
            $failed++
        }
    }

    Write-Host ""
    Write-Info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    Write-Success "✓ Installation complete!"
    Write-Success "  Successfully installed: $installed"
    if ($failed -gt 0) {
        Write-Warning "  Failed: $failed"
    }
    Write-Host ""
    Write-Info "Next steps:"
    Write-Info "  1. Restart QGIS"
    Write-Info "  2. Go to: Plugins → Manage and Install Plugins"
    Write-Info "  3. Enable plugins in the 'Installed' tab"
    Write-Host ""
    Write-Info "For more info: https://github.com/opengeos/qgis-plugins"
    Write-Info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    Write-Host ""

    if ($failed -gt 0) {
        exit 1
    }
}

# Run main function
Main
