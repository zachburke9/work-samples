"""Tests for the forecasting feature engineering and data generation."""

import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from booking_forecast import FEATURE_COLUMNS, build_features, generate_bookings


def test_generate_is_reproducible() -> None:
    pd.testing.assert_frame_equal(
        generate_bookings(50, seed=7), generate_bookings(50, seed=7)
    )


def test_build_features_creates_columns_and_drops_lag_window() -> None:
    raw = generate_bookings(30, seed=1)
    feats = build_features(raw)
    for column in FEATURE_COLUMNS:
        assert column in feats.columns
    # The first 7 rows lack a full lag_7 / rolling_7 window and are dropped.
    assert len(feats) == len(raw) - 7
    assert not feats[FEATURE_COLUMNS].isnull().any().any()


def test_lag_features_match_shifted_values() -> None:
    frame = pd.DataFrame(
        {
            "date": pd.date_range("2023-01-01", periods=10),
            "bookings": [10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
            "is_promo": [0] * 10,
        }
    )
    first = build_features(frame).iloc[0]  # corresponds to original index 7
    assert first["bookings"] == 17
    assert first["lag_1"] == 16
    assert first["lag_7"] == 10
    assert first["rolling_7"] == 13  # mean of bookings[0:7] = mean(10..16)
