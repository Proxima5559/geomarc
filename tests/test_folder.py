from pathlib import Path
import pytest
from PIL import Image

from geomarc.image.folder import process_folder


@pytest.fixture
def sample_folder(tmp_path: Path) -> Path:
    input_dir = tmp_path / "input"
    input_dir.mkdir()

    img_path_1 = input_dir / "test1.png"
    Image.new("RGB", (100, 100), color="red").save(img_path_1)

    img_path_2 = input_dir / "test2.jpg"
    Image.new("RGB", (100, 100), color="blue").save(img_path_2)

    bad_file = input_dir / "data.xlsx"
    bad_file.write_text("some excel dummy data")

    return input_dir


def test_process_folder_success_skip(sample_folder: Path, tmp_path: Path) -> None:
    output_dir = tmp_path / "output"

    processed, skipped = process_folder(
        input_dir=sample_folder,
        output_dir=output_dir,
        complexity="low",
        on_unsupported="skip",
    )

    assert processed == 2
    assert skipped == 1

    assert (output_dir / "test1.png").exists()
    assert (output_dir / "test2.jpg").exists()
    assert not (output_dir / "data.xlsx").exists()


def test_process_folder_fail_on_unsupported(sample_folder: Path, tmp_path: Path) -> None:
    output_dir = tmp_path / "output_fail"

    with pytest.raises(ValueError, match="Unsupported file format"):
        process_folder(
            input_dir=sample_folder,
            output_dir=output_dir,
            complexity="low",
            on_unsupported="fail",
        )


def test_process_folder_invalid_directory(tmp_path: Path) -> None:
    non_existent = tmp_path / "ghost_dir"
    output_dir = tmp_path / "out"

    with pytest.raises(NotADirectoryError, match="Input directory not found"):
        process_folder(
            input_dir=non_existent,
            output_dir=output_dir,
        )


@pytest.mark.parametrize("count", [2, 11])
def test_process_folder_invalid_count(sample_folder: Path, tmp_path: Path, count: int) -> None:
    output_dir = tmp_path / "output_count"

    with pytest.raises(ValueError, match="Count must be between 3 and 10"):
        process_folder(
            input_dir=sample_folder,
            output_dir=output_dir,
            count=count,
        )


def test_process_folder_invalid_on_unsupported(sample_folder: Path, tmp_path: Path) -> None:
    output_dir = tmp_path / "output_unsupported"

    with pytest.raises(ValueError, match="on_unsupported must be 'skip' or 'fail'"):
        process_folder(
            input_dir=sample_folder,
            output_dir=output_dir,
            on_unsupported="invalid_mode",
        )


def test_process_folder_corrupted_image_skip(tmp_path: Path) -> None:
    input_dir = tmp_path / "input_corrupt"
    input_dir.mkdir()

    corrupt_file = input_dir / "corrupt.png"
    corrupt_file.write_text("not an image")

    output_dir = tmp_path / "output_corrupt"

    processed, skipped = process_folder(
        input_dir=input_dir,
        output_dir=output_dir,
        on_unsupported="skip",
    )

    assert processed == 0
    assert skipped == 1