import pytest
from unittest.mock import MagicMock
from geomarc.generator.pattern import Pattern, Line, Polygon, Point
from geomarc.generator.placement import Placement
from geomarc.renders.pdf_render import render_pattern


@pytest.fixture
def sample_placement():
    return Placement(x=0.0, y=0.0, width=100.0, height=100.0, rotation=0.0)


def test_render_pattern_invalid_line_width(sample_placement):
    page = MagicMock()
    pattern = Pattern(width=100, height=100, points=[], lines=[], polygons=[])
    
    with pytest.raises(ValueError, match="Line width must be greater than 0"):
        render_pattern(page, pattern, placement=sample_placement, line_width=0, opacity=100)
    
    with pytest.raises(ValueError, match="Line width must be greater than 0"):
        render_pattern(page, pattern, placement=sample_placement, line_width=-1.5, opacity=100)


def test_render_pattern_invalid_opacity(sample_placement):
    page = MagicMock()
    pattern = Pattern(width=100, height=100, points=[], lines=[], polygons=[])
    
    with pytest.raises(ValueError, match="Opacity must be between 0 and 255"):
        render_pattern(page, pattern, placement=sample_placement, line_width=2.0, opacity=-1)
    
    with pytest.raises(ValueError, match="Opacity must be between 0 and 255"):
        render_pattern(page, pattern, placement=sample_placement, line_width=2.0, opacity=256)


def test_render_pattern_draws_lines_and_polygons(sample_placement):
    page = MagicMock()
    
    line = Line(start=Point(0, 0), end=Point(10, 10))
    polygon = Polygon(points=[Point(20, 20), Point(30, 20), Point(25, 30)])
    pattern = Pattern(width=100, height=100, points=[], lines=[line], polygons=[polygon])

    render_pattern(page, pattern, placement=sample_placement, line_width=2.0, opacity=128)

    assert page.draw_line.call_count == 1