from pathlib import Path
from typing import Any, Callable, Self, Iterable

class Validator:
    def __init__(self, value: Any, name: str):
        self.value = value
        self.name = name

    def gte(self, min_val: Any) -> Self:
        if self.value < min_val:
            raise ValueError(f"{self.name} ({self.value}) must be >= {min_val}")
        return self

    def lte(self, max_val: Any) -> Self:
        if self.value > max_val:
            raise ValueError(f"{self.name} ({self.value}) must be <= {max_val}")
        return self

    def gt(self, min_val: Any) -> Self:
        if self.value <= min_val:
            raise ValueError(f"{self.name} must be greater than {min_val}")
        return self

    def between(self, min_val: Any, max_val: Any) -> Self:
        if not (min_val <= self.value <= max_val):
            raise ValueError(f"{self.name} must be between {min_val} and {max_val}")
        return self

    def in_choices(self, choices: Iterable[Any]) -> Self:
        if self.value not in choices:
            choices_str = ", ".join(f"'{c}'" for c in choices)
            raise ValueError(f"{self.name} must be {choices_str}")
        return self

    def is_file(self) -> Self:
        if not isinstance(self.value, Path):
            path_obj = Path(self.value)
        else:
            path_obj = self.value
            
        if not path_obj.is_file():
            raise FileNotFoundError(f"Input file not found: {path_obj}")
        return self

    def is_dir(self) -> Self:
        if not isinstance(self.value, Path):
            path_obj = Path(self.value)
        else:
            path_obj = self.value
            
        if not path_obj.is_dir():
            raise NotADirectoryError(f"Input directory not found: {path_obj}")
        return self

    def maybe(self, method_name: str, *args, **kwargs) -> Self:
        if self.value is None:
            return self
        method = getattr(self, method_name)
        return method(*args, **kwargs)
