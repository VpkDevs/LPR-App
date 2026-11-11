"""Command-line interface for the LPR app."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from lpr_app.pipeline import Recognizer


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Recognize license plate text from an image.")
    parser.add_argument("image", type=Path, help="Path to the image to process")
    parser.add_argument("--json", action="store_true", help="Emit structured JSON output")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    result = Recognizer().recognize(args.image)
    if args.json:
        print(json.dumps({"plate": result.plate, "raw_text": result.raw_text}))
    else:
        print(result.plate)
