"""
config.py
Configuración global de la aplicación.
Todos estos valores son internos y no son modificables por el usuario.
"""

from pathlib import Path

# ==========================
# Recursos
# ==========================

ASSETS_FOLDER = Path("assets")

WATERMARK_FILENAME = "watermark.png"
ICON_FILENAME = "icon.ico"

# ==========================
# Carpeta de salida
# ==========================

OUTPUT_FOLDER_NAME = "Watermarked"

# ==========================
# Formatos soportados
# ==========================

SUPPORTED_FORMATS = (
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".bmp",
    ".tif",
    ".tiff",
)

# ==========================
# Configuración de la marca
# ==========================

# Tamaño de la marca respecto al ancho de la imagen
# 0.18 = 18%
WATERMARK_SCALE = 0.5

# Opacidad (0.0 a 1.0)
WATERMARK_OPACITY = 0.70

# Margen respecto a los bordes (px)
WATERMARK_MARGIN = 30

# Posición fija
WATERMARK_POSITION = "bottom_right"

# ==========================
# Procesamiento
# ==========================

# Calidad de salida para JPG
JPEG_QUALITY = 95

# Sobrescribir si existe una carpeta/zip previo
OVERWRITE_OUTPUT = True