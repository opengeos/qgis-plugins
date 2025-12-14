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
   - **Name:** `GeoAI Plugins`
   - **URL:** `https://qgis.gishub.org/plugins.xml`
6. Click **OK**
7. Enable **Show also experimental plugins** in Settings

## Available Plugins

### GeoAI

AI-powered geospatial analysis plugin featuring:

- **Moondream Vision-Language Model**: Image captioning, natural language querying, object detection, and point localization
- **Semantic Segmentation**: Train and run custom segmentation models (U-Net, DeepLabV3+, FPN, etc.)
- **SamGeo**: Segment objects using text, point, or box prompts

📦 [Download](https://qgis.gishub.org/geoai.zip) | 🏠 [Homepage](https://opengeoai.org) | 🐛 [Issues](https://github.com/opengeos/geoai/issues)

### HyperCoast

Hyperspectral data visualization and analysis plugin supporting:

- **Data Formats**: EMIT, PACE, DESIS, NEON, AVIRIS, PRISMA, EnMAP, Tanager, Wyvern
- **Tools**: Band combination, spectral signature inspection, PCA analysis, RGB composite creation

📦 [Download](https://qgis.gishub.org/hypercoast.zip) | 🏠 [Homepage](https://hypercoast.org) | 🐛 [Issues](https://github.com/opengeos/HyperCoast/issues)

### SamGeo

Remote sensing image segmentation powered by Meta's Segment Anything Model (SAM):

- Text-based segmentation
- Interactive point prompts
- Box prompts for region selection
- Export to vector layers or GeoTIFF

📦 [Download](https://qgis.gishub.org/samgeo.zip) | 🏠 [Homepage](https://github.com/opengeos/qgis-samgeo-plugin) | 🐛 [Issues](https://github.com/opengeos/qgis-samgeo-plugin/issues)

## Requirements

- QGIS 3.22 or higher (3.28+ recommended for GeoAI)
- Python packages as specified in each plugin's requirements
- PyTorch with CUDA support recommended for optimal AI performance

## License

MIT License
