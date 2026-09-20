import pytest
import random
from geomarc.generator.placement import (
    generate_placements,
    Placement,
    _generate_size,
    _generate_position,
    _boxes_overlap,
)

def test_generate_placements_success():
    image_width = 1000
    image_height = 800
    count = 5
    
    result = generate_placements(image_width, image_height, count=count)
    
    assert isinstance(result, tuple)
    assert len(result) == count
    for item in result:
        assert isinstance(item, Placement)
        assert item.width > 0
        assert item.height > 0
        assert 0 <= item.x <= image_width
        assert 0 <= item.y <= image_height
        assert -45 <= item.rotation <= 45

def test_generate_placements_determinism():
    image_width = 500
    image_height = 500
    seed = 42
    
    res1 = generate_placements(image_width, image_height, count=4, seed=seed)
    res2 = generate_placements(image_width, image_height, count=4, seed=seed)
    
    assert res1 == res2

def test_generate_placements_invalid_dimensions():
    with pytest.raises(ValueError, match="Image dimensions must be greater than 0"):
        generate_placements(0, 500)
        
    with pytest.raises(ValueError, match="Image dimensions must be greater than 0"):
        generate_placements(500, -10)

@pytest.mark.parametrize("count", [2, 11, 0, -5])
def test_generate_placements_invalid_count(count):
    with pytest.raises(ValueError, match="Count must be between 3 and 10"):
        generate_placements(500, 500, count=count)

def test_generate_size_logic():
    rng = random.Random(123)
    width, height = _generate_size(1000, 500, rng)
    
    assert width > 0
    assert height > 0
    assert width <= 1000 * 0.45
    assert height <= 500 * 0.45

def test_generate_position_logic():
    rng = random.Random(123)
    image_width = 800
    image_height = 600
    w_width = 200
    w_height = 150
    rotation = 0.0
    
    x, y = _generate_position(image_width, image_height, w_width, w_height, rotation, rng)
    
    assert 0 <= x <= (image_width - w_width)
    assert 0 <= y <= (image_height - w_height)

def test_boxes_overlap():
    box1 = (0.0, 0.0, 100.0, 100.0)
    box2 = (50.0, 50.0, 150.0, 150.0)
    box3 = (200.0, 200.0, 300.0, 300.0)
    
    assert _boxes_overlap(box1, box2) is True
    assert _boxes_overlap(box1, box3) is False

def test_generate_placements_exhaustion_raises_runtime_error():
    # Force collision exhaustion by requesting too many large placements in a tiny space
    with pytest.raises(RuntimeError, match="Could not find valid placement"):
        generate_placements(100, 100, count=10, seed=42)