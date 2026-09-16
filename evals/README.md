# Evaluations

These check what the skill changes about an agent's answer.
They are not unit tests: each one is a prompt given to an agent twice, once with the skill loaded and once without, and the two answers are compared.

## Running one

1. Give an agent the prompt from `evals.json`, with the fixture directory named in `files` as its working material.
2. Do it twice: once with `skills/diataxis/` installed, once with no skill.
3. Save each answer as `<runs>/<eval-name>/<config>/outputs/answer.md`, where `<config>` is `with_skill` or `without_skill`.
4. Grade:

```bash
python3 evals/results/grade_discriminating.py <runs>
python3 evals/results/grade_baseline_assertions.py <runs>
```

The runs directory defaults to `evals/runs`, or set `DIATAXIS_EVAL_RUNS`.

Use an agent that has not read this repository.
An agent that has read the skill cannot produce a without-skill answer.

## What is here

| File | Contents |
|---|---|
| `evals.json` | The prompts and what each one is looking for |
| `fixtures/` | The docs trees the prompts operate on |
| `results/grade_discriminating.py` | Assertions aimed at what the skill supplies |
| `results/grade_baseline_assertions.py` | An earlier set, kept because it separated nothing |

`grade_baseline_assertions.py` is kept deliberately.
It checked things like "names all four modes", which the model does unaided, so it scored identically both ways.
An assertion that cannot fail cannot tell you whether a skill is worth its context.
