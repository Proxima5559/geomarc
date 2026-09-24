import hashlib
from pathlib import Path

def _generate_seed(seed: int | None, *args: str | int | Path) -> int | None:

    if seed is None:
        return None
    
    formatted_args = [
        arg.name if isinstance(arg, Path) else str(arg) 
        for arg in args
    ]
    
    unique_str = "_".join([str(seed)] + formatted_args)
    hash_bytes = hashlib.sha256(unique_str.encode("utf-8")).digest()
    
    return int.from_bytes(hash_bytes, byteorder="big") % 4294967296

def _pattern_seed(seed: int | None, index: int) -> int | None:
    
    if seed is None:
        return None

    return seed + index + 1