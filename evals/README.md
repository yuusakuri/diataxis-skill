# Evaluations

These check whether an agent loaded with the skill does what the skill says.
Each assertion states a behaviour `SKILL.md` asks for.
A failing assertion is a gap between the skill and what the agent did.

## Running

1. Load `skills/diataxis/` into an agent that has not read this repository.
2. Give it the prompt from `evals.json`, with the fixture directory named in `files` as its working material.
3. Save the answer as `<runs>/<eval-name>/outputs/answer.md`.
4. Grade:

```bash
python3 evals/results/grade.py <runs>
```

The runs directory defaults to `evals/runs`, or set `DIATAXIS_EVAL_RUNS`.
Exit is 0 only when every assertion passes and every eval has an answer.

## What is here

| File | Contents |
|---|---|
| `evals.json` | The prompts and what each one is looking for |
| `fixtures/` | The docs trees the prompts operate on |
| `results/grade.py` | The assertions |

## Writing an assertion

Assert a behaviour the skill asks for, not knowledge the model already has.
"Names all four modes" passes without the skill loaded, so it measures nothing and cannot fail.

The graders match text with regular expressions, so an answer can satisfy one by saying the right words.
Read the answers as well as the score.
