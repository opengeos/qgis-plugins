#!/bin/bash

###############################################################################
# QGIS Plugin Installer (Shell Script)
#
# This script automatically discovers and installs all plugin .zip files
# from the plugins/ directory to the QGIS plugins folder.
###############################################################################

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}$1${NC}"
}

print_success() {
    echo -e "${GREEN}$1${NC}"
}

print_error() {
    echo -e "${RED}$1${NC}"
}

print_warning() {
    echo -e "${YELLOW}$1${NC}"
}

# Function to get QGIS plugins directory based on OS
get_qgis_plugins_dir() {
    local os_type=$(uname -s)

    case "$os_type" in
        Linux*)
            echo "$HOME/.local/share/QGIS/QGIS3/profiles/default/python/plugins"
            ;;
        Darwin*)
            echo "$HOME/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins"
            ;;
        MINGW*|MSYS*|CYGWIN*)
            # Windows (Git Bash, MSYS2, or Cygwin)
            if [ -n "$APPDATA" ]; then
                echo "$APPDATA/QGIS/QGIS3/profiles/default/python/plugins"
            else
                print_error "Error: APPDATA environment variable not found"
                exit 1
            fi
            ;;
        *)
            print_error "Error: Unsupported operating system: $os_type"
            exit 1
            ;;
    esac
}

# Function to install a single plugin
install_plugin() {
    local zip_file="$1"
    local target_dir="$2"
    local plugin_name=$(basename "$zip_file" .zip)

    print_info "Installing $plugin_name..."

    # Create temporary directory
    local temp_dir="$target_dir/_temp_$plugin_name"
    mkdir -p "$temp_dir"

    # Extract zip file
    if ! unzip -q "$zip_file" -d "$temp_dir"; then
        print_error "  ✗ Failed to extract $plugin_name"
        rm -rf "$temp_dir"
        return 1
    fi

    # Find the plugin directory (usually the only subdirectory)
    local plugin_dir=$(find "$temp_dir" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | head -n 1)

    if [ -n "$plugin_dir" ]; then
        local plugin_basename=$(basename "$plugin_dir")
        local final_dir="$target_dir/$plugin_basename"

        # Remove existing plugin if it exists
        if [ -d "$final_dir" ]; then
            rm -rf "$final_dir" 2>/dev/null || true
        fi

        # Move plugin to final location
        if mv "$plugin_dir" "$final_dir" 2>/dev/null; then
            print_success "  ✓ $plugin_name installed successfully"
        else
            print_error "  ✗ Failed to move $plugin_name to final location"
            rm -rf "$temp_dir" 2>/dev/null || true
            return 1
        fi
    else
        # If no subdirectory found, move the whole temp directory
        local final_dir="$target_dir/$plugin_name"

        if [ -d "$final_dir" ]; then
            rm -rf "$final_dir" 2>/dev/null || true
        fi

        if mv "$temp_dir" "$final_dir" 2>/dev/null; then
            print_success "  ✓ $plugin_name installed successfully"
            temp_dir=""  # Prevent cleanup
        else
            print_error "  ✗ Failed to move $plugin_name to final location"
            rm -rf "$temp_dir" 2>/dev/null || true
            return 1
        fi
    fi

    # Clean up temporary directory if it still exists
    if [ -n "$temp_dir" ] && [ -d "$temp_dir" ]; then
        rm -rf "$temp_dir" 2>/dev/null || true
    fi

    return 0
}

# Main script
main() {
    echo "QGIS Plugin Installer"
    echo "=================================================="

    # Get repository directory (where this script is located)
    REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
    print_info "Repository: $REPO_DIR"

    # Get QGIS plugins directory
    QGIS_PLUGINS_DIR=$(get_qgis_plugins_dir)
    print_info "QGIS plugins directory: $QGIS_PLUGINS_DIR"

    # Create QGIS plugins directory if it doesn't exist
    if [ ! -d "$QGIS_PLUGINS_DIR" ]; then
        print_warning "Creating QGIS plugins directory: $QGIS_PLUGINS_DIR"
        mkdir -p "$QGIS_PLUGINS_DIR"
    fi

    # Check if plugins directory exists in repository
    if [ ! -d "$REPO_DIR/plugins" ]; then
        print_error "Error: Plugins directory not found: $REPO_DIR/plugins"
        exit 1
    fi

    # Find all plugin .zip files
    shopt -s nullglob
    PLUGIN_ZIPS=("$REPO_DIR/plugins"/*.zip)

    if [ ${#PLUGIN_ZIPS[@]} -eq 0 ]; then
        print_error "Error: No .zip files found in $REPO_DIR/plugins"
        exit 1
    fi

    echo ""
    print_info "Found ${#PLUGIN_ZIPS[@]} plugin(s) to install:"
    for zip_file in "${PLUGIN_ZIPS[@]}"; do
        echo "  - $(basename "$zip_file" .zip)"
    done

    echo ""
    print_info "Installing plugins..."
    echo "--------------------------------------------------"

    # Install each plugin
    installed=0
    failed=0

    for zip_file in "${PLUGIN_ZIPS[@]}"; do
        if install_plugin "$zip_file" "$QGIS_PLUGINS_DIR"; then
            installed=$((installed + 1))
        else
            failed=$((failed + 1))
        fi
    done

    echo "--------------------------------------------------"
    echo ""
    print_success "Installation complete!"
    print_success "  Successfully installed: $installed"

    if [ $failed -gt 0 ]; then
        print_warning "  Failed: $failed"
    fi

    echo ""
    print_info "Please restart QGIS and enable the plugins from:"
    print_info "  Plugins → Manage and Install Plugins → Installed"

    return $failed
}

# Check for required commands
if ! command -v unzip &> /dev/null; then
    print_error "Error: 'unzip' command not found. Please install it first."
    exit 1
fi

# Run main function
main
exit $?
