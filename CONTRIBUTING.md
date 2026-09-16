# Contributing

## Changing the skill

Read the primary source at [diataxis.fr](https://diataxis.fr/) before changing anything about the four modes.
This repository applies Diátaxis; it does not reinterpret it.

Keep `SKILL.md` under 500 lines.
Detail belongs in `references/`, which the agent reads only when it needs to.

The check:

```bash
python3 tests/validate_skill.py
```

It parses the frontmatter as YAML and checks the fields the [Agent Skills spec](https://agentskills.io/specification) requires, that the name matches the directory, and that every bundled file `SKILL.md` points at exists.

## Changing what the skill decides

A change to the skill's judgement needs evidence that it changed the answer.
`evals/` holds the prompts and the graders.
Add a case there showing the behaviour you are fixing, and record the result with and without the skill.

A change that leaves every eval identical is a change to the wording, not to the skill.

## Reporting a problem

Open an issue with the prompt you gave, the docs tree you gave it, and the answer you got.
The answer is the evidence: the skill produces judgements, and a judgement you disagree with is worth more than a description of it.
