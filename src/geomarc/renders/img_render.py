from PIL import Image, ImageDraw

from ..generator.pattern import Pattern
from ..utils.colors import Color

def render_pattern(
    pattern: Pattern,
    line_width: float,
    opacity: int,
    color: Color = (255, 255, 255),
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
        color=color
    )

    return image


def _draw_pattern(
    draw: ImageDraw.ImageDraw,
    pattern: Pattern,
    line_width: float,
    opacity: int,
    color: Color,
) -> None:
    width = max(1, round(line_width))

    fill = (*color, opacity)
    for line in pattern.lines:
        draw.line(
            (
                line.start.x,
                line.start.y,
                line.end.x,
                line.end.y,
            ),
            fill=fill,
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
            fill=fill,
            width=width,
        )