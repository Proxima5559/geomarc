import random

from geomarc.constants import (
    MAX_DIMENSION_RATIO as DEFAULT_MAX_RATIO,
    MAX_SCALE as DEFAULT_MAX_SCALE,
    MIN_SCALE,
    SIZE_MODE_RATIO
)


def generate_size(
    image_width: int,
    image_height: int,
    rng: random.Random,
    max_scale: float = DEFAULT_MAX_SCALE, 
    max_dimension_ratio: float = DEFAULT_MAX_RATIO, 
) -> tuple[float, float]:
    min_dimension = min(
        image_width,
        image_height,
    )
    mode_scale = MIN_SCALE + (max_scale - MIN_SCALE) * SIZE_MODE_RATIO

    scale = rng.triangular(
        MIN_SCALE,
        max_scale,
        mode_scale
    )

    base_size = min_dimension * scale

    aspect_ratio = rng.uniform(
        0.75,
        1.25,
    )

    width = base_size
    height = base_size * aspect_ratio

    max_width = (
        image_width
        * max_dimension_ratio
    )

    max_height = (
        image_height
        * max_dimension_ratio
    )

    width = min(width, max_width)
    height = min(height, max_height)

    min_size = min_dimension * MIN_SCALE

    width = max(width, min_size)
    height = max(height, min_size)

    return width, height