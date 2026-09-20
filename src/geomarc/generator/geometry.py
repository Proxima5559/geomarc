# И пока не добавляем сюда random, complexity, Pillow, opacity и т.д.
from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    x: float
    y: float


@dataclass(frozen=True)
class Line:
    start: Point
    end: Point


@dataclass(frozen=True)
class Polygon:
    points: tuple[Point, ...]


def distance(a: Point, b: Point) -> float:
    dx = b.x - a.x
    dy = b.y - a.y

    return (dx**2 + dy**2) ** 0.5


def line_length(line: Line) -> float:
    return distance(line.start, line.end)