# Changelog

All notable changes to this portfolio are recorded here. Format loosely follows
[Keep a Changelog](https://keepachangelog.com/).

## [2.0.0] - 2026-07-17

A full overhaul focused on correctness, structure, and reproducibility.

### Added
- Competency-based structure: `01_sql_etl`, `02_analytics_automation`,
  `03_ml_forecasting`, `04_mentorship`, `05_platform_migration`,
  `06_agentic_engineering`.
- The centerpiece piece on agentic engineering and institutional intelligence:
  six pillars, an architecture diagram, and generic examples of the machinery
  (a skill definition, a guardrail hook, a memory note template).
- Runnable sample data for every project, so each sample works offline with no
  database or credentials.
- A window-function SQL query with a SQLite harness that runs it against fixtures.
- A test suite (`pytest`) covering the detection, forecasting, and validation
  logic, plus a CI workflow that runs `ruff` and `pytest`.
- A reproducible forecasting pipeline with a saved predicted-vs-actual chart.
- A generalized ETL-platform migration case study with an architecture diagram.
- `LICENSE` (MIT), `.gitignore`, and pinned `requirements.txt`.

### Changed
- Merged the two near-duplicate anomaly scripts into one engineered module with
  logging, type hints, and a CLI.
- Email alerting now reads credentials from environment variables (see
  `.env.example`) instead of hardcoded values, and is import-safe.
- Rewrote the README around a competency matrix and an embedded chart.

### Fixed
- `requirements.txt` no longer lists a non-existent package, so
  `pip install -r requirements.txt` succeeds.
- The cost-transformation SQL now defines `discount_inventory_category`, which was
  referenced but never created, so the query runs and the consolidation is correct.

### Removed
- The aspirational `RELEASE.md` and references to folders that did not exist.

## [1.1.0] - 2025-03-13
- Initial public portfolio: SQL ETL sample and four Python analytics scripts.
