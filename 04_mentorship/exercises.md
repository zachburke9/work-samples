# Analyst Onboarding Exercises

This is a short set of exercises I use when bringing a junior analyst onto a data
team. The goal is not to test cleverness. It is to build the habits that keep a
reporting layer trustworthy: validate before you analyze, write SQL that answers
the question once, and leave code the next person can read.

Each exercise has a short prompt and a worked solution. Work the prompt first,
then compare. The `data_quality.py` module in this folder is the reference
implementation for exercises 1 and 2.

---

## Exercise 1: Validate before you trust

You are handed a customer extract with `id`, `age`, and `name` columns. Before it
feeds any report, confirm three things: no missing values, no duplicate ids, and
no impossible ages (outside 0 to 120).

**Prompt.** Write functions that return the offending rows for each check, then a
single function that runs all three and reports the counts.

**Solution.** See `data_quality.py`. The key idea: each check returns the bad
rows as a DataFrame instead of printing, so the checks compose and can be tested.

```python
from data_quality import validate

report = validate(customers, id_column="id", range_checks={"age": (0, 120)})
if not report.is_clean:
    print(report.summary())   # e.g. {'missing_value_rows': 1, 'duplicate_id_rows': 2, ...}
```

The lesson: a check that prints is a check you cannot reuse. A check that returns
data is one you can assert on in a test and wire into a pipeline gate.

---

## Exercise 2: One row per thing

A raw feed has several rows per order (one per line item), and a teammate wants
"total revenue per order." They reach for a spreadsheet.

**Prompt.** Do it in SQL. Return one row per `order_id` with the summed revenue,
and keep the order date.

**Solution.**

```sql
SELECT
    order_id,
    MIN(order_date)      AS order_date,
    SUM(line_revenue)    AS total_revenue
FROM order_lines
GROUP BY order_id;
```

The lesson: decide the grain (one row per order) before you write the query, and
let the database do the aggregation so the number is reproducible.

---

## Exercise 3: Do not repeat the filter

You need each region's best sales day and how that day compares to the region's
average. A first instinct is two queries and a manual join.

**Prompt.** Do it in one query using window functions.

**Solution.**

```sql
SELECT
    region,
    sale_date,
    daily_sales,
    RANK() OVER (PARTITION BY region ORDER BY daily_sales DESC) AS rank_in_region,
    ROUND(AVG(daily_sales) OVER (PARTITION BY region), 1)       AS region_avg
FROM daily_region_sales;
```

The lesson: window functions let you compare a row to its group without a second
pass. See `../01_sql_etl/sql/booking_pace_window_functions.sql` for a fuller
example.

---

## Exercise 4: Name things for the reader

A report column is named `flg_actv_1`. A leader asks what it means in a meeting
and no one is sure.

**Prompt.** Rename the output columns of a query so a non-technical reader can
read the result with no legend.

**Solution.** There is no single right answer, but the habit is: name a column
for the state the reader cares about, not the database encoding. `flg_actv_1`
becomes `is_active`. `stat_cd = 'C'` surfaced as a column becomes `status` with
values like `Confirmed`. The reader should never need a decoder.

The lesson: the last mile of an analysis is making it legible. Clear names are
part of the work, not an afterthought.
