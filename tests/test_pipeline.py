from pathlib import Path

import pytest

from lpr_app.pipeline import Recognizer


class StubOcrEngine:
    def __init__(self, text: str) -> None:
        self.text = text
        self.seen_path: Path | None = None

    def read_text(self, image_path: Path) -> str:
        self.seen_path = image_path
        return self.text


def test_recognizer_returns_structured_result(tmp_path: Path) -> None:
    image = tmp_path / "plate.jpg"
    image.write_bytes(b"not a real image; OCR is stubbed")
    engine = StubOcrEngine("ny abc-1234")

    result = Recognizer(engine).recognize(image)

    assert result.plate == "ABC1234"
    assert result.raw_text == "ny abc-1234"
    assert result.image_path == image
    assert engine.seen_path == image


def test_recognizer_requires_existing_file(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        Recognizer(StubOcrEngine("abc")).recognize(tmp_path / "missing.jpg")
