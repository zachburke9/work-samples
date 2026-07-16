"""Reusable data-quality checks for analyst onboarding.

A small, importable toolkit of the validation checks every dataset should pass
before it reaches a report: missing values, duplicate identifiers, and
out-of-range numbers. Each check returns the offending rows as a DataFrame
rather than printing, so the checks compose, can be asserted on in tests, and can
gate a pipeline. This is the reference module behind the exercises in
``exercises.md``.

Run the demo:  python data_quality.py
"""

from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd


def find_missing_values(frame: pd.DataFrame) -> pd.DataFrame:
    """Return the rows that have a null in any column."""
    return frame[frame.isnull().any(axis=1)]


def find_duplicate_ids(frame: pd.DataFrame, id_column: str) -> pd.DataFrame:
    """Return every row that shares an ``id_column`` value with another row."""
    return frame[frame.duplicated(id_column, keep=False)]


def find_out_of_range(
    frame: pd.DataFrame, column: str, low: float, high: float
) -> pd.DataFrame:
    """Return the rows whose ``column`` value falls outside the inclusive bounds."""
    return frame[(frame[column] < low) | (frame[column] > high)]


@dataclass
class ValidationReport:
    """A summary of one validation pass: the offending rows plus roll-up counts."""

    missing: pd.DataFrame
    duplicate_ids: pd.DataFrame
    out_of_range: dict[str, pd.DataFrame] = field(default_factory=dict)

    @property
    def is_clean(self) -> bool:
        """True when every check passed with no offending rows."""
        return (
            self.missing.empty
            and self.duplicate_ids.empty
            and all(rows.empty for rows in self.out_of_range.values())
        )

    def summary(self) -> dict[str, int]:
        """Return a flat {check_name: offending_row_count} mapping."""
        counts = {
            "missing_value_rows": len(self.missing),
            "duplicate_id_rows": len(self.duplicate_ids),
        }
        for column, rows in self.out_of_range.items():
            counts[f"out_of_range_{column}"] = len(rows)
        return counts


def validate(
    frame: pd.DataFrame,
    id_column: str,
    range_checks: dict[str, tuple[float, float]],
) -> ValidationReport:
    """Run all checks and return a report.

    ``range_checks`` maps a column name to an ``(low, high)`` inclusive bound.
    """
    return ValidationReport(
        missing=find_missing_values(frame),
        duplicate_ids=find_duplicate_ids(frame, id_column),
        out_of_range={
            column: find_out_of_range(frame, column, low, high)
            for column, (low, high) in range_checks.items()
        },
    )


def _demo() -> None:
    frame = pd.DataFrame(
        {
            "id": [1, 2, 3, 4, 5, 5],
            "age": [25, 37, 19, 52, -1, 44],
            "name": ["Alice", "Bob", None, "Diana", "Ethan", "Frank"],
        }
    )
    report = validate(frame, id_column="id", range_checks={"age": (0, 120)})
    print("Validation summary:")
    for check, count in report.summary().items():
        print(f"  {check}: {count}")
    print(f"\nClean dataset: {report.is_clean}")


if __name__ == "__main__":
    _demo()
