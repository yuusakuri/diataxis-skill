# Contributing

## Reporting a problem with a finding

If it flags something it should not, open an issue with the page and the lines it cited.
A false finding is a bug: a tool people learn to ignore is worse than no tool.

## Changing the detection rules

Add a fixture showing the case, then change the rule.
Two properties must hold:

- A correctly organised tree produces no findings.
- A tree with mode-mixing produces a finding naming the right page and reason.

```bash
python3 tests/validate_skill.py
```

## Changing the skill

Read the primary source at [diataxis.fr](https://diataxis.fr/) before changing anything about the four modes.
This repository applies Diátaxis; it does not reinterpret it.

Keep `SKILL.md` under 500 lines.
Detail belongs in `references/`, which the agent reads only when it needs to.
