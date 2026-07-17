# Pillar 6: Self-Auditing

**The rule: the system periodically measures what it actually knows against
what it believes it knows, and the audit cannot grade itself kindly.**

## The problem it solves

Every knowledge system drifts toward flattering itself. Documentation claims
coverage it no longer has; a team believes it understands a pipeline because it
understood it two years ago; an AI answers confidently from a note that went
stale last quarter. Without a mechanism that checks belief against evidence,
confidence and accuracy quietly part ways, and nobody notices until a decision
lands on the gap.

## The design

Self-auditing here is a set of instruments, not a resolution to be careful:

- **A maturity ladder, scored per lane.** The system's self-knowledge is scored
  on an explicit six-rung ladder, from pure amnesia at the bottom, through
  faithful recording, organized retrieval, monitoring (knowing what it knows
  and how well), and control (acting on that knowledge: demoting stale answers,
  filing gaps as work), up to the top rung: measuring whether its own
  confidence judgments are empirically accurate. Scoring is per knowledge lane,
  because maturity is never uniform: the schema-knowledge lane can sit two
  rungs above the loose-notes lane, and pretending otherwise hides exactly the
  weakness the audit exists to find.
- **The evidence-path rule.** A rung criterion counts only with a live pointer
  to the artifact that proves it. No evidence path, no credit. This one rule is
  what keeps the audit from becoming self-congratulation: claims about the
  system are held to the same sourcing standard as claims about the data.
- **Pre-registered judgments.** Before a major audit runs, the expected
  findings are written down and frozen in version control. The audit then
  grades those priors as confirmed, complicated, or refuted, and the grade is
  appended beneath the frozen record, never edited into it. The commit history
  is the proof that the system predicted, then measured, rather than measuring
  and then retrofitting the prediction. Honest instance from practice: one
  audit's priors survived seventeen confirmed, three complicated, and one miss,
  and the miss stays in the record because a self-audit that cannot lose is not
  an audit.
- **Calibration as the summit.** The top rung asks the question most systems
  never ask: when the system labels an answer as verified versus derived versus
  guessed, do those labels predict empirical accuracy? Every worked
  gap-ticket is graded on close (was the promoted answer confirmed or
  corrected?), feeding a per-label accuracy measure. The honest current state:
  this rung is the newest and least earned, which the audit says out loud.
- **The apparatus audits itself too.** On a recurring basis, every piece of the
  machinery (including the audit machinery) faces the same triage: keep,
  lighten, delegate, or delete. Discipline that only ever adds instruments
  collapses under its own weight; the value is the gate, not the ceremony
  around it.

## What it teaches

Trustworthiness is not a launch property; it is a maintenance property. Build
the instruments that let the system catch its own drift: an honest maturity
score, evidence-or-no-credit, predictions frozen before measurement, and
calibration checked against outcomes. Then point those instruments at the
instruments. What survives that is worth trusting.
