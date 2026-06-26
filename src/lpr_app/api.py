"""FastAPI application for license plate recognition."""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel

from lpr_app.pipeline import Recognizer

app = FastAPI(title="LPR App", version="0.1.0")
recognizer = Recognizer()


class RecognitionResponse(BaseModel):
    """API response model for plate recognition."""

    plate: str
    raw_text: str


@app.get("/health")
def health() -> dict[str, str]:
    """Return service health for load balancers and deployment checks."""
    return {"status": "ok"}


@app.post("/recognize", response_model=RecognitionResponse)
async def recognize_plate(file: Annotated[UploadFile, File(...)]) -> RecognitionResponse:
    """Recognize a license plate from an uploaded image."""
    suffix = Path(file.filename or "upload.jpg").suffix or ".jpg"
    try:
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=True) as temp_file:
            temp_file.write(await file.read())
            temp_file.flush()
            result = recognizer.recognize(temp_file.name)
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return RecognitionResponse(plate=result.plate, raw_text=result.raw_text)
