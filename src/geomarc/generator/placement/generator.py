import math
import random

from geomarc.constants import (
    ATTEMPTS_MULTIPLIER,
    MAX_COUNT,
    MAX_ROTATION,
    MIN_COUNT,
    MIN_ROTATION,
)
from geomarc.constants.placement_con import (
    MAX_SCALE,
    MIN_SCALE,
)

from .bounds import bounding_box
from .collision import is_valid_placement
from .models import Placement
from .position import generate_position
from .protected import (
    ProtectedRegion,
    intersects_protected_region,
)
from .size import generate_size


def generate_placements(
    image_width: int,
    image_height: int,
    count: int = 5,
    seed: int | None = None,
    protected_regions: list[ProtectedRegion] | None = None,
) -> tuple[Placement, ...]:
    if image_width <= 0 or image_height <= 0:
        raise ValueError(
            "Image dimensions must be greater than 0"
        )

    if not MIN_COUNT <= count <= MAX_COUNT:
        raise ValueError(
            f"Count must be between "
            f"{MIN_COUNT} and {MAX_COUNT}"
        )

    if protected_regions is None:
        protected_regions = []

    _validate_protected_regions(
        protected_regions=protected_regions,
        image_width=image_width,
        image_height=image_height,
    )

    rng = random.Random(seed)

    placements: list[Placement] = []

    dynamic_max_scale = MAX_SCALE

    if count > 3:
        dynamic_max_scale = max(
            MIN_SCALE,
            MAX_SCALE / math.sqrt(count / 3.0),
        )

    max_attempts = (
        count
        * ATTEMPTS_MULTIPLIER
    )

    for _ in range(count):
        placement = _find_placement(
            image_width=image_width,
            image_height=image_height,
            existing=placements,
            protected_regions=protected_regions,
            rng=rng,
            max_attempts=max_attempts,
            max_scale_override=dynamic_max_scale,
        )

        placements.append(placement)

    return tuple(placements)


def _find_placement(
    image_width: int,
    image_height: int,
    existing: list[Placement],
    protected_regions: list[ProtectedRegion],
    rng: random.Random,
    max_attempts: int,
    max_scale_override: float,
) -> Placement:
    for _ in range(max_attempts):
        width, height = generate_size(
            image_width=image_width,
            image_height=image_height,
            rng=rng,
            max_scale=max_scale_override,
        )

        rotation = rng.uniform(
            MIN_ROTATION,
            MAX_ROTATION,
        )

        x, y = generate_position(
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

        if not is_valid_placement(
            candidate=candidate,
            existing=existing,
            image_width=image_width,
            image_height=image_height,
        ):
            continue

        candidate_box = bounding_box(candidate)

        if intersects_protected_region(
            placement_box=candidate_box,
            protected_regions=protected_regions,
        ):
            continue

        return candidate

    raise RuntimeError(
        f"Could not find valid placement "
        f"after {max_attempts} attempts"
    )


def _validate_protected_regions(
    protected_regions: list[ProtectedRegion],
    image_width: int,
    image_height: int,
) -> None:
    for region in protected_regions:
        if region.right > image_width:
            raise ValueError(
                "Protected region right edge "
                "cannot exceed image width"
            )

        if region.bottom > image_height:
            raise ValueError(
                "Protected region bottom edge "
                "cannot exceed image height"
            )