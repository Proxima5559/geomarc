# import math
import pymupdf
from ..generator.pattern import Pattern
from ..generator.placement import Placement

def render_pattern(
    page: pymupdf.Page,
    pattern: Pattern,
    placement: Placement,
    line_width: float,
    opacity: int,
) -> None:
    if line_width <= 0:
        raise ValueError("Line width must be greater than 0")
    if not 0 <= opacity <= 255:
        raise ValueError("Opacity must be between 0 and 255")
        
    _draw_pattern(
        page=page,
        pattern=pattern,
        placement=placement,
        line_width=line_width,
        opacity=opacity,
    )

def _draw_pattern(
    page: pymupdf.Page,
    pattern: Pattern,
    placement: Placement,
    line_width: float,
    opacity: int,
) -> None:
    stroke_opacity = opacity / 255.0
    matrix = _get_transformation_matrix(pattern, placement)
    
    for line in pattern.lines:
        start = pymupdf.Point(line.start.x, line.start.y) * matrix
        end = pymupdf.Point(line.end.x, line.end.y) * matrix
        
        page.draw_line(
            start,
            end,
            color=(0, 0, 0),
            width=line_width,
            stroke_opacity=stroke_opacity,
            overlay=True,
        )
        
    for polygon in pattern.polygons:
        if len(polygon.points) < 3:
            continue
            
        points = [pymupdf.Point(p.x, p.y) * matrix for p in polygon.points]
        points.append(points[0]) 
        
        page.draw_polyline(
            points,
            color=(0, 0, 0),
            width=line_width,
            stroke_opacity=stroke_opacity,
            overlay=True,
        )

def _get_transformation_matrix(pattern: Pattern, placement: Placement) -> pymupdf.Matrix:
    """Computes a single transformation matrix for the entire placement."""
    scale_x = placement.width / pattern.width
    scale_y = placement.height / pattern.height
    
    center_x = placement.width / 2.0
    center_y = placement.height / 2.0
    
    mat = pymupdf.Matrix(scale_x, scale_y)
    mat.pretranslate(-center_x, -center_y)
    mat.prerotate(-placement.rotation)
    mat.pretranslate(placement.x + center_x, placement.y + center_y)
    
    return mat