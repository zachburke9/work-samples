# Mentorship

The material I use to bring a junior analyst onto a data team. It is small on
purpose: the habits that keep a reporting layer trustworthy matter more than
volume.

## Contents

- `data_quality.py` is a reusable, tested toolkit of the checks every dataset
  should pass before it reaches a report: missing values, duplicate identifiers,
  and out-of-range numbers. Each check returns the offending rows rather than
  printing, so the checks compose, can be asserted on, and can gate a pipeline.
- `exercises.md` is a short set of graded exercises with worked solutions,
  covering validation, query grain, window functions, and naming for the reader.
- `tests/` covers the validation toolkit.

## Run it

```bash
python data_quality.py
```

```
Validation summary:
  missing_value_rows: 1
  duplicate_id_rows: 2
  out_of_range_age: 1

Clean dataset: False
```

## The teaching idea

A check that prints is a check you cannot reuse. A check that returns data is one
you can test and wire into a pipeline. That single shift, from printing problems
to returning them, is most of what separates a script from something a team can
depend on, and it is the first habit I try to build.
