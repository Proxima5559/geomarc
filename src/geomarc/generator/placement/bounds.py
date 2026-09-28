import math

from .models import Placement


def rotated_bounds(
    width: float,
    height: float,
    rotation: float,
) -> tuple[float, float]:
    radians = math.radians(rotation)

    cos_value = abs(math.cos(radians))
    sin_value = abs(math.sin(radians))

    bounding_width = (
        width * cos_value
        + height * sin_value
    )

    bounding_height = (
        width * sin_value
        + height * cos_value
    )

    return bounding_width, bounding_height


def bounding_box(
    placement: Placement,
) -> tuple[float, float, float, float]:
    width, height = rotated_bounds(
        placement.width,
        placement.height,
        placement.rotation,
    )

    left = placement.x
    top = placement.y
    right = left + width
    bottom = top + height

    return left, top, right, bottom


def expanded_bounding_box(
    placement: Placement,
    spacing: float,
) -> tuple[float, float, float, float]:
    left, top, right, bottom = bounding_box(placement)

    return (
        left - spacing,
        top - spacing,
        right + spacing,
        bottom + spacing,
    )