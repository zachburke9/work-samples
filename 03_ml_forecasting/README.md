# ML Forecasting

A reproducible daily-bookings forecast. It generates a realistic synthetic series
(trend, weekly seasonality, promotion lift, noise), engineers calendar and lag
features, and trains a random-forest regressor, evaluating in a way that respects
time order.

## Contents

- `booking_forecast.py` builds the data, engineers features, trains the model, and
  writes the chart. Everything is seeded, so the run is reproducible offline.
- `outputs/forecast_vs_actual.png` is the chart the script produces.
- `tests/` covers the feature engineering and reproducibility.

## Run it

```bash
python booking_forecast.py
```

## Results

The model trains on the earliest 80 percent of days and is scored on the most
recent 20 percent it has never seen, plus a 5-fold rolling time-series
cross-validation. On the held-out period:

| Metric | Value |
|--------|-------|
| MAE | 8.13 bookings |
| RMSE | 9.92 bookings |
| R-squared | 0.654 |
| Time-series CV MAE | 5.76 bookings |

The run is seeded, so these figures are deterministic for a given environment;
expect small drift across scikit-learn or numpy versions.

![Daily bookings: actual vs predicted](outputs/forecast_vs_actual.png)

The predictions track the weekly rhythm and promotion spikes. The model
under-shoots the very highest peaks, which is expected: a random forest cannot
predict above the range it was trained on. Feature importances line up with how
the data was built, with day-of-week seasonality and the promotion flag carrying
most of the signal.

## Why the evaluation is set up this way

Forecasting is a time-ordered problem, so a random train/test shuffle would let
the model peek at the future and report a score it could never earn in practice.
Training on the past and scoring on the most recent unseen days is the honest
test. The lag features (yesterday, same day last week, trailing 7-day average)
are what let a tree model track a moving level without extrapolating.
