# How to run the auditor in CI

The auditor exits non-zero with `--strict`, so it can gate a pull request.

## Add it to a workflow

```yaml
- name: Check documentation structure
  run: python3 path/to/audit_docs.py docs/ --strict
```

No dependencies to install.
Python 3.9 or later is enough.

## Start without failing the build

A tree that has never been audited will have findings.
Failing the build on day one means people will disable the check.
Report first:

```yaml
- name: Check documentation structure
  run: python3 path/to/audit_docs.py docs/
```

Without `--strict` it always exits zero.
Fix findings over a few weeks, then add the flag.

## Fail only on new problems

If you cannot fix the backlog, record it and compare against it:

```bash
# once, committed
python3 audit_docs.py docs/ --json | jq '.summary.findings' > .docs-baseline

# in CI
current=$(python3 audit_docs.py docs/ --json | jq '.summary.findings')
[ "$current" -le "$(cat .docs-baseline)" ] || {
  echo "documentation findings increased" >&2; exit 1; }
```

This blocks new mixing without demanding the old be fixed first.

## If the auditor flags something you disagree with

It detects the shape of prose, not meaning.
A reference page may legitimately contain one worked example.
Two options:

- Move the content, if the finding is right.
- Leave it and accept the finding, if it is not.
  There is no ignore file by design — a suppression list becomes a place where problems go to be forgotten.

See [findings reference](../reference/findings.md) for what each finding means.
