from geomarc.constants import MIN_SPACING_RATIO

from .bounds import bounding_box, expanded_bounding_box
from .models import Placement


def is_valid_placement(
    candidate: Placement,
    existing: list[Placement],
    image_width: int,
    image_height: int,
) -> bool:
    spacing = min(image_width, image_height) * MIN_SPACING_RATIO

    candidate_box = expanded_bounding_box(candidate, spacing)

    for placement in existing:
        existing_box = bounding_box(placement) 

        if boxes_overlap(candidate_box, existing_box):
            return False

    return True

def boxes_overlap(
    first: tuple[float, float, float, float],
    second: tuple[float, float, float, float],
) -> bool:
    first_left, first_top, first_right, first_bottom = first
    second_left, second_top, second_right, second_bottom = second

    return not (
        first_right <= second_left
        or first_left >= second_right
        or first_bottom <= second_top
        or first_top >= second_bottom
    )