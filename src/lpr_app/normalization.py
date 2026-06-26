"""Utilities for normalizing OCR output into license-plate-like candidates."""

from __future__ import annotations

import re

_ALLOWED = re.compile(r"[^A-Z0-9]")
_SPACE = re.compile(r"\s+")


def normalize_plate_text(raw_text: str, *, min_length: int = 2, max_length: int = 10) -> str:
    """Return the strongest plate candidate found in OCR text.

    OCR engines often return whitespace, punctuation, or multiple lines. This function keeps
    alphanumeric characters, uppercases them, and returns the longest plausible token.
    """
    if min_length < 1:
        raise ValueError("min_length must be at least 1")
    if max_length < min_length:
        raise ValueError("max_length must be greater than or equal to min_length")

    compacted = _SPACE.sub(" ", raw_text.upper()).strip()
    tokens = [_ALLOWED.sub("", token) for token in compacted.split(" ")]
    candidates = [token[:max_length] for token in tokens if len(token) >= min_length]

    if candidates:
        return max(candidates, key=lambda value: (len(value), value))

    fallback = _ALLOWED.sub("", compacted)
    return fallback[:max_length]
