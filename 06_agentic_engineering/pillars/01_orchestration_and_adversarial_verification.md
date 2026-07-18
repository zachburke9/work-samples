# Pillar 1: Orchestration and Adversarial Verification

**The rule: findings are claims until an independent pass has tried to kill
them.**

## The problem it solves

A single AI agent, like a single analyst, produces plausible work. Plausible is
the dangerous word. The failure mode of capable systems is not nonsense, which
anyone can catch; it is the confident, coherent finding that happens to be
wrong. No amount of asking the same agent "are you sure?" fixes this, because
you are asking the author to review their own work with the same blind spots
that produced it.

## The design

Work fans out to specialists, and every consequential finding runs a gauntlet
before it counts:

- **Specialist agents by role.** An explorer that sweeps broadly and returns
  conclusions, not file dumps. A reviewer that audits changes against the
  house rules. A lineage hunter whose only job is tracing where a value truly
  comes from, across every system that touches it. Each has its own context and
  its own narrow contract, so depth in one lane never crowds out another.
- **Verify-to-refute, not verify-to-confirm.** Verification agents are prompted
  to disprove the finding, with the default set to "refuted" when uncertain.
  A finding survives only if the refutation fails. For findings that can fail
  in different ways, the verifiers get different lenses (correctness, security,
  reproducibility) rather than three copies of the same skeptic.
- **Judge panels for open design questions.** When the solution space is wide,
  generate independent attempts from different starting biases, score them with
  independent judges, then synthesize from the winner while grafting the best
  ideas from the runners-up. One attempt iterated three times explores less
  than three attempts judged once.
- **The parity gate on anything that replaces anything.** The plain version:
  a replacement must produce the same answers as the thing it replaces, and it
  does not ship until it does. When new logic replaces old logic, old and new
  run side by side and the outputs are diffed row by row. The new version ships when the diff is empty or every difference
  is explained and signed off. Intended improvements ship separately, after,
  visibly. This single discipline is what makes large migrations safe.
- **Review works to zero.** On changes that matter, automated review findings
  are worked to zero across every severity tier: each finding is either applied
  or rebutted with reasoning. Silence and deferral do not count as closure.

## The economics

Adversarial verification looks expensive and is actually cheap. The costly
event in analytics is not agent time; it is a wrong number reaching a decision
maker, or a silent logic change corrupting a pipeline for months. Spending
three verifier passes to kill a plausible-but-wrong finding before it ships is
the best trade available. The discipline also compounds: killed findings teach
the system its own failure patterns, and those patterns become checks.

## What it teaches

Do not scale by making one agent smarter. Scale by making the process
skeptical: independent perspectives, refutation as the default posture, and a
gate that no confident claim can talk its way past.
