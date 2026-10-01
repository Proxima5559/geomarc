from dataclasses import dataclass


@dataclass(frozen=True)
class ProtectedRegion:
    left: float
    top: float
    right: float
    bottom: float

    def __post_init__(self) -> None:
        if self.left < 0:
            raise ValueError("Protected region left must be >= 0")
        if self.left > 1:
            raise ValueError("Protected region left must be <= 1")

        if self.top < 0:
            raise ValueError("Protected region top must be >= 0")
        if self.top > 1:
            raise ValueError("Protected region top must be <= 1")

        if self.right <= self.left:
            raise ValueError(
                "Protected region right must be greater than left"
            )
        if self.right > 1:
            raise ValueError("Protected region right must be <= 1")

        if self.bottom <= self.top:
            raise ValueError(
                "Protected region bottom must be greater than top"
            )
        if self.bottom > 1:
            raise ValueError("Protected region bottom must be <= 1")

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