import math
import random
from dataclasses import dataclass
from typing import List, Tuple, Optional
from geomarc.constants import (
    MIN_COUNT,
    MAX_COUNT,
    MIN_SCALE,
    MAX_SCALE,
    MIN_ROTATION,
    MAX_ROTATION,
    MAX_DIMENSION_RATIO,
    ATTEMPTS_MULTIPLIER
)

@dataclass(frozen=True)
class Placement:
    """Represents a watermark placement with position, size, and rotation."""
    x: float
    y: float
    width: float
    height: float
    rotation: float


def generate_placements(
    image_width: int,
    image_height: int,
    count: int = 5,
    seed: Optional[int] = None,
) -> Tuple[Placement, ...]:
    """
    Generate non-overlapping watermark placements within an image.

    Args:
        image_width: Width of the container image in pixels.
        image_height: Height of the container image in pixels.
        count: Number of placements to generate (3-10).
        seed: Optional random seed for reproducibility.

    Returns:
        Tuple of Placement objects with x, y, width, height, and rotation.

    Raises:
        ValueError: If dimensions are invalid or count is out of range.
        RuntimeError: If valid placements cannot be found.
    """
    if image_width <= 0 or image_height <= 0:
        raise ValueError("Image dimensions must be greater than 0")

    if not MIN_COUNT <= count <= MAX_COUNT:
        raise ValueError(f"Count must be between {MIN_COUNT} and {MAX_COUNT}")

    rng = random.Random(seed)
    placements: List[Placement] = []
    max_attempts = count * ATTEMPTS_MULTIPLIER

    for _ in range(count):
        placement = _find_placement(
            image_width=image_width,
            image_height=image_height,
            existing=placements,
            rng=rng,
            max_attempts=max_attempts,
        )
        placements.append(placement)

    return tuple(placements)


def _find_placement(
    image_width: int,
    image_height: int,
    existing: List[Placement],
    rng: random.Random,
    max_attempts: int,
) -> Placement:
    """Find a valid placement that doesn't overlap with existing placements."""
    for _ in range(max_attempts):
        width, height = _generate_size(
            image_width=image_width,
            image_height=image_height,
            rng=rng,
        )

        rotation = rng.uniform(MIN_ROTATION, MAX_ROTATION)

        x, y = _generate_position(
            image_width=image_width,
            image_height=image_height,
            watermark_width=width,
            watermark_height=height,
            rotation=rotation,
            rng=rng,
        )

        candidate = Placement(
            x=x,
            y=y,
            width=width,
            height=height,
            rotation=rotation,
        )

        if _is_valid_placement(candidate=candidate, existing=existing):
            return candidate

    raise RuntimeError(
        f"Could not find valid placement after {max_attempts} attempts"
    )


def _generate_size(
    image_width: int,
    image_height: int,
    rng: random.Random,
) -> Tuple[float, float]:
    """Generate random watermark dimensions within acceptable bounds."""
    min_dimension = min(image_width, image_height)
    scale = rng.uniform(MIN_SCALE, MAX_SCALE)

    base_size = min_dimension * scale
    aspect_ratio = rng.uniform(0.7, 1.3)

    width = base_size
    height = base_size * aspect_ratio

    max_width = image_width * MAX_DIMENSION_RATIO
    max_height = image_height * MAX_DIMENSION_RATIO

    width = min(width, max_width)
    height = min(height, max_height)

    min_size = min_dimension * 0.05
    width = max(width, min_size)
    height = max(height, min_size)

    return width, height


def _generate_position(
    image_width: int,
    image_height: int,
    watermark_width: float,
    watermark_height: float,
    rotation: float,
    rng: random.Random,
) -> Tuple[float, float]:
    bounding_width, bounding_height = _rotated_bounds(
        watermark_width,
        watermark_height,
        rotation,
    )

    available_width = max(0, image_width - bounding_width)
    available_height = max(0, image_height - bounding_height)

    x = rng.uniform(0, available_width)
    y = rng.uniform(0, available_height)

    return x, y


def _rotated_bounds(
    width: float,
    height: float,
    rotation: float,
) -> Tuple[float, float]:
    radians = math.radians(rotation)
    cos_value = abs(math.cos(radians))
    sin_value = abs(math.sin(radians))

    bounding_width = width * cos_value + height * sin_value
    bounding_height = width * sin_value + height * cos_value

    return bounding_width, bounding_height


def _is_valid_placement(
    candidate: Placement,
    existing: List[Placement],
) -> bool:
    candidate_box = _bounding_box(candidate)

    for placement in existing:
        existing_box = _bounding_box(placement)

        if _boxes_overlap(candidate_box, existing_box):
            return False

    return True


def _bounding_box(
    placement: Placement,
) -> Tuple[float, float, float, float]:
    width, height = _rotated_bounds(
        placement.width,
        placement.height,
        placement.rotation,
    )

    left = placement.x
    top = placement.y
    right = left + width
    bottom = top + height

    return left, top, right, bottom


def _boxes_overlap(
    first: Tuple[float, float, float, float],
    second: Tuple[float, float, float, float],
) -> bool:
    first_left, first_top, first_right, first_bottom = first
    second_left, second_top, second_right, second_bottom = second

    return not (
        first_right <= second_left
        or first_left >= second_right
        or first_bottom <= second_top
        or first_top >= second_bottom
    )