"""Automated metric monitoring with rolling-average anomaly detection.

Given a daily time series of a business metric, flag the days where the value
departs from its local baseline by more than a configurable number of standard
deviations. The baseline is a trailing rolling average, and the threshold is
derived from the spread of the residuals (metric minus rolling average), so it
scales to how noisy the metric actually is: a jittery metric needs a bigger jump
to flag than a quiet one. The method targets point anomalies against a locally
stable baseline; a sustained level shift will flag until the rolling window
catches up, which is the expected behavior for a detector this simple.

Run:
    python anomaly_monitor.py --input sample_data/metrics.csv --window 7 --sensitivity 2.0
"""

from __future__ import annotations

import argparse
import logging
from pathlib import Path

import pandas as pd

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s"
)
logger = logging.getLogger(__name__)

DEFAULT_INPUT = Path(__file__).resolve().parent / "sample_data" / "metrics.csv"


def load_metrics(path: str | Path) -> pd.DataFrame:
    """Load a metrics CSV with ``date`` and ``metric`` columns, sorted by date."""
    frame = pd.read_csv(path, parse_dates=["date"])
    missing = {"date", "metric"} - set(frame.columns)
    if missing:
        raise ValueError(f"input is missing required column(s): {sorted(missing)}")
    return frame.sort_values("date").reset_index(drop=True)


def compute_rolling_stats(frame: pd.DataFrame, window: int = 7) -> pd.DataFrame:
    """Add a trailing rolling average and the residual (metric minus average)."""
    result = frame.copy()
    result["rolling_avg"] = result["metric"].rolling(window=window, min_periods=1).mean()
    result["residual"] = result["metric"] - result["rolling_avg"]
    return result


def detect_deviations(frame: pd.DataFrame, sensitivity: float = 2.0) -> pd.DataFrame:
    """Return the rows whose residual exceeds ``sensitivity`` residual std devs.

    The threshold uses the standard deviation of the residuals, not of the raw
    metric. A flat series has zero residual spread and therefore no anomalies.
    """
    residual_std = frame["residual"].std()
    if pd.isna(residual_std) or residual_std == 0:
        return frame.iloc[0:0].copy()
    threshold = sensitivity * residual_std
    flagged = frame[frame["residual"].abs() > threshold].copy()
    flagged["threshold"] = round(threshold, 2)
    return flagged


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Flag anomalous days in a metric time series."
    )
    parser.add_argument(
        "--input", type=Path, default=DEFAULT_INPUT, help="metrics CSV path"
    )
    parser.add_argument(
        "--window", type=int, default=7, help="rolling-average window in days"
    )
    parser.add_argument(
        "--sensitivity", type=float, default=2.0, help="residual std-dev multiplier"
    )
    args = parser.parse_args()

    frame = compute_rolling_stats(load_metrics(args.input), window=args.window)
    flagged = detect_deviations(frame, sensitivity=args.sensitivity)

    if flagged.empty:
        logger.info("No significant deviations detected across %d days.", len(frame))
        return

    logger.warning("Detected %d anomalous day(s):", len(flagged))
    for _, row in flagged.iterrows():
        logger.warning(
            "  %s  metric=%.1f  rolling_avg=%.1f  residual=%+.1f",
            row["date"].date(),
            row["metric"],
            row["rolling_avg"],
            row["residual"],
        )


if __name__ == "__main__":
    main()
