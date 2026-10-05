import random
from dataclasses import dataclass

from geomarc.constants import COMPLEXITY_SETTINGS, STYLE_CHOICES
from geomarc.generator.styles import generate_styled_pattern_elements

from .geometry import Line, Point, Polygon


@dataclass(frozen=True)
class Pattern:
    width: int
    height: int
    points: tuple[Point, ...]
    lines: tuple[Line, ...]
    polygons: tuple[Polygon, ...]
    style: str = None


def generate_pattern(
    width: int,
    height: int,
    complexity: str = "medium",
    style: str | None = None,
    seed: int | None = None,
) -> Pattern:
    if complexity not in COMPLEXITY_SETTINGS:
        raise ValueError(
            f"Unknown complexity: {complexity}. "
            f"Choose: {', '.join(COMPLEXITY_SETTINGS)}"
        )

    settings = COMPLEXITY_SETTINGS[complexity]

    rng = random.Random(seed)

    
    if style is None:
        style = rng.choice(STYLE_CHOICES)
    elif style not in STYLE_CHOICES:
        raise ValueError(
            f"Unknown style: {style}. "
            f"Choose: {', '.join(STYLE_CHOICES)}"
        )

    points, lines, polygons = generate_styled_pattern_elements(
        width=width,
        height=height,
        style=style,
        base_points_count=settings["points"],
        base_extra_lines=settings["extra_lines"],
        base_polygons_count=settings["polygons"],
        rng=rng,
    )

    return Pattern(
        width=width,
        height=height,
        points=tuple(points),
        lines=tuple(lines),
        polygons=tuple(polygons),
    )
