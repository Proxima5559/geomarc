from dataclasses import dataclass

from geomarc.utils.validator import Validator


@dataclass(frozen=True)
class ProtectedRegion:
    left: float
    top: float
    right: float
    bottom: float

    def __post_init__(self) -> None:
      Validator(self.left, "Protected region left").between(0, 1)
      Validator(self.top, "Protected region top").between(0, 1)
      Validator(self.right, "Protected region right").gt(self.left).lte(1)
      Validator(self.bottom, "Protected region bottom").gt(self.top).lte(1)

    @property
    def box(self) -> tuple[float, float, float, float]:
        return (
            self.left,
            self.top,
            self.right,
            self.bottom,
        )


def intersects_protected_region(
    placement_box: tuple[float, float, float, float],
    protected_regions: list[ProtectedRegion],
) -> bool:
    for region in protected_regions:
        if boxes_overlap(
            placement_box,
            region.box,
        ):
            return True

    return False


def boxes_overlap(
    first: tuple[float, float, float, float],
    second: tuple[float, float, float, float],
) -> bool:
    first_left, first_top, first_right, first_bottom = first
    second_left, second_top, second_right, second_bottom = second

    return not (
        first_right <= second_left
        or first_left >= second_right
        or first_bottom <= second_top
        or first_top >= second_bottom
    )