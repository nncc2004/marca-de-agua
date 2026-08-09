"""
resources.py
Gestiona el acceso a los recursos de la aplicación.
Compatible tanto al ejecutar desde Python como desde un .exe generado con
PyInstaller.
"""

import sys
from pathlib import Path

from config import (
    ASSETS_FOLDER,
    WATERMARK_FILENAME,
    ICON_FILENAME,
)


def get_base_path() -> Path:
    """
    Retorna la carpeta base de la aplicación.
    """
    if getattr(sys, "_MEIPASS", None):
        return Path(sys._MEIPASS)

    return Path(__file__).resolve().parent.parent


def get_asset_path(filename: str) -> Path:
    """
    Retorna la ruta absoluta de un recurso dentro de assets/.
    """
    return get_base_path() / ASSETS_FOLDER / filename


def get_watermark_path() -> Path:
    """
    Retorna la ruta de la marca de agua.
    """
    return get_asset_path(WATERMARK_FILENAME)


def get_icon_path() -> Path:
    """
    Retorna la ruta del ícono de la aplicación.
    """
    return get_asset_path(ICON_FILENAME)