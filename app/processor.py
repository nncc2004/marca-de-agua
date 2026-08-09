"""
processor.py
Coordina el procesamiento completo de las imágenes.
"""

from pathlib import Path
from shutil import rmtree

from config import (
    OUTPUT_FOLDER_NAME,
    OVERWRITE_OUTPUT,
)
from app.watermark import apply_watermark


def process_images(
    image_paths: list[str | Path],
    output_folder: str | Path,
    progress_callback=None,
) -> Path:
    """
    Procesa una lista de imágenes.

    Parameters
    ----------
    image_paths : lista de rutas de imágenes.
    output_folder : carpeta donde guardar los resultados.
    progress_callback : callback(current, total)

    Returns
    -------
    Ruta de la carpeta generada.
    """

    if not image_paths:
        raise ValueError("No se seleccionaron imágenes.")

    image_paths = [Path(image) for image in image_paths]
    output_folder = Path(output_folder)

    watermarked_folder = output_folder / OUTPUT_FOLDER_NAME

    if watermarked_folder.exists():

        if OVERWRITE_OUTPUT:
            rmtree(watermarked_folder)
        else:
            raise FileExistsError(watermarked_folder)

    watermarked_folder.mkdir(parents=True)

    total = len(image_paths)

    for index, image_path in enumerate(image_paths, start=1):

        destination = watermarked_folder / image_path.name

        apply_watermark(
            input_path=image_path,
            output_path=destination,
        )

        if progress_callback:
            progress_callback(index, total)

    return watermarked_folder