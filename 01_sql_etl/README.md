# SQL ETL

Two SQL samples with runnable fixtures. Each query is standard SQL, verified on
SQLite via `run_samples.py`, and portable to Postgres, Snowflake, or Oracle
unchanged.

## Contents

- `sql/cost_data_transformation.sql` normalizes raw, multi-row cost data into one
  enriched row per record: gross and net cost, adjustments, cross-system discount
  reconciliation, and lookup joins.
- `sql/booking_pace_window_functions.sql` turns a daily bookings feed into a pace
  view: running total, day-over-day change, a 3-day moving average, and a
  within-region rank, using window functions.
- `sample_data/` holds the CSV fixtures for both queries and the generated
  `*_output.csv` results.
- `run_samples.py` loads the fixtures into in-memory SQLite, runs each query, and
  writes the results. Standard library only, no database required.

## Run it

```bash
python run_samples.py
```

The script prints a preview and writes each query's result to
`sample_data/<query>_output.csv`.

## The scenario: cost transformation

Raw cost data arrives with several rows per service transaction, one per cost
component. Two source systems encode promotional discounts differently: SYSTEM_A
as a negative revenue row, SYSTEM_B in a separate column. The query reconciles
both so the reporting layer sees one consistent shape, and it filters out
settlement and special-promotion rows that do not belong in the cost view.

| Service | Category   | Revenue |
|---------|------------|---------|
| 123     | BASE       | 100     |
| 123     | ADJUSTMENT | -20     |
| 123     | PROMOTIONS | -10     |

The transformation derives `gross_cost`, `net_cost`, `cost_adjustments`,
`cost_discounts`, and a `consolidated_inventory_category`, then enriches each row
with location and employee lookups.
