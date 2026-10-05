import random
from geomarc.constants import STYLE_CONFIGS
from .geometry import Line, Point, Polygon


def generate_styled_pattern_elements(
    width: int,
    height: int,
    style: str,
    base_points_count: int,
    base_extra_lines: int,
    base_polygons_count: int,
    rng: random.Random,
) -> tuple[list[Point], list[Line], list[Polygon]]:
    config = STYLE_CONFIGS.get(style, STYLE_CONFIGS["line_mesh"])

    p_count = max(2, int(base_points_count * config["points_multiplier"]))
    l_count = int(base_extra_lines * config["lines_multiplier"])
    poly_count = int(base_polygons_count * config["polygons_multiplier"])

    if style == "minimal":
        points = _generate_minimal_points(width, height, p_count, rng)
    elif style == "angular_sharp":
        points = _generate_angular_points(width, height, p_count, rng)
    else:
        points = _generate_default_points(width, height, p_count, rng)

    lines = _generate_lines_for_style(points, l_count, style, rng)
    polygons = _generate_polygons_for_style(points, poly_count, style, rng)

    return points, lines, polygons


def _generate_default_points(width: int, height: int, count: int, rng: random.Random) -> list[Point]:
    margin_x = width * 0.05
    margin_y = height * 0.05
    return [
        Point(
            x=rng.uniform(margin_x, width - margin_x),
            y=rng.uniform(margin_y, height - margin_y),
        )
        for _ in range(count)
    ]


def _generate_minimal_points(width: int, height: int, count: int, rng: random.Random) -> list[Point]:
    margin_x = width * 0.15
    margin_y = height * 0.15
    return [
        Point(
            x=rng.uniform(margin_x, width - margin_x),
            y=rng.uniform(margin_y, height - margin_y),
        )
        for _ in range(count)
    ]


def _generate_angular_points(width: int, height: int, count: int, rng: random.Random) -> list[Point]:
    points = _generate_default_points(width, height, count, rng)
    return points


def _generate_lines_for_style(points: list[Point], extra_lines: int, style: str, rng: random.Random) -> list[Line]:
    lines = []
    if len(points) < 2:
        return lines

    shuffled = points.copy()
    rng.shuffle(shuffled)

    step = 1 if style != "minimal" else 2
    for index in range(0, len(shuffled) - step, step):
        lines.append(Line(start=shuffled[index], end=shuffled[index + step]))

    for _ in range(extra_lines):
        if len(points) >= 2:
            start, end = rng.sample(points, 2)
            lines.append(Line(start=start, end=end))

    return lines


def _generate_polygons_for_style(points: list[Point], count: int, style: str, rng: random.Random) -> list[Polygon]:
    polygons = []
    if len(points) < 3 or style == "minimal":
        return polygons

    max_poly_size = 4 if style == "angular_sharp" else 5

    for _ in range(count):
        size = rng.randint(3, max_poly_size)
        if len(points) < size:
            size = len(points)

        polygon_points = tuple(rng.sample(points, size))
        polygons.append(Polygon(points=polygon_points))

    return polygons