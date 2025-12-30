#!/bin/bash

###############################################################################
# QGIS Plugins One-Line Installer
# Usage: curl -LsSf https://qgis.gishub.org/install.sh | bash
###############################################################################

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_info() { echo -e "${BLUE}$1${NC}"; }
print_success() { echo -e "${GREEN}$1${NC}"; }
print_error() { echo -e "${RED}$1${NC}"; }
print_warning() { echo -e "${YELLOW}$1${NC}"; }

# Function to get QGIS plugins directory
get_qgis_plugins_dir() {
    local os_type=$(uname -s)
    case "$os_type" in
        Linux*)
            echo "$HOME/.local/share/QGIS/QGIS3/profiles/default/python/plugins"
            ;;
        Darwin*)
            echo "$HOME/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins"
            ;;
        *)
            print_error "Unsupported OS: $os_type. Use install.ps1 for Windows."
            exit 1
            ;;
    esac
}

# Function to download and install a plugin
install_plugin() {
    local plugin_name="$1"
    local base_url="$2"
    local target_dir="$3"

    print_info "Installing $plugin_name..."

    local temp_zip="/tmp/${plugin_name}.zip"
    local temp_dir="/tmp/_qgis_${plugin_name}_$$"

    # Download plugin
    if ! curl -fsSL "${base_url}/plugins/${plugin_name}.zip" -o "$temp_zip"; then
        print_error "  ✗ Failed to download $plugin_name"
        return 1
    fi

    # Extract plugin
    mkdir -p "$temp_dir"
    if ! unzip -q "$temp_zip" -d "$temp_dir" < /dev/null 2>/dev/null; then
        print_error "  ✗ Failed to extract $plugin_name"
        rm -f "$temp_zip"
        rm -rf "$temp_dir"
        return 1
    fi

    # Find plugin directory
    local plugin_dir=$(find "$temp_dir" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | head -n 1 < /dev/null)

    if [ -n "$plugin_dir" ]; then
        local plugin_basename=$(basename "$plugin_dir")
        local final_dir="$target_dir/$plugin_basename"

        # Remove existing plugin
        [ -d "$final_dir" ] && rm -rf "$final_dir"

        # Move plugin to final location
        if mv "$plugin_dir" "$final_dir" 2>/dev/null; then
            print_success "  ✓ $plugin_name installed"
        else
            print_error "  ✗ Failed to install $plugin_name"
            rm -f "$temp_zip"
            rm -rf "$temp_dir"
            return 1
        fi
    fi

    # Cleanup
    rm -f "$temp_zip"
    rm -rf "$temp_dir"
    return 0
}

main() {
    echo ""
    print_info "╔════════════════════════════════════════╗"
    print_info "║   QGIS Plugins Installer (OpenGeos)   ║"
    print_info "╔════════════════════════════════════════╗"
    echo ""

    # Get QGIS plugins directory
    QGIS_PLUGINS_DIR=$(get_qgis_plugins_dir)
    print_info "Target directory: $QGIS_PLUGINS_DIR"

    # Create directory if needed
    mkdir -p "$QGIS_PLUGINS_DIR"

    # Base URL for plugins
    BASE_URL="https://qgis.gishub.org"

    # List of all plugins
    PLUGINS=(
        "geoai"
        "samgeo"
        "whitebox_agent"
        "hypercoast"
        "maxar_open_data"
        "nasa_earthdata"
        "nasa_opera"
        "qgis_geemap"
        "gee_data_catalogs"
        "timelapse"
        "qgis_leafmap"
        "qgis_notebook"
        "plugin_template"
    )

    echo ""
    print_info "Installing ${#PLUGINS[@]} plugins..."
    echo ""

    installed=0
    failed=0

    for plugin in "${PLUGINS[@]}"; do
        if install_plugin "$plugin" "$BASE_URL" "$QGIS_PLUGINS_DIR"; then
            installed=$((installed + 1))
        else
            failed=$((failed + 1))
        fi
    done

    echo ""
    print_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    print_success "✓ Installation complete!"
    print_success "  Successfully installed: $installed"
    [ $failed -gt 0 ] && print_warning "  Failed: $failed"
    echo ""
    print_info "Next steps:"
    print_info "  1. Restart QGIS"
    print_info "  2. Go to: Plugins → Manage and Install Plugins"
    print_info "  3. Enable plugins in the 'Installed' tab"
    echo ""
    print_info "For more info: https://github.com/opengeos/qgis-plugins"
    print_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""

    return $failed
}

# Check for required commands
for cmd in curl unzip; do
    if ! command -v $cmd &> /dev/null; then
        print_error "Error: '$cmd' is required but not installed."
        exit 1
    fi
done

main
exit $?
