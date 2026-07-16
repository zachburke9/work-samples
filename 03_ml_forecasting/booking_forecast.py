"""Daily booking forecasting with engineered calendar and lag features.

Generates a realistic synthetic bookings series (slow trend + weekly seasonality
+ promotion lift + noise), engineers calendar and lag features, and trains a
random-forest regressor to predict daily bookings. Evaluation respects time
order: the model trains on the earliest 80 percent of days and is scored on the
most recent 20 percent it has never seen, plus a rolling time-series
cross-validation. Produces MAE, RMSE, R-squared, feature importances, and a
predicted-vs-actual chart saved to ``outputs/``.

The data is synthetic and seeded, so the run is fully reproducible offline with
no database or network access.

Run:  python booking_forecast.py
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # headless backend: render to file, never open a window

import matplotlib.pyplot as plt  # noqa: E402  (must follow backend selection)
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from sklearn.ensemble import RandomForestRegressor  # noqa: E402
from sklearn.metrics import (  # noqa: E402
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)
from sklearn.model_selection import TimeSeriesSplit, cross_val_score  # noqa: E402

SEED = 42
OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"
FEATURE_COLUMNS = ["day_of_week", "month", "is_promo", "lag_1", "lag_7", "rolling_7"]


def generate_bookings(n_days: int = 400, seed: int = SEED) -> pd.DataFrame:
    """Create a synthetic daily bookings series with realistic structure."""
    rng = np.random.default_rng(seed)
    dates = pd.date_range("2023-01-01", periods=n_days, freq="D")
    day_of_week = dates.dayofweek.to_numpy()

    trend = np.linspace(100, 115, n_days)              # mild growth over time
    weekly = 15 * np.sin(2 * np.pi * day_of_week / 7)  # weekday/weekend shape
    is_promo = rng.binomial(1, 0.15, n_days)           # ~15% of days run a promo
    promo_lift = 25 * is_promo
    noise = rng.normal(0, 5, n_days)

    bookings = np.clip(trend + weekly + promo_lift + noise, 0, None).round()
    return pd.DataFrame({"date": dates, "bookings": bookings, "is_promo": is_promo})


def build_features(frame: pd.DataFrame) -> pd.DataFrame:
    """Add calendar and lag features, then drop rows without a full lag window."""
    result = frame.copy()
    result["day_of_week"] = result["date"].dt.dayofweek
    result["month"] = result["date"].dt.month
    result["lag_1"] = result["bookings"].shift(1)
    result["lag_7"] = result["bookings"].shift(7)
    result["rolling_7"] = result["bookings"].shift(1).rolling(7).mean()
    return result.dropna().reset_index(drop=True)


def train_and_evaluate(features: pd.DataFrame) -> dict:
    """Train a random forest with a time-ordered split; return metrics and model."""
    split = int(len(features) * 0.8)
    train, test = features.iloc[:split], features.iloc[split:]

    x_train, y_train = train[FEATURE_COLUMNS], train["bookings"]
    x_test, y_test = test[FEATURE_COLUMNS], test["bookings"]

    model = RandomForestRegressor(n_estimators=200, random_state=SEED)
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)

    cv_mae = -cross_val_score(
        model,
        features[FEATURE_COLUMNS],
        features["bookings"],
        cv=TimeSeriesSplit(n_splits=5),
        scoring="neg_mean_absolute_error",
    ).mean()

    return {
        "model": model,
        "test": test.assign(predicted=predictions),
        "mae": mean_absolute_error(y_test, predictions),
        "rmse": float(np.sqrt(mean_squared_error(y_test, predictions))),
        "r2": r2_score(y_test, predictions),
        "cv_mae": float(cv_mae),
        "importances": dict(
            sorted(
                zip(FEATURE_COLUMNS, model.feature_importances_),
                key=lambda item: item[1],
                reverse=True,
            )
        ),
    }


def plot_forecast(test: pd.DataFrame, path: Path) -> None:
    """Save an actual-vs-predicted line chart for the held-out test window."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(10, 4.5))
    ax.plot(test["date"], test["bookings"], label="Actual", color="#1f4e79", linewidth=1.8)
    ax.plot(
        test["date"],
        test["predicted"],
        label="Predicted",
        color="#c55a11",
        linewidth=1.8,
        linestyle="--",
    )
    ax.set_title("Daily bookings: actual vs predicted (held-out test period)")
    ax.set_xlabel("Date")
    ax.set_ylabel("Bookings")
    ax.legend()
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(path, dpi=120)
    plt.close(fig)


def main() -> None:
    features = build_features(generate_bookings())
    results = train_and_evaluate(features)

    print("Held-out test performance (most recent 20% of days):")
    print(f"  MAE : {results['mae']:.2f} bookings")
    print(f"  RMSE: {results['rmse']:.2f} bookings")
    print(f"  R2  : {results['r2']:.3f}")
    print(f"  Time-series CV MAE (5 folds): {results['cv_mae']:.2f} bookings")
    print("\nFeature importances:")
    for name, importance in results["importances"].items():
        print(f"  {name:12s} {importance:.3f}")

    chart_path = OUTPUT_DIR / "forecast_vs_actual.png"
    plot_forecast(results["test"], chart_path)
    print(f"\nSaved chart to {chart_path}")


if __name__ == "__main__":
    main()
