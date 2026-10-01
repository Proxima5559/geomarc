from pathlib import Path
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TaskProgressColumn, TimeRemainingColumn

from geomarc.utils.validator import Validator
from .watermark import apply_watermark
from geomarc.constants import SUPPORTED_EXTENSIONS
from geomarc.utils.seed import _generate_seed as _file_seed
from geomarc.generator.placement import ProtectedRegion

def process_folder(
    input_dir: str | Path,
    output_dir: str | Path,
    complexity: str = "medium",
    line_width: float = 2,
    opacity: int = 100,
    seed: int | None = None,
    count: int = 5,
    on_unsupported: str = "skip",
    protected_regions: list[ProtectedRegion] | None = None,
) -> tuple[int, int]:
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)

    Validator(input_dir, "Input directory").is_dir()
    Validator(count, "Count").between(3, 10)
    Validator(on_unsupported, "on_unsupported").in_choices({"skip", "fail"})

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
                    protected_regions=protected_regions,
                )
                processed += 1

            except ValueError as e:
                if on_unsupported == "fail":
                    raise e
                skipped += 1

            progress.advance(task)

    return processed, skipped
