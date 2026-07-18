# Pillar 2: Institutional Memory

**The rule: one fact, one home, at the velocity it changes. Everything else is
a pointer.**

## The problem it solves

AI sessions are amnesiac by default, and teams are amnesiac by attrition. Both
lose the same things: why a decision was made, which source is authoritative,
what was already tried and disproven. Most attempts to fix this produce a wiki
that grows until it rots, because accumulation is easy and consolidation is
work. A confidently stale knowledge base is worse than none: it answers with
authority it no longer has.

## The design

The memory is a curated knowledge graph written in plain, version-controlled
text, operated under a few hard disciplines:

- **Two tiers, published deliberately.** A personal source-of-truth tier holds
  everything, including process notes that generalize to no one. A curated
  shared mirror is published from it through an explicit manifest: share the
  source of truth, keep the scratchpad personal. Sync is direction-aware, so an
  edit made in the wrong tier is caught, never silently overwritten.
- **An index that refuses to grow.** The always-loaded index holds anchors,
  global rules, and one line per domain hub. A canary trips when it exceeds a
  size budget, forcing a consolidation pass: the largest flat cluster gets
  promoted into its own hub and collapses back to one line. Growth is roughly
  one line per new domain, never one line per new fact.
- **The graph is derived, never hand-fed.** Notes link to each other in plain
  markdown, load-bearing links carry types (supersedes, depends_on), and a
  small script derives the graph from the text itself, reporting broken links,
  orphans, duplicates, and naming drift. There is no parallel database to fall
  out of sync with the prose, because the prose is the database.
- **Three operations, not ad-hoc edits.** Ingest folds a new source into the
  graph in one pass: distill, re-verify against current live data, choose its
  home, update every artifact that links to it, log it. Query answers from the
  graph with citations. Lint is the periodic consolidation pass: contradictions,
  stale claims, duplicated facts, orphaned notes. The lint proposes; a human
  approves. Curated prose is never rewritten silently.
- **Facts live at the velocity they change.** Fast-moving state (versions,
  statuses, dates) lives where it updates automatically and is pointed to,
  never copied into slow documents. Every fact has exactly one home; every
  other mention is a link. Stale pointers are treated as defects, not chores:
  if there is a link, updating it is part of the same work, not a follow-up.

## The honest lineage

The architecture deliberately builds on the emerging LLM-wiki pattern (a
curated index, hub notes, ingest/query/lint operations) and on published work
arguing for typed edges over bare links. The house divergence is the important
part: where the published pattern treats ingested sources as immutable raw
material, this system re-verifies every ingested claim against current live
data before it earns a place in the graph. Trust is granted by verification,
not by arrival.

## What it teaches

Memory is not storage; it is maintenance. Anyone can write things down. The
institution emerges from the disciplines that keep what is written true: one
home per fact, consolidation on a tripwire, verification before trust, and a
publish step that separates what you know from what you share.
