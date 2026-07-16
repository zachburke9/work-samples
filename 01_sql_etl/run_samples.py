"""Run the SQL samples in this folder against the CSV fixtures in sample_data/.

Loads every fixture CSV in ``sample_data/`` into an in-memory SQLite database
(one table per file, named after the file stem), executes each ``.sql`` file in
``sql/``, writes each result to ``sample_data/<query_name>_output.csv``, and
prints a short preview so the transformation is legible without a warehouse.

Standard library only (csv, sqlite3, pathlib). Run:  python run_samples.py
"""

from __future__ import annotations

import csv
import sqlite3
from pathlib import Path

HERE = Path(__file__).resolve().parent
SAMPLE_DIR = HERE / "sample_data"
SQL_DIR = HERE / "sql"


def _coerce(value: str) -> object | None:
    """Convert a CSV cell to int/float/None where possible, else keep the string."""
    if value == "":
        return None
    for cast in (int, float):
        try:
            return cast(value)
        except ValueError:
            continue
    return value


def load_fixtures(conn: sqlite3.Connection) -> None:
    """Create and populate one table per fixture CSV (skipping generated outputs)."""
    for csv_path in sorted(SAMPLE_DIR.glob("*.csv")):
        if csv_path.stem.endswith("_output"):
            continue
        with csv_path.open(newline="") as handle:
            reader = csv.reader(handle)
            header = next(reader)
            rows = [[_coerce(cell) for cell in row] for row in reader]
        columns = ", ".join(f'"{name}"' for name in header)
        placeholders = ", ".join("?" for _ in header)
        conn.execute(f'CREATE TABLE "{csv_path.stem}" ({columns})')
        conn.executemany(
            f'INSERT INTO "{csv_path.stem}" VALUES ({placeholders})', rows
        )


def run_query(conn: sqlite3.Connection, sql_path: Path) -> tuple[list[str], list[tuple]]:
    """Execute a single-statement .sql file and return its columns and rows."""
    cursor = conn.execute(sql_path.read_text())
    columns = [description[0] for description in cursor.description]
    return columns, cursor.fetchall()


def main() -> None:
    conn = sqlite3.connect(":memory:")
    load_fixtures(conn)
    for sql_path in sorted(SQL_DIR.glob("*.sql")):
        columns, rows = run_query(conn, sql_path)
        out_path = SAMPLE_DIR / f"{sql_path.stem}_output.csv"
        with out_path.open("w", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(columns)
            writer.writerows(rows)
        print(f"\n{sql_path.name}  ->  {out_path.name}  ({len(rows)} rows)")
        print(" | ".join(columns))
        for row in rows[:8]:
            print(" | ".join("" if value is None else str(value) for value in row))
    conn.close()


if __name__ == "__main__":
    main()
