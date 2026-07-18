# Example Artifact: A Memory Note Template

Every durable fact in the knowledge base lives in a note shaped like this. The
shape is the point: provenance, verification date, and typed links are mandatory,
so a note is never just an assertion. It is an assertion plus the evidence trail
plus its place in the graph. This example is generic and reconstructed for
illustration.

```markdown
---
name: revenue-ledger-source-of-truth
description: >
  One line a reader can trust without opening the note: the actuals ledger is
  the authoritative revenue source; the rate log overstates by never reversing
  cancellations.
type: domain
verified: 2026-05-14 (row-level comparison, both sources, 3-year window)
links:
  - supersedes: [[rate-log-revenue-method]]
  - depends_on: [[ledger-table-profile]]
  - see_also: [[cancellation-handling]]
---

## The fact

Revenue reporting must read the transaction ledger, not the rate log. The rate
log writes a row when a rate is set but never reverses it when the booking
cancels, so it overstates realized revenue materially over any long window.

## The evidence

Row-level comparison over a 3-year window, run 2026-05-14: the two sources agree
on non-cancelled bookings and diverge by exactly the cancelled set. Query
preserved alongside this note so the check is re-runnable.

## What changed because of this

The revenue pipeline was repointed at the ledger. The old method's note is
marked superseded (link above) rather than deleted, so the history of why
remains findable.
```

Design points:

- **Typed links, not bare links.** `supersedes`, `depends_on`, and `see_also`
  carry different meanings, and the maintenance pass treats them differently: a
  superseded note is kept but never cited; a broken `depends_on` is a defect.
- **Verification is a date and a method, not a vibe.** "verified" states when
  and how, so staleness is measurable. A note whose evidence is older than its
  domain's tolerance gets demoted until re-checked.
- **Supersede, never silently delete.** Wrong-but-was-believed is itself
  institutional knowledge. Deleting it invites rediscovering the error.
