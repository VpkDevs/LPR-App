# LPR App

A lightweight, testable license plate recognition (LPR) service. The project provides:

- A reusable Python recognition pipeline.
- Optional OpenCV + Tesseract OCR integration.
- A FastAPI HTTP service for image uploads.
- A CLI for local batch-style use.
- Unit tests and CI-ready quality checks.

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev,vision]'
pytest
```

If you only want to run tests without native OCR dependencies, install `.[dev]`.

## CLI usage

```bash
lpr-app ./examples/plate.jpg --json
```

## API usage

```bash
uvicorn lpr_app.api:app --reload
curl -F "file=@./examples/plate.jpg" http://127.0.0.1:8000/recognize
```

Health checks are available at `GET /health`.

## Architecture

The recognition flow is intentionally small and testable:

1. Validate that the input image path exists.
2. Extract raw OCR text with an injectable OCR engine.
3. Normalize OCR noise into a plate-like alphanumeric candidate.
4. Return a structured `RecognitionResult`.

The default OCR engine uses OpenCV preprocessing and pytesseract. Tests inject a stub OCR engine so the core pipeline remains deterministic and fast.

## Development

```bash
pip install -e '.[dev]'
ruff check .
pytest
```

See [`docs/ROADMAP.md`](docs/ROADMAP.md) for recommended next milestones.
