"""Recognition pipeline with optional OpenCV/Tesseract integrations."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Protocol

from lpr_app.normalization import normalize_plate_text


class OcrEngine(Protocol):
    """Protocol implemented by OCR backends."""

    def read_text(self, image_path: Path) -> str:
        """Extract text from an image path."""


@dataclass(frozen=True)
class RecognitionResult:
    """Structured output returned by the recognizer."""

    plate: str
    raw_text: str
    image_path: Path


class TesseractOcrEngine:
    """OCR backend using pytesseract and optional OpenCV preprocessing."""

    def read_text(self, image_path: Path) -> str:
        try:
            import cv2
            import pytesseract
        except ImportError as exc:  # pragma: no cover - exercised only without optional deps
            raise RuntimeError(
                "Install optional vision dependencies with `pip install 'lpr-app[vision]'`."
            ) from exc

        image = cv2.imread(str(image_path))
        if image is None:
            raise ValueError(f"Unable to read image: {image_path}")

        grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        filtered = cv2.bilateralFilter(grayscale, 11, 17, 17)
        thresholded = cv2.adaptiveThreshold(
            filtered,
            255,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            31,
            2,
        )
        return pytesseract.image_to_string(
            thresholded,
            config="--psm 7 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789",
        )


class Recognizer:
    """Coordinates file validation, OCR, and plate text normalization."""

    def __init__(self, ocr_engine: OcrEngine | None = None) -> None:
        self._ocr_engine = ocr_engine or TesseractOcrEngine()

    def recognize(self, image_path: str | Path) -> RecognitionResult:
        path = Path(image_path)
        if not path.exists():
            raise FileNotFoundError(f"Image does not exist: {path}")
        if not path.is_file():
            raise ValueError(f"Image path is not a file: {path}")

        raw_text = self._ocr_engine.read_text(path)
        plate = normalize_plate_text(raw_text)
        return RecognitionResult(plate=plate, raw_text=raw_text, image_path=path)
