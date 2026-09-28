import random

from geomarc.constants import EDGE_MARGIN_RATIO

from .bounds import rotated_bounds


def generate_position(
    image_width: int,
    image_height: int,
    watermark_width: float,
    watermark_height: float,
    rotation: float,
    rng: random.Random,
) -> tuple[float, float]:
    bounding_width, bounding_height = rotated_bounds(
        watermark_width,
        watermark_height,
        rotation,
    )

    margin_x = image_width * EDGE_MARGIN_RATIO
    margin_y = image_height * EDGE_MARGIN_RATIO

    min_x = margin_x
    min_y = margin_y

    max_x = (
        image_width
        - bounding_width
        - margin_x
    )

    max_y = (
        image_height
        - bounding_height
        - margin_y
    )

    if max_x < min_x:
        x = image_width / 2 - bounding_width / 2
    else:
        x = rng.uniform(
            min_x,
            max_x,
        )

    if max_y < min_y:
        y = image_height / 2 - bounding_height / 2
    else:
        y = rng.uniform(
            min_y,
            max_y,
        )

    return x, y