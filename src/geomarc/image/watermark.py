from pathlib import Path

from PIL import Image, UnidentifiedImageError

from ..generator.pattern import generate_pattern
from ..generator.placement import generate_placements
from ..renders.img_render import render_pattern


def apply_watermark(
    input_path: str | Path,
    output_path: str | Path,
    complexity: str = "medium",
    line_width: float = 2,
    opacity: int = 100,
    seed: int | None = None,
    count: int = 5,
) -> None:
    input_path = Path(input_path)
    output_path = Path(output_path)

    if not input_path.is_file():
        raise FileNotFoundError(
            f"Input file not found: {input_path}"
        )

    if line_width <= 0:
        raise ValueError(
            "Line width must be greater than 0"
        )

    if not 0 <= opacity <= 255:
        raise ValueError(
            "Opacity must be between 0 and 255"
        )

    if not 3 <= count <= 10:
        raise ValueError(
            "Count must be between 3 and 10"
        )

    try:
        with Image.open(input_path) as image:
            image.load()
            image = image.convert("RGBA")

            overlay = _create_overlay(
                image_width=image.width,
                image_height=image.height,
                complexity=complexity,
                line_width=line_width,
                opacity=opacity,
                seed=seed,
                count=count,
            )

            result = Image.alpha_composite(
                image,
                overlay,
            )

            output_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            _save_image(
                image=result,
                output_path=output_path,
            )

    except (
        UnidentifiedImageError,
        ValueError,
        OSError,
        SyntaxError,
    ) as error:
        raise ValueError(
            f"Invalid or corrupted image file "
            f"'{input_path.name}': {error}"
        ) from error


def _create_overlay(
    image_width: int,
    image_height: int,
    complexity: str,
    line_width: float,
    opacity: int,
    seed: int | None,
    count: int,
) -> Image.Image:
    placements = generate_placements(
        image_width=image_width,
        image_height=image_height,
        count=count,
        seed=seed,
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
            seed=pattern_seed,
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


def _pattern_seed(
    seed: int | None,
    index: int,
) -> int | None:
    if seed is None:
        return None

    return seed + index + 1


def _save_image(
    image: Image.Image,
    output_path: Path,
) -> None:
    suffix = output_path.suffix.lower()

    if suffix in {".jpg", ".jpeg"}:
        image = image.convert("RGB")

    image.save(output_path)