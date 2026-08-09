"""
watermark.py
Aplica la marca de agua a una imagen.
"""

from pathlib import Path

from PIL import Image

from config import (
    JPEG_QUALITY,
    WATERMARK_MARGIN,
    WATERMARK_OPACITY,
    WATERMARK_SCALE,
)
from app.resources import get_watermark_path


def apply_watermark(input_path: Path, output_path: Path) -> None:
    """
    Aplica la marca de agua a una imagen y la guarda.
    """

    image = Image.open(input_path).convert("RGBA")
    watermark = Image.open(get_watermark_path()).convert("RGBA")

    # Escalar marca
    new_width = int(image.width * WATERMARK_SCALE)
    ratio = new_width / watermark.width
    new_height = int(watermark.height * ratio)

    watermark = watermark.resize(
        (new_width, new_height),
        Image.Resampling.LANCZOS,
    )

    # Aplicar opacidad
    alpha = watermark.getchannel("A")
    alpha = alpha.point(lambda p: int(p * WATERMARK_OPACITY))
    watermark.putalpha(alpha)

    # Posición (centrada)
    x = (image.width - watermark.width) // 2
    y = (image.height - watermark.height) // 2

    # Composición
    result = image.copy()
    result.alpha_composite(watermark, (x, y))

    # Guardar
    if output_path.suffix.lower() in (".jpg", ".jpeg"):
        result.convert("RGB").save(
            output_path,
            quality=JPEG_QUALITY,
        )
    else:
        result.save(output_path)
