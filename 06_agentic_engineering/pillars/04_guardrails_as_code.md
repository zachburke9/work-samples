# Pillar 4: Guardrails as Code

**The rule: a lesson is not learned until it is enforced by something that
cannot forget it.**

## The problem it solves

Every data team accumulates hard-won knowledge about its own traps: the column
name that parses but returns wrong data, the join that silently duplicates
rows, the empty-string comparison that a particular database treats as NULL.
Traditionally this knowledge lives in people and documents, which means it is
enforced by memory and mood. It decays with turnover and fails exactly when
someone is tired, rushed, or new.

## The design

Enforcement depth is the organizing idea: prose asks nicely, gates hold. Rules
that can be checked objectively get pushed down the stack until they are
mechanical.

- **Deterministic hooks at the moment of action.** A hook is a script the
  environment runs by itself at a fixed point, so the check happens without
  anyone needing to remember it. They fire on every SQL save (known column traps,
  null-comparison mistakes, composite-key misuse), before a query touches an
  unprofiled table (a reminder that this is unmapped territory), before any
  write that could leak something that should not be shared. They are fast,
  objective, and tuned for near-zero false positives, because a guardrail that
  cries wolf gets disabled.
- **One gate engine, two layers.** The same checking script runs as a local
  pre-commit hook and as CI on every pull request. One definition of clean, two
  enforcement points, no drift between them. The checks are diff-scoped, so
  legacy files are not re-litigated on every change.
- **The two-layer review split.** Hooks carry only the objective tripwires.
  Contextual judgment (does this filter make sense for this business question?)
  belongs to a separate deep-review pass, agent or human. Keeping the layers
  separate is what keeps the fast layer trustworthy and the deep layer focused.
- **Expectation-first data checks.** Every owned table ships with named,
  re-runnable assertions written alongside its DDL, not after its first bug:
  key uniqueness, row-count bands, reconciliation back to source, null-rate
  ceilings. They run after every refresh. A load that succeeds mechanically but
  writes a tenth of the usual rows is a failure, and the system treats it as
  one instead of advancing its bookmark.
- **Mistakes become guardrails.** The loop that makes this compound: when a
  defect is diagnosed, the fix ships twice. Once in the artifact, and once as a
  new trap in the hook or a new assertion in the suite, making the same silent
  failure structurally unrepeatable. The guardrail file reads as the fossil
  record of every sharp edge the team has ever hit.

## The boundary

Not everything belongs in a gate. Judgment calls forced into mechanical checks
produce false positives, and false positives corrode trust in the whole layer.
The discipline cuts both ways: objective and consequential goes in the gate;
contextual goes to review; trivial goes nowhere. An apparatus heavier than the
work it protects is its own defect.

## What it teaches

Culture does not scale; enforcement does. Write the standard down, then ask:
what part of this can a script hold so no person has to remember it? The part
that remains is where the humans and the judgment belong.
