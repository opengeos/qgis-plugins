# QGIS Plugin Repository

A custom QGIS plugin repository for AI-powered geospatial analysis tools.

## Repository URL

```
https://qgis.gishub.org/plugins.xml
```

## How to Add This Repository to QGIS

1. Open QGIS
2. Go to **Plugins** → **Manage and Install Plugins**
3. Click the **Settings** tab
4. Click **Add...** under "Plugin Repositories"
5. Enter:
   - **Name:** `OpenGeos`
   - **URL:** `https://qgis.gishub.org/plugins.xml`
6. Click **OK**
7. Enable **Show also experimental plugins** in Settings

## Available Plugins

### AI & Machine Learning

#### GeoAI

AI-powered geospatial analysis plugin featuring:

- **Moondream Vision-Language Model**: Image captioning, natural language querying, object detection, and point localization
- **Semantic Segmentation**: Train and run custom segmentation models (U-Net, DeepLabV3+, FPN, etc.)
- **SamGeo**: Segment objects using text, point, or box prompts

📦 [Download](https://qgis.gishub.org/plugins/geoai.zip) | 🏠 [Homepage](https://opengeoai.org) | 🐛 [Issues](https://github.com/opengeos/geoai/issues)

#### SamGeo

Remote sensing image segmentation powered by Meta's Segment Anything Model (SAM):

- Text-based segmentation (describe what you want to segment)
- Interactive point prompts (click to segment objects)
- Box prompts (draw rectangles to segment regions)
- Export to vector layers or GeoTIFF rasters

📦 [Download](https://qgis.gishub.org/plugins/samgeo.zip) | 🏠 [Homepage](https://github.com/opengeos/qgis-samgeo-plugin) | 🐛 [Issues](https://github.com/opengeos/qgis-samgeo-plugin/issues)

#### Whitebox AI Agent

AI-powered agent for running WhiteboxTools through natural language:

- Chat-style interface for natural language queries
- Multiple LLM backends: Ollama, Claude, OpenAI, Gemini
- Automatic algorithm discovery and parameter validation
- Smart layer detection and output loading

📦 [Download](https://qgis.gishub.org/plugins/whitebox_agent.zip) | 🏠 [Homepage](https://github.com/opengeos/qgis-whitebox-agent) | 🐛 [Issues](https://github.com/opengeos/qgis-whitebox-agent/issues)

### Hyperspectral & Remote Sensing

#### HyperCoast

Hyperspectral data visualization and analysis plugin supporting:

- **Data Formats**: EMIT, PACE, DESIS, NEON, AVIRIS, PRISMA, EnMAP, Tanager, Wyvern
- **Tools**: Band combination, spectral signature inspection, PCA analysis, RGB composite creation

📦 [Download](https://qgis.gishub.org/plugins/hypercoast.zip) | 🏠 [Homepage](https://hypercoast.org) | 🐛 [Issues](https://github.com/opengeos/HyperCoast/issues)

### Satellite Data Access

#### Maxar Open Data

Browse and visualize Maxar Open Data satellite imagery for disaster events:

- Browse pre- and post-event high-resolution satellite imagery
- View and filter imagery footprints on the map
- Load Cloud Optimized GeoTIFFs (COG) directly
- Support for visual (RGB), multispectral, and panchromatic imagery

📦 [Download](https://qgis.gishub.org/plugins/maxar_open_data.zip) | 🏠 [Homepage](https://github.com/opengeos/qgis-maxar-plugin) | 🐛 [Issues](https://github.com/opengeos/qgis-maxar-plugin/issues)

#### NASA Earthdata

Search, visualize, and download NASA Earthdata products in QGIS:

- Search and browse NASA Earthdata catalog
- COG (Cloud Optimized GeoTIFF) visualization
- Data footprint display on map
- Direct integration with NASA Earthdata authentication

📦 [Download](https://qgis.gishub.org/plugins/nasa_earthdata.zip) | 🏠 [Homepage](https://github.com/opengeos/qgis-nasa-earthdata-plugin) | 🐛 [Issues](https://github.com/opengeos/qgis-nasa-earthdata-plugin/issues)

#### NASA OPERA

Search and visualize NASA OPERA satellite data products:

- **Datasets**: DSWX-HLS, DSWX-S1, DIST-ALERT-HLS, DIST-ANN-HLS, RTC-S1, CSLC-S1
- Search by location, date range, and dataset type
- Display footprints and visualize raster data
- Automatic NASA Earthdata authentication

📦 [Download](https://qgis.gishub.org/plugins/nasa_opera.zip) | 🏠 [Homepage](https://github.com/opengeos/qgis-nasa-opera-plugin) | 🐛 [Issues](https://github.com/opengeos/qgis-nasa-opera-plugin/issues)

### Google Earth Engine

#### Geemap

QGIS plugin that integrates geemap for working with Google Earth Engine data:

- Add Earth Engine Image and ImageCollection layers to QGIS
- Add Earth Engine FeatureCollection layers as vector data
- Use familiar geemap Map API within QGIS
- Interactive map controls for center, zoom, and bounds

📦 [Download](https://qgis.gishub.org/plugins/qgis_geemap.zip) | 🏠 [Homepage](https://github.com/opengeos/qgis-geemap-plugin) | 🐛 [Issues](https://github.com/opengeos/qgis-geemap-plugin/issues)

#### Timelapse

Create timelapse animations from satellite and aerial imagery using Google Earth Engine:

- **Data Sources**: NAIP, Landsat, Sentinel-2, Sentinel-1, GOES, MODIS NDVI
- Define area of interest by drawing or using vector layers
- Customizable output settings (dimensions, FPS, text overlays)
- GIF and MP4 output formats

📦 [Download](https://qgis.gishub.org/plugins/timelapse.zip) | 🏠 [Homepage](https://github.com/opengeos/qgis-timelapse-plugin) | 🐛 [Issues](https://github.com/opengeos/qgis-timelapse-plugin/issues)

### Visualization & Utilities

#### Leafmap

Interactive layer comparison with transparency control and swipe tools:

- Interactive layer transparency control with real-time preview
- Swipe tool for comparing two layers side-by-side
- Dockable panels positioned anywhere in the QGIS interface
- Plugin update checker

📦 [Download](https://qgis.gishub.org/plugins/qgis_leafmap.zip) | 🏠 [Homepage](https://github.com/opengeos/qgis-leafmap-plugin) | 🐛 [Issues](https://github.com/opengeos/qgis-leafmap-plugin/issues)

#### Notebook

Render and run Jupyter notebooks within QGIS:

- Open and render Jupyter notebook (.ipynb) files
- Execute notebook cells with Python kernel
- View markdown and code cell outputs
- Syntax highlighting for code cells
- Integration with QGIS Python environment

📦 [Download](https://qgis.gishub.org/plugins/qgis_notebook.zip) | 🏠 [Homepage](https://github.com/opengeos/qgis-notebook-plugin) | 🐛 [Issues](https://github.com/opengeos/qgis-notebook-plugin/issues)

### Development

#### Plugin Template

Template for creating QGIS plugins with best practices:

- Dockable panels that can be positioned anywhere
- Plugin update checker from GitHub
- About dialog with version information
- Clean, modular code structure

📦 [Download](https://qgis.gishub.org/plugins/plugin_template.zip) | 🏠 [Homepage](https://github.com/opengeos/qgis-plugin-template) | 🐛 [Issues](https://github.com/opengeos/qgis-plugin-template/issues)

## Requirements

- QGIS 3.28 or higher
- Python packages as specified in each plugin's requirements
- PyTorch with CUDA support recommended for optimal AI performance
- Google Earth Engine account for Geemap and Timelapse plugins
- NASA Earthdata account for NASA OPERA plugin

## License

MIT License
