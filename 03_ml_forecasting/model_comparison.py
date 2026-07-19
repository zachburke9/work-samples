"""Benchmark several forecasting approaches on one time-ordered split.

Reuses the data and features from ``booking_forecast``, then compares a seasonal
naive baseline against linear regression, a random forest, and gradient boosting
on identical train and test data. Reporting a baseline alongside the models is
the honest way to show a model earns its complexity: a method that cannot beat
"same day last week" is not worth shipping, however sophisticated it looks.

Run:  python model_comparison.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # headless backend: render to file, never open a window

import matplotlib.pyplot as plt  # noqa: E402  (must follow backend selection)
import numpy as np  # noqa: E402
from booking_forecast import (  # noqa: E402
    FEATURE_COLUMNS,
    SEED,
    build_features,
    generate_bookings,
)
from sklearn.ensemble import (  # noqa: E402
    GradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.linear_model import LinearRegression  # noqa: E402
from sklearn.metrics import (  # noqa: E402
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)

OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"


def _split(features):
    """Time-ordered 80/20 split, matching booking_forecast."""
    cut = int(len(features) * 0.8)
    train, test = features.iloc[:cut], features.iloc[cut:]
    return (
        train[FEATURE_COLUMNS],
        train["bookings"],
        test[FEATURE_COLUMNS],
        test["bookings"],
    )


def _score(y_true, y_pred) -> dict[str, float]:
    return {
        "MAE": mean_absolute_error(y_true, y_pred),
        "RMSE": float(np.sqrt(mean_squared_error(y_true, y_pred))),
        "R2": r2_score(y_true, y_pred),
    }


def evaluate_models(features) -> dict[str, dict[str, float]]:
    """Score a seasonal-naive baseline and three models on the same split."""
    x_train, y_train, x_test, y_test = _split(features)
    results: dict[str, dict[str, float]] = {}

    # Baseline: predict last week's same-day value (the lag_7 feature).
    results["Seasonal naive"] = _score(y_test, x_test["lag_7"])

    models = {
        "Linear regression": LinearRegression(),
        "Random forest": RandomForestRegressor(n_estimators=200, random_state=SEED),
        "Gradient boosting": GradientBoostingRegressor(random_state=SEED),
    }
    for name, model in models.items():
        model.fit(x_train, y_train)
        results[name] = _score(y_test, model.predict(x_test))
    return results


def plot_comparison(results: dict[str, dict[str, float]], path: Path) -> None:
    """Save a bar chart of MAE by model, with the baseline greyed for contrast."""
    path.parent.mkdir(parents=True, exist_ok=True)
    names = list(results)
    maes = [results[name]["MAE"] for name in names]
    colors = ["#9aa5b1"] + ["#1f4e79"] * (len(names) - 1)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    bars = ax.bar(names, maes, color=colors)
    ax.set_ylabel("MAE in bookings (lower is better)")
    ax.set_title("Forecast model comparison on the held-out test period")
    ax.bar_label(bars, fmt="%.1f", padding=3)
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)


def main() -> None:
    results = evaluate_models(build_features(generate_bookings()))

    print(f"{'Model':<20}{'MAE':>8}{'RMSE':>8}{'R2':>8}")
    print("-" * 44)
    for name, metrics in results.items():
        print(
            f"{name:<20}{metrics['MAE']:>8.2f}"
            f"{metrics['RMSE']:>8.2f}{metrics['R2']:>8.3f}"
        )

    chart_path = OUTPUT_DIR / "model_comparison.png"
    plot_comparison(results, chart_path)
    print(f"\nSaved chart to {chart_path}")


if __name__ == "__main__":
    main()
