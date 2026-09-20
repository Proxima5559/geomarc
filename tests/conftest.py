import sys
from pathlib import Path

src_path = str(Path(__file__).resolve().parent.parent / "src")
sys.path.insert(0, src_path)
print("DEBUG: Added path ->", src_path)