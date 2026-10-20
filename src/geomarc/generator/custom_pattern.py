import json
from dataclasses import dataclass
from pathlib import Path

from geomarc.constants import MAX_POINTS, MAX_EXTRA_LINES, MAX_POLYGONS

@dataclass(frozen=True)
class CustomPattern:
    points: int
    extra_lines: int
    polygons: int



def load_custom_pattern(path: Path) -> CustomPattern:
    try:
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError as error:
        raise ValueError(f"Pattern file not found: {path}") from error
    except json.JSONDecodeError as error:
        raise ValueError(f"Invalid JSON in pattern file: {path}") from error

    if not isinstance(data, dict):
        raise ValueError("Pattern file must contain a JSON object.")

    return validate_custom_pattern(data)


def validate_custom_pattern(data: dict) -> CustomPattern:
    required_keys = ("points", "extra_lines", "polygons")
    missing = [key for key in required_keys if key not in data]

    if missing:
        raise ValueError(
            "Pattern file is missing required keys: "
            f"{', '.join(missing)}"
        )

    values = {}

    for key in required_keys:
        value = data[key]

        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError(f"Pattern value '{key}' must be an integer.")

        if value < 0:
            raise ValueError(f"Pattern value '{key}' must not be negative.")

        values[key] = value

    if values["points"] > MAX_POINTS:
        raise ValueError(
            f"Pattern value 'points' must not be greater than {MAX_POINTS}."
        )

    if values["extra_lines"] > MAX_EXTRA_LINES:
        raise ValueError(
            f"Pattern value 'extra_lines' must not be greater "
            f"than {MAX_EXTRA_LINES}."
        )

    if values["polygons"] > MAX_POLYGONS:
        raise ValueError(
            f"Pattern value 'polygons' must not be greater "
            f"than {MAX_POLYGONS}."
        )

    return CustomPattern(**values)