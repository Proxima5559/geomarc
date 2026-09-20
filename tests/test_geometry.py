from geomarc.generator.geometry import Line, Point, Polygon, distance, line_length
from geomarc.generator.pattern import generate_pattern


def test_point_creation():
    point = Point(10, 20)

    assert point.x == 10
    assert point.y == 20


def test_distance():
    a = Point(0, 0)
    b = Point(3, 4)

    assert distance(a, b) == 5


def test_line_length():
    line = Line(
        start=Point(0, 0),
        end=Point(3, 4),
    )

    assert line_length(line) == 5


def test_polygon_creation():
    polygon = Polygon(
        points=(
            Point(0, 0),
            Point(100, 0),
            Point(50, 100),
        )
    )

    assert len(polygon.points) == 3


def test_pattern_is_deterministic():
    first = generate_pattern(
        width=1000,
        height=800,
        complexity="high",
        seed=12345,
    )
    
    second = generate_pattern(
        width=1000,
        height=800,
        complexity="high",
        seed=12345,
    )

    assert first == second

def test_different_seeds_create_different_patterns():
    first = generate_pattern(
        width=1000,
        height=800,
        complexity="high",
        seed=12345,
    )

    second = generate_pattern(
        width=1000,
        height=800,
        complexity="high",
        seed=54321,
    )

    assert first != second