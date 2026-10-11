import json
from pathlib import Path
import click

CONFIG_FILE_NAME = "config.json"
VALID_KEYS = {"complexity", "count", "opacity", "line_width"}


def get_config_path() -> Path:
    app_dir = Path(click.get_app_dir("geomarc"))
    app_dir.mkdir(parents=True, exist_ok=True)
    return app_dir / CONFIG_FILE_NAME


def load_config() -> dict:
    path = get_config_path()
    if not path.exists():
        return {}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, dict):
                return data
    except (json.JSONDecodeError, OSError):
        pass
    return {}


def save_config(config: dict) -> None:
    path = get_config_path()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def get_config_value(key: str):
    config = load_config()
    return config.get(key)


def set_config_value(key: str, value) -> None:
    if key not in VALID_KEYS:
        raise ValueError(f"Invalid configuration key: {key}")
    config = load_config()
    config[key] = value
    save_config(config)


def reset_config() -> None:
    path = get_config_path()
    if path.exists():
        path.unlink()