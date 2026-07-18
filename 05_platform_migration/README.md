# Case Study: Migrating Off a Visual ETL Tool to SQL-Native Ownership

This is a generalized write-up of a migration I have led: moving a body of
business-critical data pipelines off a drag-and-drop ETL tool and onto owned,
version-controlled SQL. It is deliberately vendor-neutral and carries no
company-specific data. The point is to show how I scope a migration, de-risk it,
and prove the result is correct.

## The situation

A reporting estate had grown up inside a visual ETL tool: dozens of workflows,
each a canvas of connected tools, feeding dashboards that leaders depended on.
That tool did its job for years. Over time the cost of staying on it grew:

- **Opaque logic.** Business rules lived inside tool configurations that did not
  diff, review, or search like code. Understanding a workflow meant opening it
  and clicking through nodes.
- **Single points of knowledge.** A workflow was understood by whoever built it.
  When that person was out, changes stalled.
- **Runtime quirks.** The tool's own execution differed from the database in
  small, sharp ways (statement parsing, comment handling, how it staged writes),
  so logic that looked correct could still fail at run time.
- **Licensing and lock-in.** The estate was tied to one vendor's runtime.

## The approach

I did not attempt a big-bang rewrite. The strategy was to **own each pipeline as
SQL, one at a time, behind a parity gate**, so nothing changed for the consumer
until the new version was proven equal to the old one.

1. **Reverse-engineer before rewriting.** Extract every input query and the
   transformation logic from each workflow, and write down what it actually does
   (not what it was assumed to do). Weird-looking logic is load-bearing more often
   than it is a mistake, so it gets preserved until proven otherwise.
2. **Rebuild as SQL-native.** Re-express the pipeline as version-controlled SQL
   that the database runs directly: CTEs for the transformation steps, a target
   table the reporting layer already reads, and a scheduled refresh.
3. **Prove parity.** Run old and new side by side and diff the output row for
   row. The new version does not ship until the diff is empty or every remaining
   difference is explained and signed off. This is the gate that makes the
   migration safe.
4. **Add observability the old tool lacked.** A small run-history table records
   every refresh (start, end, row counts, status), so a failed or partial load is
   visible instead of silent.
5. **Cut over and retire.** Point the schedule at the SQL version, watch it for a
   cycle, then retire the old workflow.

## Why parity is the whole game

The reason migrations like this fail is not that the new SQL is hard to write. It
is that a subtle difference in a business rule ships unnoticed and a leader makes
a decision on a number that quietly changed. The parity gate removes that risk:
the migration is not "done" when the SQL runs, it is done when the SQL produces
the **same** answer as the system of record, and any intended improvement is made
as a separate, visible, signed-off change afterward.

## Outcome

- Business logic became reviewable, diffable, and searchable, like any other
  code.
- Pipelines stopped depending on one person's memory of a canvas.
- Refreshes became observable through the run-history table.
- The estate moved off a vendor runtime and onto the database it already ran on.

## What this folder shows

- `README.md` (this file): the case study and the reasoning.
- `architecture.md`: the target design, the parity-gate method, the run-history
  table, and a dataflow diagram.

The SQL patterns referenced here are demonstrated concretely in
[`../01_sql_etl`](../01_sql_etl), which includes a working transformation and a
window-function query with runnable sample data.
