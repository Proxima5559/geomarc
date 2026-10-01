import pytest
from geomarc.generator.placement.protected  import ProtectedRegion, boxes_overlap, intersects_protected_region



def test_protected_region_valid():
    region = ProtectedRegion(left=0.1, top=0.2, right=0.4, bottom=0.5)
    assert region.box == (0.1, 0.2, 0.4, 0.5)


@pytest.mark.parametrize("left,top,right,bottom,expected_msg", [
    (-0.1, 0.2, 0.4, 0.5, "Protected region left must be >= 0"),
    (0.1, -0.2, 0.4, 0.5, "Protected region top must be >= 0"),
    (0.4, 0.2, 0.4, 0.5, "Protected region right must be greater than left"),
    (0.5, 0.2, 0.4, 0.5, "Protected region right must be greater than left"),
    (0.1, 0.5, 0.4, 0.5, "Protected region bottom must be greater than top"),
    (0.1, 0.6, 0.4, 0.5, "Protected region bottom must be greater than top"),
    (1.1, 0.2, 1.4, 0.5, "Protected region left must be <= 1"),
    (0.1, 1.2, 0.4, 1.5, "Protected region top must be <= 1"),
    (0.1, 0.2, 1.5, 0.5, "Protected region right must be <= 1"),
    (0.1, 0.2, 0.4, 1.5, "Protected region bottom must be <= 1"),
])
def test_protected_region_invalid_values(left, top, right, bottom, expected_msg):
    with pytest.raises(ValueError) as exc_info:
        ProtectedRegion(left=left, top=top, right=right, bottom=bottom)
    assert expected_msg in str(exc_info.value)



def test_boxes_overlap_true():
    box1 = (0.1, 0.1, 0.5, 0.5)
    
    assert boxes_overlap(box1, (0.1, 0.1, 0.5, 0.5)) is True
    assert boxes_overlap(box1, (0.2, 0.2, 0.4, 0.4)) is True
    assert boxes_overlap(box1, (0.4, 0.4, 0.8, 0.8)) is True


def test_boxes_overlap_false():
    box1 = (0.1, 0.1, 0.4, 0.4)
    
    assert boxes_overlap(box1, (0.5, 0.1, 0.8, 0.4)) is False
    assert boxes_overlap(box1, (0.1, 0.5, 0.4, 0.8)) is False


def test_boxes_overlap_touching_edges():
    box1 = (0.1, 0.1, 0.4, 0.4)
    
    assert boxes_overlap(box1, (0.4, 0.1, 0.7, 0.4)) is False
    assert boxes_overlap(box1, (0.1, 0.4, 0.4, 0.7)) is False



def test_intersects_protected_region_empty_list():
    placement = (0.1, 0.1, 0.3, 0.3)
    assert intersects_protected_region(placement, []) is False


def test_intersects_protected_region_multiple():
    regions = [
        ProtectedRegion(0.1, 0.1, 0.3, 0.3),
        ProtectedRegion(0.7, 0.7, 0.9, 0.9)
    ]
    
    assert intersects_protected_region((0.2, 0.2, 0.4, 0.4), regions) is True
    assert intersects_protected_region((0.8, 0.8, 0.95, 0.95), regions) is True
    assert intersects_protected_region((0.4, 0.4, 0.6, 0.6), regions) is False
