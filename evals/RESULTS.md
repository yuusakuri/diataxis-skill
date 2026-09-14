# Evaluation

Three realistic prompts were run twice each — once with the skill loaded, once with no
skill — by independent agents that had not seen this repository. Prompts and fixtures
are in [`evals.json`](evals.json); the graders are in [`results/`](results/) and every
assertion is checked programmatically, so the numbers are reproducible rather than a
matter of the author's opinion about their own skill.

## First attempt: the assertions measured nothing

| eval | with skill | baseline |
|---|---|---|
| restructure a messy docs tree | 6/6 | 6/6 |
| diagnose a single mixed page | 4/4 | 4/4 |

Identical. The assertions checked things like "names all four modes" and "proposes
splitting the page" — and the model does those unaided, because Diátaxis is well known
and it had already read the same primary sources. **The first assertion set measured
the model's prior knowledge, not the skill.**

That is worth recording rather than quietly replacing. A skill that restates what the
model already does is not worth its context cost, and the only way to find out is to
write assertions that could fail.

## Second attempt: assertions targeting what the skill actually supplies

| eval | with skill | baseline |
|---|---|---|
| restructure a messy docs tree | 5/5 | 3/5 |
| diagnose a single mixed page | 4/4 | 2/4 |
| defer on an ADR | 4/4 | not run |
| **total (comparable evals)** | **9/9** | **5/9** |

The four assertions that separated them:

| Assertion | With skill | Baseline |
|---|---|---|
| Cites concrete line ranges as evidence | pass (both evals) | fail (both evals) |
| Refuses to create an empty placeholder tutorial | pass | fail |
| Does not offer "add some headings" as an acceptable fix | pass | fail |

And the four the skill did **not** change — the model already did them unaided:

- names all four modes
- classifies `setup.md` as a tutorial rather than a how-to
- warns that a subject-named file will re-accumulate content
- gives an incremental move procedure

## What this says the skill is for

Not teaching the framework. The value it measurably adds is:

1. **Mechanical evidence.** The bundled auditor produces line-number citations, so the
   recommendation is checkable rather than assertive. Neither baseline run produced
   any, because neither had a tool to produce them.
2. **Discipline against plausible non-fixes.** The baseline offered "add four `##`
   headings" — which makes a four-mode page easier to skim while leaving it four modes
   — and was willing to scaffold an empty tutorial. The skill's red flags rule both out.
3. **A deferral boundary.** Asked where an architecture decision should live, the
   skill-loaded run identified it as an ADR and declined to force it into the four
   modes, while still naming explanation as the legitimate follow-on.

## Limitations

- Three prompts, one run each. Enough to show a direction, not to put a number on it.
- No baseline was run for the ADR deferral case, so that column is empty rather than
  zero — the skill's 4/4 there is unopposed.
- The graders use regular expressions over the answers. They can be fooled by an answer
  that says the right words without meaning them; the answers were also read.
