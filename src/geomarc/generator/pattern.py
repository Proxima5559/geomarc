import random
from dataclasses import dataclass

from geomarc.constants import COMPLEXITY_SETTINGS

from .geometry import Line, Point, Polygon


@dataclass(frozen=True)
class Pattern:
    width: int
    height: int
    points: tuple[Point, ...]
    lines: tuple[Line, ...]
    polygons: tuple[Polygon, ...]


def generate_pattern(
    width: int,
    height: int,
    complexity: str = "medium",
    seed: int | None = None,
) -> Pattern:
    if complexity not in COMPLEXITY_SETTINGS:
        raise ValueError(
            f"Unknown complexity: {complexity}. "
            f"Choose: {', '.join(COMPLEXITY_SETTINGS)}"
        )

    settings = COMPLEXITY_SETTINGS[complexity]

    rng = random.Random(seed)

    points = _generate_points(
        width=width,
        height=height,
        count=settings["points"],
        rng=rng,
    )

    lines = _generate_lines(
        points=points,
        extra_lines=settings["extra_lines"],
        rng=rng,
    )

    polygons = _generate_polygons(
        points=points,
        count=settings["polygons"],
        rng=rng,
    )

    return Pattern(
        width=width,
        height=height,
        points=tuple(points),
        lines=tuple(lines),
        polygons=tuple(polygons),
    )


def _generate_points(
    width: int,
    height: int,
    count: int,
    rng: random.Random,
) -> list[Point]:
    margin_x = width * 0.05
    margin_y = height * 0.05

    points = []

    for _ in range(count):
        x = rng.uniform(
            margin_x,
            width - margin_x,
        )

        y = rng.uniform(
            margin_y,
            height - margin_y,
        )

        points.append(
            Point(
                x=x,
                y=y,
            )
        )

    return points


def _generate_lines(
    points: list[Point],
    extra_lines: int,
    rng: random.Random,
) -> list[Line]:
    lines = []

    if len(points) < 2:
        return lines

    shuffled = points.copy()
    rng.shuffle(shuffled)

    for index in range(len(shuffled) - 1):
        lines.append(
            Line(
                start=shuffled[index],
                end=shuffled[index + 1],
            )
        )

    for _ in range(extra_lines):
        start, end = rng.sample(points, 2)

        lines.append(
            Line(
                start=start,
                end=end,
            )
        )

    return lines


def _generate_polygons(
    points: list[Point],
    count: int,
    rng: random.Random,
) -> list[Polygon]:
    polygons = []

    if len(points) < 3:
        return polygons

    for _ in range(count):
        size = rng.randint(3, 5)

        if len(points) < size:
            size = len(points)

        polygon_points = tuple(
            rng.sample(points, size)
        )

        polygons.append(
            Polygon(
                points=polygon_points,
            )
        )

    return polygons