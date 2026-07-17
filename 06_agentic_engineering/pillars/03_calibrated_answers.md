# Pillar 3: Calibrated Answers

**The rule: the confidence label comes before the answer, and only verified
answers get stated as fact.**

## The problem it solves

An AI system will answer almost anything fluently, and fluency reads as
confidence. In a business setting that is dangerous: a leader cannot tell the
difference between "we ran this against production last week and checked it" and
"this sounds right." If both arrive in the same confident sentence, the system
is laundering guesses into facts.

## The design

Every answer resolves through a four-level confidence lattice, and the level is
displayed first, never as a footnote:

- **VERIFIED.** The answer was produced by running the query against live data
  and checking it, and the sources it cites have not changed since. This is the
  only level allowed to assert a number as fact.
- **DERIVED.** Grounded in canonical, cited knowledge (business rules, schema
  profiles, the decode references) but not itself a live run. Trustable
  reasoning from trusted sources, labeled as exactly that.
- **GUESS.** A reasoned inference beyond what the sources state. It must carry
  two things: the explicit assumption it rests on, and the disconfirming test
  (the query or check that would prove it wrong). Never presented as settled.
- **UNKNOWN.** Said plainly, and automatically filed as a ticket so the gap
  enters the improvement loop instead of vanishing.

Resolution order is first-match-wins down that ladder, with one crucial twist:
**staleness demotion**. A verified answer stores a fingerprint of the sources it
was checked against, plus a staleness horizon tuned to how fast its class of
fact actually decays (access grants drift in weeks; business rules hold for a
year). If a cited source changes, or the horizon passes, the answer stops being
VERIFIED and demotes to DERIVED-pending-recheck at answer time. The system never
silently serves a stale certainty.

## The flywheel

Every miss is fuel. UNKNOWN answers file tickets automatically; DERIVED and
GUESS answers can seed them. Working a ticket means running the real check
against live data and promoting the answer to VERIFIED with its fingerprint and
date. The verified set grows week over week, which means the system improves
through knowledge and verification, not through retraining. That distinction is
the whole point: the improvement is inspectable, auditable, and owned.

## Why this is rare

The ingredients are published: confidence scoring, provenance tracking,
staleness detection all exist in the literature. What is genuinely uncommon is
shipping them together as a working discipline: label-before-answer, plus
fingerprint-based auto-demotion, plus a miss-to-verified flywheel, enforced on
every question in a production analytics setting. When we later benchmarked the
design against the field, the honest summary was that it assembles published
pieces into a combination the mainstream tools do not ship.

## What it teaches

Calibration is a property you build, not a personality trait you hope the model
has. If your system cannot say "I do not know" in a way that creates work, it
will eventually say something false in a way that creates damage.
