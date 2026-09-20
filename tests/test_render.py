import pytest
from PIL import Image
from geomarc.generator.pattern import Pattern
from geomarc.renders.img_render import render_pattern


def test_render_pattern_success():
    pattern = Pattern(
        width=100, 
        height=100, 
        points=[], 
        lines=[], 
        polygons=[]
    )
    image = render_pattern(pattern, line_width=2.0, opacity=255)
    
    assert isinstance(image, Image.Image)
    assert image.size == (100, 100)
    assert image.mode == "RGBA"


def test_render_pattern_min_dimensions():
    pattern = Pattern(
        width=0, 
        height=0, 
        points=[], 
        lines=[], 
        polygons=[]
    )
    image = render_pattern(pattern, line_width=1.0, opacity=100)
    
    assert isinstance(image, Image.Image)
    assert image.size == (1, 1)


@pytest.mark.parametrize("line_width", [0, -1.5])
def test_render_pattern_invalid_line_width(line_width: float):
    pattern = Pattern(
        width=100, 
        height=100, 
        points=[], 
        lines=[], 
        polygons=[]
    )
    
    with pytest.raises(ValueError, match="Line width must be greater than 0"):
        render_pattern(pattern, line_width=line_width, opacity=255)


@pytest.mark.parametrize("opacity", [-1, 256])
def test_render_pattern_invalid_opacity(opacity: int):
    pattern = Pattern(
        width=100, 
        height=100, 
        points=[], 
        lines=[], 
        polygons=[]
    )
    
    with pytest.raises(ValueError, match="Opacity must be between 0 and 255"):
        render_pattern(pattern, line_width=2.0, opacity=opacity)