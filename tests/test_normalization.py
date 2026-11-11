import pytest

from lpr_app.normalization import normalize_plate_text


def test_normalize_plate_text_prefers_longest_candidate() -> None:
    assert normalize_plate_text("\n ca 7abc123 !!!\n") == "7ABC123"


def test_normalize_plate_text_compacts_when_no_token_is_long_enough() -> None:
    assert normalize_plate_text("a - b", min_length=4) == "AB"


def test_normalize_plate_text_validates_lengths() -> None:
    with pytest.raises(ValueError, match="min_length"):
        normalize_plate_text("abc", min_length=0)

    with pytest.raises(ValueError, match="max_length"):
        normalize_plate_text("abc", min_length=4, max_length=3)
