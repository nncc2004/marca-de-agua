"""
scanner.py
Busca imágenes dentro de una carpeta.
"""

from pathlib import Path

from config import SUPPORTED_FORMATS


def scan_folder(folder: str | Path) -> list[Path]:
    """
    Retorna una lista de imágenes encontradas en la carpeta.
    """

    folder = Path(folder)

    if not folder.exists():
        raise FileNotFoundError(f"No existe la carpeta: {folder}")

    if not folder.is_dir():
        raise NotADirectoryError(folder)

    images = [
        file
        for file in folder.iterdir()
        if file.is_file() and file.suffix.lower() in SUPPORTED_FORMATS
    ]

    return sorted(images)