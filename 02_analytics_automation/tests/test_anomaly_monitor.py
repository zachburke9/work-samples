"""Tests for the anomaly monitor's detection logic."""

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from anomaly_monitor import compute_rolling_stats, detect_deviations, load_metrics


def _series(values: list[float]) -> pd.DataFrame:
    dates = pd.date_range("2024-01-01", periods=len(values))
    return pd.DataFrame({"date": dates, "metric": values})


def test_flags_single_isolated_spike() -> None:
    frame = compute_rolling_stats(_series([100] * 15 + [400]), window=7)
    flagged = detect_deviations(frame, sensitivity=2.0)
    assert len(flagged) == 1
    assert flagged.iloc[0]["metric"] == 400


def test_flat_series_has_no_anomalies() -> None:
    frame = compute_rolling_stats(_series([100] * 20), window=7)
    assert detect_deviations(frame, sensitivity=2.0).empty


def test_higher_sensitivity_flags_fewer() -> None:
    # The same spike should stop flagging once the threshold is raised far enough.
    frame = compute_rolling_stats(_series([100] * 15 + [400]), window=7)
    assert len(detect_deviations(frame, sensitivity=2.0)) == 1
    assert detect_deviations(frame, sensitivity=50.0).empty


def test_load_metrics_reads_and_sorts(tmp_path: Path) -> None:
    csv = tmp_path / "m.csv"
    csv.write_text("date,metric\n2024-01-02,110\n2024-01-01,100\n")
    frame = load_metrics(csv)
    assert list(frame["metric"]) == [100, 110]  # sorted by date
