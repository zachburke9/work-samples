# Analytics Automation

A small monitoring pipeline: detect anomalous days in a business metric, and
alert on them by email. The two pieces are separate so the detector can be tested
and reused without ever touching a mail server.

## Contents

- `anomaly_monitor.py` loads a metric time series, computes a trailing rolling
  average, and flags days whose residual exceeds a configurable number of
  residual standard deviations. Has a CLI, logging, and type hints.
- `email_alerts.py` is an importable notifier. It formats flagged rows into a
  plain-text alert and sends it over SMTP, reading credentials from environment
  variables. Importing it does nothing; nothing sends unless you call it.
- `.env.example` documents the environment variables the notifier reads.
- `sample_data/metrics.csv` is a 30-day series with two planted anomalies.
- `tests/` covers the detection logic.

## Run it

```bash
python anomaly_monitor.py --input sample_data/metrics.csv --window 7 --sensitivity 2.0
```

On the sample data this flags two days: a spike and a dip.

```
WARNING Detected 2 anomalous day(s):
WARNING   2024-01-14  metric=180.0  rolling_avg=120.4  residual=+59.6
WARNING   2024-01-24  metric=40.0   rolling_avg=99.7   residual=-59.7
```

## Sending alerts

Credentials never live in source. Copy `.env.example` to `.env`, fill it in, and
load it into the environment, then chain the notifier onto the monitor:

```python
from anomaly_monitor import load_metrics, compute_rolling_stats, detect_deviations
from email_alerts import format_alert, send_alert, SmtpSettings

flagged = detect_deviations(compute_rolling_stats(load_metrics("sample_data/metrics.csv")))
if not flagged.empty:
    send_alert(format_alert(flagged), SmtpSettings.from_env())
```

## A note on the method

The threshold is based on the spread of the residuals, not the raw metric, so it
scales to how noisy the metric is. It targets point anomalies against a locally
stable baseline. A sustained level shift will flag until the rolling window
catches up, which is the honest limitation of a detector this simple and the
right place to reach for something heavier if the data needs it.
