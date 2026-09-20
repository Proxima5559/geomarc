from pathlib import Path
import pytest
from PIL import Image

from geomarc.image.watermark import apply_watermark


def test_watermark_creates_output(tmp_path: Path):
    input_path = tmp_path / "input.png"
    output_path = tmp_path / "output.png"

    image = Image.new("RGB", (800, 600), "gray")
    image.save(input_path)

    apply_watermark(
        input_path=input_path,
        output_path=output_path,
        complexity="medium",
        line_width=2,
        opacity=100,
        seed=12345,
    )

    assert output_path.exists()


def test_watermark_preserves_dimensions(tmp_path: Path):
    input_path = tmp_path / "input.png"
    output_path = tmp_path / "output.png"

    image = Image.new("RGB", (800, 600), "gray")
    image.save(input_path)

    apply_watermark(
        input_path=input_path,
        output_path=output_path,
        seed=12345,
    )

    with Image.open(output_path) as result:
        assert result.size == (800, 600)


def test_watermark_changes_image(tmp_path: Path):
    input_path = tmp_path / "input.png"
    output_path = tmp_path / "output.png"

    image = Image.new("RGB", (800, 600), "gray")
    image.save(input_path)

    apply_watermark(
        input_path=input_path,
        output_path=output_path,
        complexity="high",
        line_width=2,
        opacity=255,
        seed=12345,
    )

    with Image.open(input_path) as original:
        original_pixels = list(original.convert("RGBA").get_flattened_data())

    with Image.open(output_path) as result:
        result_pixels = list(result.convert("RGBA").get_flattened_data())

    assert original_pixels != result_pixels


def test_watermark_jpeg_conversion(tmp_path: Path):
    input_path = tmp_path / "input.png"
    output_path = tmp_path / "output.jpg"

    image = Image.new("RGB", (400, 300), "white")
    image.save(input_path)

    apply_watermark(
        input_path=input_path,
        output_path=output_path,
        seed=42,
    )

    assert output_path.exists()
    with Image.open(output_path) as result:
        assert result.mode == "RGB"
        assert result.size == (400, 300)


def test_watermark_rejects_invalid_opacity(tmp_path: Path):
    input_path = tmp_path / "input.png"
    output_path = tmp_path / "output.png"

    image = Image.new("RGB", (100, 100), "gray")
    image.save(input_path)

    with pytest.raises(ValueError, match="Opacity must be between 0 and 255"):
        apply_watermark(
            input_path=input_path,
            output_path=output_path,
            opacity=300,
        )


def test_watermark_rejects_invalid_line_width(tmp_path: Path):
    input_path = tmp_path / "input.png"
    output_path = tmp_path / "output.png"

    image = Image.new("RGB", (100, 100), "gray")
    image.save(input_path)

    with pytest.raises(ValueError, match="Line width must be greater than 0"):
        apply_watermark(
            input_path=input_path,
            output_path=output_path,
            line_width=0,
        )


@pytest.mark.parametrize("count", [2, 11])
def test_watermark_rejects_invalid_count(tmp_path: Path, count: int):
    input_path = tmp_path / "input.png"
    output_path = tmp_path / "output.png"

    image = Image.new("RGB", (100, 100), "gray")
    image.save(input_path)

    with pytest.raises(ValueError, match="Count must be between 3 and 10"):
        apply_watermark(
            input_path=input_path,
            output_path=output_path,
            count=count,
        )


def test_watermark_raises_file_not_found(tmp_path: Path):
    input_path = tmp_path / "nonexistent.png"
    output_path = tmp_path / "output.png"

    with pytest.raises(FileNotFoundError, match="Input file not found"):
        apply_watermark(
            input_path=input_path,
            output_path=output_path,
        )


def test_watermark_raises_on_corrupted_image(tmp_path: Path):
    input_path = tmp_path / "corrupted.png"
    output_path = tmp_path / "output.png"

    input_path.write_text("not an image")

    with pytest.raises(ValueError, match="Invalid or corrupted image file"):
        apply_watermark(
            input_path=input_path,
            output_path=output_path,
        )