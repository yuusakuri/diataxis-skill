# What the skill adds

Diátaxis is well known, and a capable model can apply it unprompted.
So the honest question for this skill is not "does it work" but "does it add anything a model does not already do".

We measured it.
The answer is: not the framework, but three things around it.

## How it was measured

Three realistic prompts were run twice each — once with the skill loaded, once with no skill — by independent agents that had not seen the repository.
The prompts, fixtures and graders are in [`evals/`](../../evals/).
Every assertion is checked by a script, so the numbers do not depend on the author's opinion.

## The first attempt found nothing

| Eval | With skill | Without |
|---|---|---|
| Restructure a messy docs tree | 6/6 | 6/6 |
| Diagnose one mixed page | 4/4 | 4/4 |

Identical.
Those assertions checked things like "names all four modes" and "proposes splitting the page" — which the model does unaided.

That result is kept rather than deleted.
A skill that restates what the model already does is not worth the context it occupies, and assertions that cannot fail cannot tell you which kind you have.

## The second attempt found three differences

| Eval | With skill | Without |
|---|---|---|
| Restructure a messy docs tree | 5/5 | 3/5 |
| Diagnose one mixed page | 4/4 | 2/4 |
| Defer on an ADR | 4/4 | not run |

The assertions that separated them:

| Assertion | With | Without |
|---|---|---|
| Cites line numbers as evidence | pass, both evals | fail, both evals |
| Refuses to create an empty placeholder page | pass | fail |
| Does not offer "add some headings" as a fix | pass | fail |

## What that means

Evidence.
The bundled auditor produces line-number citations, so a recommendation can be checked.
Neither unaided run produced any, because neither had a tool that could.

Resistance to plausible non-fixes.
The unaided run suggested adding four `##` headings to a four-mode page.
That makes it easier to skim and leaves it four modes.
It was also willing to scaffold an empty tutorial directory.

A boundary.
Asked where an architecture decision should be written down, the skill-loaded run identified it as an ADR and declined to file it as a tutorial, how-to or reference — while still pointing at explanation as a legitimate follow-on page.

## What it did not change

Four assertions passed either way.
The model already named all four modes, already classified a beginner walkthrough as a tutorial rather than a how-to, already warned that a subject-named file re-accumulates content, and already proposed moving pages incrementally.

## Limits of this measurement

Three prompts, one run each.
Enough to show a direction, not to put a number on it.
No unaided run for the ADR case, so that row is unopposed.
The graders match text with regular expressions, so they can be satisfied by an answer that says the right words; the answers were also read.
