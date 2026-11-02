import random
import re
from geomarc.constants import (
    COLOR_SEPARATOR,
    DEFAULT_COLOR,
    HEX_COLOR_PATTERN,
    RANDOM_COLOR,
)

_HEX_RE = re.compile(HEX_COLOR_PATTERN)
Color = tuple[int, int, int]


def _parse_hex(value: str) -> Color:
    hex_val = value.lstrip("#")
    if len(hex_val) == 3:
        hex_val = "".join(c * 2 for c in hex_val)
    if len(hex_val) != 6:
        raise ValueError(f"Invalid HEX color: {value}")
    try:
        return (
            int(hex_val[0:2], 16),
            int(hex_val[2:4], 16),
            int(hex_val[4:6], 16),
        )
    except ValueError as e:
        raise ValueError(f"Invalid HEX color digits: {value}") from e


def _validate_rgb(channels: list[str] | tuple[str, str, str]) -> Color:
    if len(channels) != 3:
        raise ValueError("RGB color must have exactly 3 values: red, green, blue")
    
    rgb = []
    for name, part in zip(("Red", "Green", "Blue"), channels):
        try:
            val = int(part.strip())
        except ValueError as e:
            raise ValueError(f"{name} color value must be an integer") from e
        if not 0 <= val <= 255:
            raise ValueError(f"{name} color value must be between 0 and 255")
        rgb.append(val)
    return tuple(rgb)  


def parse_color(value: str | None) -> Color | str:
    if not value or not (val_str := value.strip()):
        return DEFAULT_COLOR

    if val_str.lower() == RANDOM_COLOR:
        return RANDOM_COLOR

    if _HEX_RE.match(val_str):
        return _parse_hex(val_str)

    if COLOR_SEPARATOR in val_str:
        return _validate_rgb(val_str.split(COLOR_SEPARATOR))

    raise ValueError(
        "Invalid color. Use HEX ('#FF5733'), RGB ('255,87,51') or 'random'."
    )

def parse_colors(value: str | None) -> list[Color] | str:
    if not value or not (val_str := value.strip()):
        return [DEFAULT_COLOR]

    if val_str.lower() == RANDOM_COLOR:
        return RANDOM_COLOR

    if ";" not in val_str:
        parsed = parse_color(val_str)
        if parsed == RANDOM_COLOR:
            return RANDOM_COLOR
        return [parsed]  
    
    raw_parts = [p.strip() for p in val_str.split(";") if p.strip()]
    
    if not raw_parts:
        raise ValueError("Color palette cannot be empty")

    colors: list[Color] = []
    for part in raw_parts:
        parsed = parse_color(part)
        if parsed == RANDOM_COLOR:
            raise ValueError("'random' cannot be mixed inside a color palette")
        colors.append(parsed)

    return colors

def resolve_color_for_index(
    color: Color | str | list[Color],
    index: int,
    seed: int | None,
) -> Color:
   
    if isinstance(color, tuple):
        return color

    if color == RANDOM_COLOR:
        return _random_color(seed=seed, index=index)

    if isinstance(color, list):
        if not color:
            return DEFAULT_COLOR
        return color[index % len(color)]

    raise TypeError(
        "Color must be an RGB tuple, 'random' or a list of RGB tuples"
    )


def _random_color(seed: int | None, index: int) -> Color:
    if seed is None:
        rng = random.Random()
    else:
        rng = random.Random(f"{seed}_{index}") 

    return (
        rng.randint(0, 255),
        rng.randint(0, 255),
        rng.randint(0, 255),
    )