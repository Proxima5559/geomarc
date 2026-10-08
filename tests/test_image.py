from pathlib import Path
import pytest
from PIL import Image

from geomarc.image.watermark import apply_watermark

from geomarc.constants import STYLE_CHOICES


def test_watermark_creates_output(tmp_path: Path):
    input_path = tmp_path / "input.png"
    output_path = tmp_path / "output.png"
    
    image = Image.new("RGB", (800, 600), "gray")
    image.save(input_path)
    
    apply_watermark(
        input_path=input_path,
        output_path=output_path,
        complexity="medium",
        style="line_mesh",
        line_width=2.0,
        opacity=100,
        seed=12345,
        count=5,
        protected_regions=(),
    )
    assert output_path.exists()


@pytest.mark.parametrize("style", STYLE_CHOICES)
def test_watermark_accepts_all_valid_styles(tmp_path: Path, style: str):
    input_path = tmp_path / "input.png"
    output_path = tmp_path / f"output_{style}.png"
    
    image = Image.new("RGB", (400, 300), "gray")
    image.save(input_path)
    
    apply_watermark(
        input_path=input_path,
        output_path=output_path,
        complexity="medium",
        style=style,
        line_width=1.5,
        opacity=120,
        seed=42,
        count=4,
        protected_regions=(),
    )
    assert output_path.exists()


def test_watermark_rejects_invalid_style(tmp_path: Path):
    input_path = tmp_path / "input.png"
    output_path = tmp_path / "output.png"
    
    image = Image.new("RGB", (100, 100), "gray")
    image.save(input_path)
    
    with pytest.raises(ValueError, match="Unknown style: completely_fake_style_123"):
        apply_watermark(
            input_path=input_path,
            output_path=output_path,
            complexity="medium",
            style="completely_fake_style_123",
            line_width=2.0,
            opacity=100,
            seed=12345,
            count=5,
            protected_regions=(),
        )

def test_watermark_preserves_dimensions(tmp_path: Path):
    input_path = tmp_path / "input.png"
    output_path = tmp_path / "output.png"
    
    image = Image.new("RGB", (800, 600), "gray")
    image.save(input_path)
    
    apply_watermark(
        input_path=input_path,
        output_path=output_path,
        complexity="medium",
        style="minimal",
        line_width=2.0,
        opacity=100,
        seed=12345,
        count=5,
        protected_regions=(),
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
        style="dense_geometric",
        line_width=2.0,
        opacity=255,
        seed=12345,
        count=5,
        protected_regions=(),
    )
    
    with Image.open(input_path) as original:
        original_bytes = original.convert("RGBA").tobytes()
    with Image.open(output_path) as result:
        result_bytes = result.convert("RGBA").tobytes()
        
    assert original_bytes != result_bytes


def test_watermark_jpeg_conversion(tmp_path: Path):
    input_path = tmp_path / "input.png"
    output_path = tmp_path / "output.jpg"
    
    image = Image.new("RGB", (400, 300), "white")
    image.save(input_path)
    
    apply_watermark(
        input_path=input_path,
        output_path=output_path,
        complexity="medium",
        style="angular_sharp",
        line_width=2.0,
        opacity=100,
        seed=42,
        count=5,
        protected_regions=(),
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
            complexity="medium",
            style="line_mesh",
            line_width=2.0,
            opacity=300,
            seed=12345,
            count=5,
            protected_regions=(),
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
            complexity="medium",
            style="line_mesh",
            line_width=0.0,
            opacity=100,
            seed=12345,
            count=5,
            protected_regions=(),
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
            complexity="medium",
            style="line_mesh",
            line_width=2.0,
            opacity=100,
            seed=12345,
            count=count,
            protected_regions=(),
        )


def test_watermark_raises_file_not_found(tmp_path: Path):
    input_path = tmp_path / "nonexistent.png"
    output_path = tmp_path / "output.png"
    
    with pytest.raises(FileNotFoundError, match="Input file not found"):
        apply_watermark(
            input_path=input_path,
            output_path=output_path,
            complexity="medium",
            style="line_mesh",
            line_width=2.0,
            opacity=100,
            seed=12345,
            count=5,
            protected_regions=(),
        )


def test_watermark_raises_on_corrupted_image(tmp_path: Path):
    input_path = tmp_path / "corrupted.png"
    output_path = tmp_path / "output.png"
    
    input_path.write_text("not an image")
    
    with pytest.raises(ValueError, match="Invalid or corrupted image file"):
        apply_watermark(
            input_path=input_path,
            output_path=output_path,
            complexity="medium",
            style="line_mesh",
            line_width=2.0,
            opacity=100,
            seed=12345,
            count=5,
            protected_regions=(),
        )
