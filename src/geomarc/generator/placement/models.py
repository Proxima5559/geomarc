from dataclasses import dataclass


@dataclass(frozen=True)
class Placement:
    x: float
    y: float
    width: float
    height: float
    rotation: float