#!/usr/bin/env python3
"""Generate a beautiful HTML homepage for the QGIS plugin repository."""

import os
import configparser
from zipfile import ZipFile
from datetime import datetime
import shutil


PLUGINS_DIR = "plugins"
ICONS_DIR = "icons"


def extract_plugin_icon(
    zip_path: str, plugin_name: str, metadata_icon_path: str = None
) -> str:
    """Extract the plugin icon from the zip file and save it to the icons directory.

    Args:
        zip_path: Path to the plugin zip file
        plugin_name: Name of the plugin
        metadata_icon_path: Icon path specified in metadata.txt (optional)
    """
    # Create icons directory if it doesn't exist
    os.makedirs(ICONS_DIR, exist_ok=True)

    try:
        with ZipFile(zip_path, "r") as zf:
            # Priority 1: Try the icon path from metadata.txt first
            if metadata_icon_path:
                # The metadata icon path might be relative to the plugin directory
                metadata_icon_candidates = [
                    f"{plugin_name}/{metadata_icon_path}",  # Relative to plugin dir
                    metadata_icon_path,  # Absolute path in zip
                ]

                for icon_path in metadata_icon_candidates:
                    if icon_path in zf.namelist():
                        # Determine extension from the file
                        extension = os.path.splitext(icon_path)[1]
                        if not extension:
                            extension = ".png"  # Default to PNG if no extension

                        icon_filename = f"{plugin_name}{extension}"
                        output_path = os.path.join(ICONS_DIR, icon_filename)

                        with zf.open(icon_path) as icon_file:
                            with open(output_path, "wb") as out_file:
                                out_file.write(icon_file.read())

                        print(
                            f"✓ Extracted icon for {plugin_name} from metadata path: {icon_path}"
                        )
                        return f"{ICONS_DIR}/{icon_filename}"

            # Priority 2: Find the icon file using standard locations
            # Priority order: icon.png/svg, then plugin_name.png/svg
            icon_candidates = [
                (f"{plugin_name}/icons/icon.png", ".png"),
                (f"{plugin_name}/icon.png", ".png"),
                (f"{plugin_name}/icons/{plugin_name}.png", ".png"),
                (f"{plugin_name}/icons/icon.svg", ".svg"),
                (f"{plugin_name}/icon.svg", ".svg"),
                (f"{plugin_name}/icons/{plugin_name}.svg", ".svg"),
            ]

            for icon_path, extension in icon_candidates:
                if icon_path in zf.namelist():
                    # Extract icon to icons directory
                    icon_filename = f"{plugin_name}{extension}"
                    output_path = os.path.join(ICONS_DIR, icon_filename)

                    with zf.open(icon_path) as icon_file:
                        with open(output_path, "wb") as out_file:
                            out_file.write(icon_file.read())

                    print(f"✓ Extracted icon for {plugin_name}")
                    return f"{ICONS_DIR}/{icon_filename}"

            # If no standard icon found, look for plugin-specific named icons
            # For example: opera.svg for nasa_opera plugin
            plugin_base_name = plugin_name.replace("_", "").replace("-", "")
            for name in zf.namelist():
                if name.endswith("icon.png") or name.endswith("/icon.png"):
                    icon_filename = f"{plugin_name}.png"
                    output_path = os.path.join(ICONS_DIR, icon_filename)

                    with zf.open(name) as icon_file:
                        with open(output_path, "wb") as out_file:
                            out_file.write(icon_file.read())

                    print(f"✓ Extracted icon for {plugin_name}")
                    return f"{ICONS_DIR}/{icon_filename}"
                elif name.endswith("icon.svg") or name.endswith("/icon.svg"):
                    icon_filename = f"{plugin_name}.svg"
                    output_path = os.path.join(ICONS_DIR, icon_filename)

                    with zf.open(name) as icon_file:
                        with open(output_path, "wb") as out_file:
                            out_file.write(icon_file.read())

                    print(f"✓ Extracted icon for {plugin_name}")
                    return f"{ICONS_DIR}/{icon_filename}"
                # Look for any SVG/PNG file in icons directory that might be the main icon
                elif "/icons/" in name and (
                    name.endswith(".svg") or name.endswith(".png")
                ):
                    # Skip common non-icon files
                    if any(
                        skip in name.lower() for skip in ["about", "settings", "logo"]
                    ):
                        continue
                    # Extract the first viable icon we find
                    extension = ".svg" if name.endswith(".svg") else ".png"
                    icon_filename = f"{plugin_name}{extension}"
                    output_path = os.path.join(ICONS_DIR, icon_filename)

                    with zf.open(name) as icon_file:
                        with open(output_path, "wb") as out_file:
                            out_file.write(icon_file.read())

                    print(f"✓ Extracted icon for {plugin_name} from {name}")
                    return f"{ICONS_DIR}/{icon_filename}"

    except Exception as e:
        print(f"⚠ Could not extract icon for {plugin_name}: {e}")

    return None


def parse_metadata(zip_path: str) -> dict:
    """Extract metadata from a QGIS plugin zip file."""
    metadata = {}
    try:
        with ZipFile(zip_path, "r") as zf:
            # Find metadata.txt in the zip
            for name in zf.namelist():
                if name.endswith("metadata.txt"):
                    # Get the modification time of metadata.txt from the zip
                    info = zf.getinfo(name)
                    # date_time is a tuple: (year, month, day, hour, minute, second)
                    metadata_date = datetime(*info.date_time)

                    with zf.open(name) as f:
                        content = f.read().decode("utf-8")
                        config = configparser.ConfigParser()
                        config.read_string(content)
                        if "general" in config:
                            metadata = dict(config["general"])
                            # Store the metadata.txt modification date
                            metadata["_metadata_date"] = metadata_date
                    break
    except Exception as e:
        print(f"Error reading {zip_path}: {e}")
    return metadata


def get_file_size(path: str) -> str:
    """Get human-readable file size."""
    size = os.path.getsize(path)
    for unit in ["B", "KB", "MB", "GB"]:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"


def generate_index_html(output_file: str = "index.html"):
    """Generate a modern HTML homepage for the plugin repository."""

    # Find all plugin zip files in the plugins directory
    plugins = []
    plugins_path = PLUGINS_DIR
    if os.path.isdir(plugins_path):
        for filename in sorted(os.listdir(plugins_path)):
            if filename.endswith(".zip"):
                zip_path = os.path.join(plugins_path, filename)
                metadata = parse_metadata(zip_path)
                if metadata:
                    # Get plugin name from filename (remove .zip extension)
                    plugin_name = filename.replace(".zip", "")

                    # Extract plugin icon using the path from metadata.txt if available
                    metadata_icon = metadata.get("icon", None)
                    icon_path = extract_plugin_icon(
                        zip_path, plugin_name, metadata_icon
                    )
                    metadata["icon_path"] = icon_path

                    # Store relative path from root for download links
                    metadata["filename"] = f"{PLUGINS_DIR}/{filename}"
                    metadata["filesize"] = get_file_size(zip_path)
                    # Use the metadata.txt modification date from inside the zip
                    if "_metadata_date" in metadata:
                        metadata["modified"] = metadata["_metadata_date"].strftime(
                            "%Y-%m-%d"
                        )
                    else:
                        # Fallback to zip file modification time
                        metadata["modified"] = datetime.fromtimestamp(
                            os.path.getmtime(zip_path)
                        ).strftime("%Y-%m-%d")
                    plugins.append(metadata)

    # Sort plugins alphabetically by name (case-insensitive)
    plugins.sort(key=lambda p: p.get("name", "").lower())

    # Generate plugin cards HTML
    plugin_cards = ""
    for p in plugins:
        name = p.get("name", p["filename"])
        version = p.get("version", "Unknown")
        description = p.get("description", "No description available.")
        author = p.get("author", "Unknown")
        homepage = p.get("homepage", "#")
        tracker = p.get("tracker", "#")
        repository = p.get("repository", "#")
        qgis_min = p.get("qgisminimumversion", "3.0")
        experimental = p.get("experimental", "False").lower() == "true"
        tags = p.get("tags", "")
        category = p.get("category", "Plugins")

        # Create tag badges
        tag_badges = ""
        if tags:
            for tag in tags.split(",")[:5]:  # Limit to 5 tags
                tag = tag.strip()
                if tag:
                    tag_badges += f'<span class="tag">{tag}</span>'

        experimental_badge = (
            '<span class="badge experimental">Experimental</span>'
            if experimental
            else ""
        )

        # Generate icon HTML if available
        icon_html = ""
        if p.get("icon_path"):
            icon_html = (
                f'<img src="{p["icon_path"]}" alt="{name} icon" class="plugin-icon">'
            )

        plugin_cards += f"""
        <div class="plugin-card">
            <div class="plugin-header">
                <div class="plugin-title-row">
                    {icon_html}
                    <h2>{name}</h2>
                </div>
                <div class="badges">
                    <span class="badge version">v{version}</span>
                    <span class="badge category">{category}</span>
                    {experimental_badge}
                </div>
            </div>
            <p class="description">{description}</p>
            <div class="tags">{tag_badges}</div>
            <div class="meta">
                <span>👤 {author}</span>
                <span>📦 {p['filesize']}</span>
                <span>🔧 QGIS {qgis_min}+</span>
                <span>📅 {p['modified']}</span>
            </div>
            <div class="actions">
                <a href="{p['filename']}" class="btn btn-primary">⬇️ Download</a>
                <a href="{homepage}" class="btn btn-secondary" target="_blank">🏠 Homepage</a>
                <a href="{repository}" class="btn btn-secondary" target="_blank">📂 Repository</a>
                <a href="{tracker}" class="btn btn-secondary" target="_blank">🐛 Issues</a>
            </div>
        </div>
        """

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QGIS Plugin Repository | GeoAI Tools</title>
    <link rel="icon" type="image/png" href="logo.png">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-primary: #0f1419;
            --bg-secondary: #1a1f26;
            --bg-card: #1e252e;
            --bg-hover: #252d38;
            --text-primary: #e7eaed;
            --text-secondary: #8b949e;
            --accent-primary: #58a6ff;
            --accent-secondary: #3fb950;
            --accent-warning: #d29922;
            --accent-purple: #a371f7;
            --border-color: #30363d;
            --shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
            min-height: 100vh;
        }}

        /* Geometric background pattern */
        body::before {{
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background:
                radial-gradient(ellipse at 20% 20%, rgba(88, 166, 255, 0.08) 0%, transparent 50%),
                radial-gradient(ellipse at 80% 80%, rgba(163, 113, 247, 0.06) 0%, transparent 50%),
                radial-gradient(ellipse at 50% 50%, rgba(63, 185, 80, 0.04) 0%, transparent 60%);
            pointer-events: none;
            z-index: -1;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }}

        header {{
            text-align: center;
            padding: 4rem 2rem;
            background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-primary) 100%);
            border-bottom: 1px solid var(--border-color);
            position: relative;
            overflow: hidden;
        }}

        header::after {{
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 1px;
            background: linear-gradient(90deg, transparent, var(--accent-primary), transparent);
        }}

        .logo {{
            width: 120px;
            height: 120px;
            margin: 0 auto 1rem;
            display: block;
        }}

        h1 {{
            font-size: 2.5rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            background: linear-gradient(135deg, var(--text-primary) 0%, var(--accent-primary) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}

        .subtitle {{
            color: var(--text-secondary);
            font-size: 1.1rem;
            max-width: 600px;
            margin: 0 auto 2rem;
        }}

        .repo-url {{
            display: inline-flex;
            align-items: center;
            gap: 0.75rem;
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1rem 1.5rem;
            font-family: 'JetBrains Mono', monospace;
            font-size: 0.95rem;
            color: var(--accent-primary);
            transition: all 0.3s ease;
        }}

        .repo-url:hover {{
            border-color: var(--accent-primary);
            box-shadow: 0 0 20px rgba(88, 166, 255, 0.15);
        }}

        .copy-btn {{
            background: var(--accent-primary);
            color: var(--bg-primary);
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 6px;
            cursor: pointer;
            font-weight: 600;
            font-size: 0.85rem;
            transition: all 0.2s ease;
        }}

        .copy-btn:hover {{
            transform: scale(1.05);
            box-shadow: 0 4px 12px rgba(88, 166, 255, 0.3);
        }}

        .instructions {{
            margin-top: 2rem;
            padding: 1.5rem;
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            max-width: 600px;
            margin-left: auto;
            margin-right: auto;
            text-align: left;
        }}

        .instructions h3 {{
            color: var(--accent-secondary);
            margin-bottom: 1rem;
            font-size: 1rem;
        }}

        .instructions ol {{
            color: var(--text-secondary);
            padding-left: 1.5rem;
            font-size: 0.9rem;
        }}

        .instructions li {{
            margin-bottom: 0.5rem;
        }}

        .plugins-section {{
            padding: 3rem 0;
        }}

        .section-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 2rem;
            flex-wrap: wrap;
            gap: 1rem;
        }}

        .section-header h2 {{
            font-size: 1.75rem;
            font-weight: 600;
        }}

        .plugin-count {{
            color: var(--text-secondary);
            font-size: 0.9rem;
        }}

        .plugins-grid {{
            display: grid;
            gap: 1.5rem;
        }}

        .plugin-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 1.75rem;
            transition: all 0.3s ease;
        }}

        .plugin-card:hover {{
            border-color: var(--accent-primary);
            transform: translateY(-2px);
            box-shadow: var(--shadow);
        }}

        .plugin-header {{
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            margin-bottom: 1rem;
            flex-wrap: wrap;
            gap: 0.75rem;
        }}

        .plugin-title-row {{
            display: flex;
            align-items: center;
            gap: 1rem;
        }}

        .plugin-icon {{
            width: 48px;
            height: 48px;
            object-fit: contain;
            border-radius: 8px;
            background: var(--bg-hover);
            padding: 4px;
        }}

        .plugin-header h2 {{
            font-size: 1.5rem;
            font-weight: 600;
            color: var(--text-primary);
        }}

        .badges {{
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
        }}

        .badge {{
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .badge.version {{
            background: rgba(88, 166, 255, 0.15);
            color: var(--accent-primary);
        }}

        .badge.category {{
            background: rgba(163, 113, 247, 0.15);
            color: var(--accent-purple);
        }}

        .badge.experimental {{
            background: rgba(210, 153, 34, 0.15);
            color: var(--accent-warning);
        }}

        .description {{
            color: var(--text-secondary);
            margin-bottom: 1rem;
            line-height: 1.7;
        }}

        .tags {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-bottom: 1rem;
        }}

        .tag {{
            background: var(--bg-hover);
            color: var(--text-secondary);
            padding: 0.25rem 0.6rem;
            border-radius: 6px;
            font-size: 0.8rem;
        }}

        .meta {{
            display: flex;
            flex-wrap: wrap;
            gap: 1.5rem;
            margin-bottom: 1.25rem;
            color: var(--text-secondary);
            font-size: 0.9rem;
        }}

        .actions {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.75rem;
        }}

        .btn {{
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.65rem 1.25rem;
            border-radius: 8px;
            font-size: 0.9rem;
            font-weight: 500;
            text-decoration: none;
            transition: all 0.2s ease;
        }}

        .btn-primary {{
            background: var(--accent-primary);
            color: var(--bg-primary);
        }}

        .btn-primary:hover {{
            box-shadow: 0 4px 16px rgba(88, 166, 255, 0.35);
            transform: translateY(-1px);
        }}

        .btn-secondary {{
            background: var(--bg-hover);
            color: var(--text-primary);
            border: 1px solid var(--border-color);
        }}

        .btn-secondary:hover {{
            border-color: var(--text-secondary);
            background: var(--bg-secondary);
        }}

        footer {{
            text-align: center;
            padding: 2rem;
            border-top: 1px solid var(--border-color);
            color: var(--text-secondary);
            font-size: 0.9rem;
        }}

        footer a {{
            color: var(--accent-primary);
            text-decoration: none;
        }}

        footer a:hover {{
            text-decoration: underline;
        }}

        @media (max-width: 768px) {{
            .container {{
                padding: 1rem;
            }}

            header {{
                padding: 2rem 1rem;
            }}

            h1 {{
                font-size: 1.75rem;
            }}

            .repo-url {{
                flex-direction: column;
                text-align: center;
                font-size: 0.85rem;
            }}

            .plugin-header {{
                flex-direction: column;
            }}

            .meta {{
                gap: 1rem;
            }}

            .actions {{
                flex-direction: column;
            }}

            .btn {{
                justify-content: center;
            }}
        }}
    </style>
</head>
<body>
    <header>
        <img src="logo.png" alt="QGIS Plugin Repository Logo" class="logo">
        <h1>QGIS Plugin Repository</h1>
        <p class="subtitle">AI-powered geospatial analysis tools for QGIS. Deep learning, hyperspectral analysis, and advanced segmentation.</p>
        <div class="repo-url">
            <span>https://qgis.gishub.org/plugins.xml</span>
            <button class="copy-btn" onclick="copyUrl()">Copy URL</button>
        </div>
        <div class="instructions">
            <h3>📋 How to Add This Repository</h3>
            <ol>
                <li>Open QGIS → <strong>Plugins</strong> → <strong>Manage and Install Plugins</strong></li>
                <li>Go to the <strong>Settings</strong> tab</li>
                <li>Click <strong>Add...</strong> under "Plugin Repositories"</li>
                <li>Paste the URL above and click OK</li>
                <li>Enable <strong>"Show also experimental plugins"</strong></li>
            </ol>
        </div>
    </header>

    <main class="container">
        <section class="plugins-section">
            <div class="section-header">
                <h2>📦 Available Plugins</h2>
                <span class="plugin-count">{len(plugins)} plugins available</span>
            </div>
            <div class="plugins-grid">
                {plugin_cards}
            </div>
        </section>
    </main>

    <footer>
        <p>
            Made with ❤️ by <a href="https://github.com/giswqs" target="_blank">Qiusheng Wu</a> |
            <a href="https://github.com/opengeos/qgis-plugins" target="_blank">Open Geospatial Solutions</a>
        </p>
    </footer>

    <script>
        function copyUrl() {{
            navigator.clipboard.writeText('https://qgis.gishub.org/plugins.xml');
            const btn = document.querySelector('.copy-btn');
            const originalText = btn.textContent;
            btn.textContent = 'Copied!';
            btn.style.background = '#3fb950';
            setTimeout(() => {{
                btn.textContent = originalText;
                btn.style.background = '';
            }}, 2000);
        }}
    </script>
</body>
</html>
"""

    with open(output_file, "w") as f:
        f.write(html_content)

    print(f"✅ Generated {output_file} with {len(plugins)} plugins")


def generate_plugins_xml(output_file: str = "plugins.xml"):
    """Generate plugins.xml for QGIS plugin repository."""

    # Find all plugin zip files in the plugins directory
    plugins_path = PLUGINS_DIR
    plugins_data = []

    if os.path.isdir(plugins_path):
        for filename in sorted(os.listdir(plugins_path)):
            if filename.endswith(".zip"):
                zip_path = os.path.join(plugins_path, filename)
                metadata = parse_metadata(zip_path)
                if metadata:
                    metadata["zip_filename"] = (
                        filename  # Just the filename for file_name tag
                    )
                    metadata["zip_path"] = (
                        f"{PLUGINS_DIR}/{filename}"  # Full path for download_url
                    )
                    plugins_data.append(metadata)

    # Sort plugins alphabetically by name (case-insensitive)
    plugins_data.sort(key=lambda p: p.get("name", "").lower())

    # Generate XML content
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n<plugins>\n'

    for p in plugins_data:
        name = p.get("name", "Unknown")
        version = p.get("version", "0.0.1")
        description = p.get("description", "No description available.")
        about = (
            p.get("about", description)
            .replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )
        qgis_min = p.get("qgisminimumversion", "3.22")
        homepage = p.get("homepage", "")
        author = p.get("author", "Unknown")
        tracker = p.get("tracker", "")
        repository = p.get("repository", "")
        experimental = p.get("experimental", "False")
        deprecated = p.get("deprecated", "False")
        tags = p.get("tags", "")
        category = p.get("category", "Plugins")
        icon = p.get("icon", "icons/icon.png")
        zip_filename = p["zip_filename"]  # Just the filename
        zip_path = p["zip_path"]  # Full path for download URL
        download_url = f"https://qgis.gishub.org/{zip_path}"

        xml_content += f"""    <pyqgis_plugin name="{name}" version="{version}">
        <description>{description}</description>
        <about>{about}</about>
        <version>{version}</version>
        <qgis_minimum_version>{qgis_min}</qgis_minimum_version>
        <homepage>{homepage}</homepage>
        <file_name>{zip_filename}</file_name>
        <icon>{icon}</icon>
        <author_name>{author}</author_name>
        <download_url>{download_url}</download_url>
        <uploaded_by>giswqs</uploaded_by>
        <experimental>{experimental}</experimental>
        <deprecated>{deprecated}</deprecated>
        <tracker>{tracker}</tracker>
        <repository>{repository}</repository>
        <tags>{tags}</tags>
        <category>{category}</category>
    </pyqgis_plugin>

"""

    xml_content += "</plugins>\n"

    with open(output_file, "w") as f:
        f.write(xml_content)

    print(f"✅ Generated {output_file} with {len(plugins_data)} plugins")


if __name__ == "__main__":
    generate_plugins_xml()
    generate_index_html()
