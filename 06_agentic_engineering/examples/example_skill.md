# Example Artifact: A Skill Definition

A skill is a packaged procedure the agent loads on demand: a trigger, the steps,
and the persistence rule. Codifying a procedure this way turns a good habit into
infrastructure: it fires the same way every session, survives personnel and
model changes, and can be reviewed like code. This example is generic and
reconstructed for illustration; it mirrors the shape of the real ones.

```markdown
---
name: schema-discover
description: >
  Fire the moment a query is about to touch a table not yet profiled. Profiles
  structure, keys, row counts, and value families, then persists the profile so
  future sessions skip re-discovery. Do not wait to be asked.
---

# Schema Discovery

## When to fire
Before writing or running a query against any table with no current profile in
`profiles/` (a profile older than 30 days does not count as current).

## Steps
1. Check `profiles/<TABLE>.md`. If a current profile exists, read it silently
   and proceed with the task.
2. Otherwise, profile the table: columns and types, primary/join keys, row
   count, and the value families of low-cardinality columns.
3. Write the profile to `profiles/<TABLE>.md` with today's date and the queries
   used, so the evidence is re-runnable.
4. Only then continue the original task.

## Persistence rule
The profile is the deliverable as much as the query is. Knowledge captured only
in the conversation is knowledge lost at the end of the session.
```

Two design points worth noticing:

- **The trigger is part of the procedure.** The skill defines when it fires, not
  just what to do, so coverage does not depend on someone remembering to invoke
  it.
- **Persist-or-it-did-not-happen.** Every skill that learns something ends by
  writing it somewhere durable. That single rule is what makes the system
  compound instead of repeating itself.
