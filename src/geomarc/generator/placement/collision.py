import math
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
    candidate_obb = None

    for placement in existing:
        existing_box = expanded_bounding_box(placement, spacing)
        
        if boxes_overlap(candidate_box, existing_box):
            if candidate_obb is None:
                candidate_obb = _get_obb_vertices(candidate, spacing)
            
            existing_obb = _get_obb_vertices(placement, spacing)
            
            if _obb_overlap(candidate_obb, existing_obb):
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

def _get_obb_vertices(placement: Placement, spacing: float) -> list[tuple[float, float]]:
    angle = placement.rotation
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    
    half_w = placement.width / 2 + spacing
    half_h = placement.height / 2 + spacing
    
    dir_x_x = half_w * cos_a
    dir_x_y = half_w * sin_a
    dir_y_x = -half_h * sin_a
    dir_y_y = half_h * cos_a
    
    cx, cy = placement.x, placement.y
    
    return [
        (cx - dir_x_x - dir_y_x, cy - dir_x_y - dir_y_y),
        (cx + dir_x_x - dir_y_x, cy + dir_x_y - dir_y_y),
        (cx + dir_x_x + dir_y_x, cy + dir_x_y + dir_y_y),
        (cx - dir_x_x + dir_y_x, cy - dir_x_y + dir_y_y)
    ]

def _obb_overlap(poly1: list[tuple[float, float]], poly2: list[tuple[float, float]]) -> bool:
    axes = [
        (poly1[1][0] - poly1[0][0], poly1[1][1] - poly1[0][1]),
        (poly1[3][0] - poly1[0][0], poly1[3][1] - poly1[0][1]),
        (poly2[1][0] - poly2[0][0], poly2[1][1] - poly2[0][1]),
        (poly2[3][0] - poly2[0][0], poly2[3][1] - poly2[0][1])
    ]
    
    for ax, ay in axes:
        proj1 = [p[0] * ax + p[1] * ay for p in poly1]
        min1, max1 = min(proj1), max(proj1)
        
        proj2 = [p[0] * ax + p[1] * ay for p in poly2]
        min2, max2 = min(proj2), max(proj2)
        
        if max1 < min2 or max2 < min1:
            return False
            
    return True