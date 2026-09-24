import hashlib
from pathlib import Path
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn
from .watermark import apply_watermark
from geomarc.constants import SUPPORTED_EXTENSIONS
from geomarc.utils.seed import _generate_seed as _file_seed

def process_folder(
    input_dir: str | Path,
    output_dir: str | Path,
    complexity: str = "medium",
    line_width: float = 2,
    opacity: int = 100,
    seed: int | None = None,
    count: int = 5,
    on_unsupported: str = "skip",
) -> tuple[int, int]:
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    if not input_dir.is_dir():
        raise NotADirectoryError(
            f"Input directory not found: {input_dir}"
        )
    if not 3 <= count <= 10:
        raise ValueError("Count must be between 3 and 10")
    
    if on_unsupported not in {"skip", "fail"}:
        raise ValueError(
            "on_unsupported must be 'skip' or 'fail'"
        )

    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    files_to_process = []
    skipped = 0

    for input_path in sorted(input_dir.iterdir()):
        if not input_path.is_file():
            continue

        if input_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            if on_unsupported == "fail":
                raise ValueError(
                    f"Unsupported file format: {input_path.name}"
                )
            skipped += 1
            continue

        files_to_process.append(input_path)

    processed = 0

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TimeRemainingColumn(),
    ) as progress:
        task = progress.add_task("Watermarking images...", total=len(files_to_process))

        for input_path in files_to_process:
            output_path = output_dir / input_path.name
            
            try:
                apply_watermark(
                    input_path=input_path,
                    output_path=output_path,
                    complexity=complexity,
                    line_width=line_width,
                    opacity=opacity,
                    seed=_file_seed(seed, input_path),
                    count=count,
                )
                processed += 1

            except ValueError as e:
                if on_unsupported == "fail":
                    raise e
                skipped += 1

            progress.advance(task)

    return processed, skipped
