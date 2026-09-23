import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch

from geomarc.pdf.watermark import (
    apply_watermark,
    _get_page_numbers,
    _generate_seed,
)


@pytest.mark.parametrize(
    "page_count, interval, expected",
    [
        (5, None, (0, 1, 2, 3, 4)),
        (5, 2, (1, 3)),
        (5, 1, (0, 1, 2, 3, 4)),
        (0, 2, ()),
        (5, 10, ()),
    ],
)
def test_get_page_numbers(page_count, interval, expected):
    assert _get_page_numbers(page_count, interval) == expected


def test_generate_seed():
    assert _generate_seed(None, "page", "file.pdf", 0) is None
    
    seed1 = _generate_seed(42, "page", "file.pdf", 0)
    seed2 = _generate_seed(42, "page", "file.pdf", 0)
    seed3 = _generate_seed(42, "page", "file.pdf", 1)
    
    assert isinstance(seed1, int)
    assert seed1 == seed2
    assert seed1 != seed3


def test_apply_watermark_file_not_found(tmp_path):
    non_existent = tmp_path / "missing.pdf"
    with pytest.raises(FileNotFoundError):
        apply_watermark(non_existent, tmp_path / "output.pdf")


@pytest.mark.parametrize(
    "kwargs, match_msg",
    [
        ({"line_width": 0}, "Line width must be greater than 0"),
        ({"opacity": 300}, "Opacity must be between 0 and 255"),
        ({"count": 2}, "Count must be between 3 and 10"),
        ({"interval": 0}, "Interval must be greater than 0"),
    ],
)
def test_apply_watermark_validation_errors(tmp_path, kwargs, match_msg):
    pdf_path = tmp_path / "test.pdf"
    pdf_path.write_bytes(b"%PDF-1.4 dummy")
    
    with pytest.raises(ValueError, match=match_msg):
        apply_watermark(pdf_path, tmp_path / "out.pdf", **kwargs)


@patch("geomarc.pdf.watermark.pymupdf.open")
@patch("geomarc.pdf.watermark.generate_placements")
@patch("geomarc.pdf.watermark.generate_pattern")
@patch("geomarc.pdf.watermark.render_pattern")
def test_apply_watermark_success(
    mock_render, mock_gen_placements, mock_pymupdf_open, tmp_path
):
    mock_page = MagicMock()
    mock_rect = MagicMock()
    mock_rect.width = 600.0
    mock_rect.height = 800.0
    mock_page.rect = mock_rect

    mock_doc = MagicMock()
    mock_doc.__len__.return_value = 2
    mock_doc.__getitem__.return_value = mock_page
    mock_pymupdf_open.return_value = mock_doc

    mock_placement = MagicMock()
    mock_placement.width = 100.0
    mock_placement.height = 100.0
    mock_gen_placements.return_value = [mock_placement]

    input_pdf = tmp_path / "input.pdf"
    input_pdf.write_bytes(b"%PDF-1.4 dummy")
    output_pdf = tmp_path / "output.pdf"

    apply_watermark(input_pdf, output_pdf, count=5, seed=123)

    mock_pymupdf_open.assert_called_once_with(input_pdf)
    mock_render.assert_called()  
    mock_doc.save.assert_called_once()
    mock_doc.close.assert_called_once()