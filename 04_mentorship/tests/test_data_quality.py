"""Tests for the reusable data-quality checks."""

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from data_quality import (
    find_duplicate_ids,
    find_missing_values,
    find_out_of_range,
    validate,
)

SAMPLE = pd.DataFrame(
    {
        "id": [1, 2, 3, 4, 5, 5],
        "age": [25, 37, 19, 52, -1, 44],
        "name": ["Alice", "Bob", None, "Diana", "Ethan", "Frank"],
    }
)


def test_find_missing_values() -> None:
    rows = find_missing_values(SAMPLE)
    assert len(rows) == 1
    assert rows.iloc[0]["id"] == 3


def test_find_duplicate_ids() -> None:
    rows = find_duplicate_ids(SAMPLE, "id")
    assert len(rows) == 2
    assert set(rows["id"]) == {5}


def test_find_out_of_range() -> None:
    rows = find_out_of_range(SAMPLE, "age", 0, 120)
    assert len(rows) == 1
    assert rows.iloc[0]["age"] == -1


def test_validate_report_counts() -> None:
    report = validate(SAMPLE, "id", {"age": (0, 120)})
    assert not report.is_clean
    summary = report.summary()
    assert summary["missing_value_rows"] == 1
    assert summary["duplicate_id_rows"] == 2
    assert summary["out_of_range_age"] == 1


def test_clean_frame_is_clean() -> None:
    clean = pd.DataFrame({"id": [1, 2], "age": [30, 40], "name": ["A", "B"]})
    assert validate(clean, "id", {"age": (0, 120)}).is_clean
