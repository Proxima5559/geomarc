from PIL import Image, ImageDraw

from ..generator.pattern import Pattern


def render_pattern(
    pattern: Pattern,
    line_width: float,
    opacity: int,
) -> Image.Image:
    if line_width <= 0:
        raise ValueError("Line width must be greater than 0")

    if not 0 <= opacity <= 255:
        raise ValueError("Opacity must be between 0 and 255")

    image = Image.new(
        "RGBA",
        (
            max(1, pattern.width),
            max(1, pattern.height),
        ),
        (0, 0, 0, 0),
    )

    draw = ImageDraw.Draw(image)

    _draw_pattern(
        draw=draw,
        pattern=pattern,
        line_width=line_width,
        opacity=opacity,
    )

    return image


def _draw_pattern(
    draw: ImageDraw.ImageDraw,
    pattern: Pattern,
    line_width: float,
    opacity: int,
) -> None:
    width = max(1, round(line_width))

    for line in pattern.lines:
        draw.line(
            (
                line.start.x,
                line.start.y,
                line.end.x,
                line.end.y,
            ),
            fill=(255, 255, 255, opacity),
            width=width,
        )

    for polygon in pattern.polygons:
        if len(polygon.points) < 3:
            continue

        points = [
            (point.x, point.y)
            for point in polygon.points
        ]

        draw.line(
            points + [points[0]],
            fill=(255, 255, 255, opacity),
            width=width,
        )