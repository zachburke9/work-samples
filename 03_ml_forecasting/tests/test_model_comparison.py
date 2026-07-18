"""Tests for the model comparison benchmark."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from booking_forecast import build_features, generate_bookings
from model_comparison import evaluate_models


def test_all_models_scored() -> None:
    results = evaluate_models(build_features(generate_bookings()))
    assert set(results) == {
        "Seasonal naive",
        "Linear regression",
        "Random forest",
        "Gradient boosting",
    }
    for metrics in results.values():
        assert set(metrics) == {"MAE", "RMSE", "R2"}


def test_a_model_beats_the_naive_baseline() -> None:
    # The point of the benchmark: at least one learned model must earn its
    # complexity by beating "same day last week" on MAE.
    results = evaluate_models(build_features(generate_bookings()))
    baseline = results["Seasonal naive"]["MAE"]
    best_model = min(
        results[name]["MAE"] for name in results if name != "Seasonal naive"
    )
    assert best_model < baseline
