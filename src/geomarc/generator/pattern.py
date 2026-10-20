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
    custom_points: int | None = None,
    custom_extra_lines: int | None = None,
    custom_polygons: int | None = None,
) -> Pattern:

    custom_pattern_enabled = any(
        value is not None
        for value in (
            custom_points,
            custom_extra_lines,
            custom_polygons,
        )
    )
     
    if not custom_pattern_enabled:
        if complexity not in COMPLEXITY_SETTINGS:
            raise ValueError(
                f"Unknown complexity: {complexity}. "
                f"Choose: {', '.join(COMPLEXITY_SETTINGS)}"
            )

        settings = COMPLEXITY_SETTINGS[complexity]
        exact_counts = False  # ДОБАВЛЕНО: обычные complexity работают по-старому.
    else:
        settings = {
            "points": custom_points or 0,
            "extra_lines": custom_extra_lines or 0,
            "polygons": custom_polygons or 0,
        }
        exact_counts = True  

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
        exact_counts=exact_counts,
    )

    return Pattern(
        width=width,
        height=height,
        points=tuple(points),
        lines=tuple(lines),
        polygons=tuple(polygons),
    )
