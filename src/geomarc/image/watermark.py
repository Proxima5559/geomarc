from pathlib import Path
from dataclasses import dataclass
from PIL import Image, UnidentifiedImageError

from geomarc.generator.placement import ProtectedRegion
from geomarc.utils.validator import Validator

from ..generator.pattern import generate_pattern
from ..generator.placement import generate_placements
from ..renders.img_render import render_pattern
from ..utils.seed import _pattern_seed



def _process_watermark(
    input_path: Path,
    target_path: Path,
    complexity: str,
    style: str | None,
    line_width: float,
    opacity: int,
    seed: int | None,
    count: int,
    protected_regions: list[ProtectedRegion] | None = None,
    custom_points: int | None = None,
    custom_extra_lines: int | None = None,
    custom_polygons: int | None = None,
) -> None:
    Validator(input_path, "Input file").is_file()
    Validator(line_width, "Line width").gt(0)
    Validator(opacity, "Opacity").between(0, 255)
    Validator(count, "Count").between(3, 10)

    try:
        with Image.open(input_path) as image:
            image.load()
            image = image.convert("RGBA")

            overlay = _create_overlay(
                image_width=image.width,
                image_height=image.height,
                complexity=complexity,
                style=style,
                line_width=line_width,
                opacity=opacity,
                seed=seed,
                count=count,
                protected_regions=protected_regions,
                custom_points=custom_points,
                custom_extra_lines=custom_extra_lines,
                custom_polygons=custom_polygons,
            )

            result = Image.alpha_composite(image, overlay)
            _save_image(image=result, output_path=target_path)

    except (UnidentifiedImageError, ValueError, OSError, SyntaxError) as error:
        raise ValueError(
            f"Invalid or corrupted image file '{input_path.name}': {error}"
        ) from error



def _create_overlay(
    image_width: int,
    image_height: int,
    complexity: str,
    style: str | None,
    line_width: float,
    opacity: int,
    seed: int | None,
    count: int,
    protected_regions: list[ProtectedRegion] | None = None,
    custom_points: int | None = None,
    custom_extra_lines: int | None = None,
    custom_polygons: int | None = None,
) -> Image.Image:
    placements = generate_placements(
        image_width=image_width,
        image_height=image_height,
        count=count,
        seed=seed,
        protected_regions=protected_regions,
    )

    overlay = Image.new(
        "RGBA",
        (
            image_width,
            image_height,
        ),
        (0, 0, 0, 0),
    )

    for index, placement in enumerate(placements):
        pattern_seed = _pattern_seed(
            seed=seed,
            index=index,
        )

        pattern = generate_pattern(
            width=max(1, round(placement.width)),
            height=max(1, round(placement.height)),
            complexity=complexity,
            style=style,
            seed=pattern_seed,
            custom_points=custom_points,
            custom_extra_lines=custom_extra_lines,
            custom_polygons=custom_polygons,
        )

        watermark = render_pattern(
            pattern=pattern,
            line_width=line_width,
            opacity=opacity,
        )

        rotated = watermark.rotate(
            placement.rotation,
            expand=True,
            resample=Image.Resampling.BICUBIC,
        )

        overlay.alpha_composite(
            rotated,
            (
                round(
                    placement.x
                    - (rotated.width - watermark.width) / 2
                ),
                round(
                    placement.y
                    - (rotated.height - watermark.height) / 2
                ),
            ),
        )

    return overlay


def _save_image(
    image: Image.Image,
    output_path: Path,
) -> None:
    suffix = output_path.suffix.lower()

    if suffix in {".jpg", ".jpeg"}:
        image = image.convert("RGB")

    image.save(output_path)


def apply_watermark(
    input_path: str | Path,
    output_path: str | Path,
    complexity: str = "medium",
    style: str | None = None,
    line_width: float = 2,
    opacity: int = 100,
    seed: int | None = None,
    count: int = 5,
    protected_regions: list[ProtectedRegion] | None = None,
    custom_points: int | None = None,
    custom_extra_lines: int | None = None,
    custom_polygons: int | None = None,
) -> None:
    _process_watermark(
        input_path=Path(input_path),
        target_path=Path(output_path),
        complexity=complexity,
        style=style,
        line_width=line_width,
        opacity=opacity,
        seed=seed,
        count=count,
        protected_regions=protected_regions,
        custom_points=custom_points,
        custom_extra_lines=custom_extra_lines,
        custom_polygons=custom_polygons,
    )


def preview_watermark(
    input_path: str | Path,
    preview_path: str | Path,
    complexity: str = "medium",
    style: str | None = None,
    line_width: float = 2,
    opacity: int = 100,
    seed: int | None = None,
    count: int = 5,
    protected_regions: list[ProtectedRegion] | None = None,
    custom_points: int | None = None,
    custom_extra_lines: int | None = None,
    custom_polygons: int | None = None,
) -> None:
    _process_watermark(
        input_path=Path(input_path),
        target_path=Path(preview_path),
        complexity=complexity,
        style=style,
        line_width=line_width,
        opacity=opacity,
        seed=seed,
        count=count,
        protected_regions=protected_regions,
        custom_points=custom_points,
        custom_extra_lines=custom_extra_lines,
        custom_polygons=custom_polygons,
    )

@dataclass
class BatchItemResult:
    input_path: Path
    output_path: Path
    success: bool
    error: str | None = None


def apply_watermark_batch(
    inputs: list[str | Path] | tuple[str | Path, ...],
    output_dir: str | Path,
    complexity: str = "medium",
    style: str | None = None,
    line_width: float = 2.0,
    opacity: int = 100,
    seed: int | None = None,
    count: int = 5,
    protected_regions: list[ProtectedRegion] | None = None,
    inspect: bool = False,
    custom_points: int | None = None,
    custom_extra_lines: int | None = None,
    custom_polygons: int | None = None,
) -> list[BatchItemResult]:
    input_paths = [Path(p) for p in inputs]
    out_dir = Path(output_dir)

    filenames = [p.name for p in input_paths]
    if len(filenames) != len(set(filenames)):
        raise ValueError("Input files have duplicate names, which would cause output conflicts.")

    out_dir.mkdir(parents=True, exist_ok=True)
    results: list[BatchItemResult] = []
    processor = preview_watermark if inspect else apply_watermark

    for input_path in input_paths:
        target_path = out_dir / input_path.name


        try:
            is_same_path = input_path.resolve() == target_path.resolve()
        except OSError:
            is_same_path = input_path == target_path

        if is_same_path:
            results.append(BatchItemResult(
                input_path=input_path,
                output_path=target_path,
                success=False,
                error="output path cannot be the same as input path"
            ))
            continue

        try:
            processor(
                input_path=input_path,
                output_path=target_path,
                complexity=complexity,
                style=style,
                line_width=line_width,
                opacity=opacity,
                seed=seed,
                count=count,
                protected_regions=protected_regions,
                custom_points=custom_points,
                custom_extra_lines=custom_extra_lines,
                custom_polygons=custom_polygons,
            )
            results.append(BatchItemResult(
                input_path=input_path,
                output_path=target_path,
                success=True
            ))
        except Exception as error:
            results.append(BatchItemResult(
                input_path=input_path,
                output_path=target_path,
                success=False,
                error=str(error)
            ))

    return results