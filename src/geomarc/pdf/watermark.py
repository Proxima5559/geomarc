from pathlib import Path

import pymupdf  
from geomarc.utils.validator import Validator
from ..generator.pattern import generate_pattern
from ..generator.placement import generate_placements
from ..renders.pdf_render import render_pattern
from ..utils.seed import _generate_seed

def apply_watermark(
    input_path: str | Path,
    output_path: str | Path,
    complexity: str = "medium",
    line_width: float = 2,
    opacity: int = 100,
    seed: int | None = None,
    count: int = 5,
    interval: int | None = None,
) -> None:
    input_path = Path(input_path)
    output_path = Path(output_path)

    Validator(input_path, "Input file").is_file()
    Validator(line_width, "Line width").gt(0)
    Validator(opacity, "Opacity").between(0, 255)
    Validator(count, "Count").between(3, 10)
    Validator(interval, "Interval").maybe("gt", 0)

    try:
        document = pymupdf.open(input_path)

        try:
            page_numbers = _get_page_numbers(
                page_count=len(document),
                interval=interval,
            )

            if not page_numbers:
                raise ValueError(
                    f"PDF has {len(document)} pages, "
                    f"but interval {interval} selects no pages"
                )

            layout_cache = {}

            for page_number in page_numbers:
                page = document[page_number]

                if seed is not None:
                    page_width = page.rect.width
                    page_height = page.rect.height
                    cache_key = (round(page_width), round(page_height))

                    if cache_key not in layout_cache:
                        generated_pairs = []
                        
                        page_seed = _generate_seed(seed, "page", input_path.name, page_number)
                        placements = generate_placements(
                            image_width=cache_key[0],
                            image_height=cache_key[1],
                            count=count,
                            seed=page_seed,
                        )
                        
                        for index, placement in enumerate(placements):
                            pattern_seed = _generate_seed(page_seed, "pattern", index)
                            pattern = generate_pattern(
                                width=max(1, round(placement.width)),
                                height=max(1, round(placement.height)),
                                complexity=complexity,
                                seed=pattern_seed,
                            )
                            generated_pairs.append((pattern, placement))
                        
                        layout_cache[cache_key] = generated_pairs

                    for pattern, placement in layout_cache[cache_key]:
                        render_pattern(
                            page=page,
                            pattern=pattern,
                            placement=placement,
                            line_width=line_width,
                            opacity=opacity,
                        )
                else:
                    _apply_page_watermark(
                        page=page,
                        complexity=complexity,
                        line_width=line_width,
                        opacity=opacity,
                        seed=seed,
                        count=count,
                        page_number=page_number,
                        file_name=input_path.name,
                    )

            output_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            document.save(output_path, garbage=3, deflate=True)

        finally:
            document.close()

    except ValueError:
        raise
    except (pymupdf.FileDataError, OSError) as error:
        raise ValueError(
            f"Invalid or corrupted PDF file "
            f"'{input_path.name}': {error}"
        ) from error


def _get_page_numbers(
    page_count: int,
    interval: int | None,
) -> tuple[int, ...]:
    if page_count <= 0:
        return ()

    if interval is None:
        return tuple(range(page_count))

    return tuple(range(interval - 1, page_count, interval))


def _apply_page_watermark(
    page: pymupdf.Page,
    complexity: str,
    line_width: float,
    opacity: int,
    seed: int | None,
    count: int,
    page_number: int,
    file_name: str,
) -> None:
    page_width = page.rect.width
    page_height = page.rect.height

    page_seed = _generate_seed(seed, "page", file_name, page_number)

    placements = generate_placements(
        image_width=round(page_width),
        image_height=round(page_height),
        count=count,
        seed=page_seed,
    )

    for index, placement in enumerate(placements):
        pattern_seed = _generate_seed(page_seed, "pattern", index)

        pattern = generate_pattern(
            width=max(1, round(placement.width)),
            height=max(1, round(placement.height)),
            complexity=complexity,
            seed=pattern_seed,
        )

        render_pattern(
            page=page,
            pattern=pattern,
            placement=placement,
            line_width=line_width,
            opacity=opacity,
        )
