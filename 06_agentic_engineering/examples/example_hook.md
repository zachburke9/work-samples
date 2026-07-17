# Example Artifact: A Guardrail Hook

A hook is a deterministic script the environment runs automatically at a fixed
point in the workflow (on save, before a query executes, before a commit). It is
the difference between "we try to remember to check" and "the check cannot be
skipped." Hooks carry the objective, near-zero-false-positive checks; judgment
stays with the humans and agents. This example is generic and reconstructed for
illustration.

```bash
#!/usr/bin/env bash
# sql-lint: fires automatically on every .sql save.
# Objective tripwires only. Anything requiring judgment belongs in review,
# not in a hook.

file="$1"
fail=0

# Known column-name traps (misspellings that parse but return wrong data).
if grep -qiE '\bRES_ADULTS\b' "$file"; then
  echo "TRAP: column is RES_ADULT (singular), not RES_ADULTS" >&2
  fail=1
fi

# Empty-string comparisons silently evaluate to NULL on this platform.
if grep -qiE "(=|<>)\s*''" "$file"; then
  echo "TRAP: use IS NULL / IS NOT NULL, never = '' or <> ''" >&2
  fail=1
fi

# A composite key joined on only half its columns returns duplicates.
if grep -qiE 'JOIN\s+origin_lookup\b' "$file" && \
   ! grep -qiE 'origin_cd' "$file"; then
  echo "TRAP: origin_lookup requires the composite key (source + origin)" >&2
  fail=1
fi

exit $fail
```

Design points:

- **Hooks are deterministic; agents are not.** The two-layer design (fast
  objective tripwires in hooks, contextual audit in a review pass) means the
  cheap layer never blocks on a false positive and the expensive layer never
  wastes effort on typos.
- **Each trap encodes a lesson once.** Every rule above is a mistake that was
  made, diagnosed, and then made impossible to repeat silently. The hook file is
  institutional memory in executable form.
- **The same checks run everywhere.** The identical script backs the editor
  save, the pre-commit hook, and the CI gate, so there is one source of truth
  for what "clean" means.
