# What the skill adds

Diátaxis is well known, and a capable model applies it unprompted.
The skill's value is therefore not the framework but the four rules below, each of which `evals/` checks.

## Evidence you can argue with

The skill requires each judgement to name the lines it rests on.
"This page is doing three jobs" is an opinion; "lines 3–5 are explanation, 7–10 a procedure, 12–16 a reference table" is something the author can disagree with point by point.

## Refusal to build empty structure

The four mode directories are not the goal.
A model asked to apply Diátaxis will readily scaffold `tutorials/` and leave it empty, or write a tutorial nobody asked for so that the set looks complete.
The skill treats a missing mode as a gap only when a reader needs it, and says so instead of filling it.

## Refusal of plausible non-fixes

Adding four `##` headings to a page containing four modes makes it easier to skim and leaves it four modes.
The skill rejects that as a fix, because the problem is which page the content is on, not how it is signposted.

## A boundary

An architecture decision record, a PRD, an RFC, a runbook and a changelog have shapes fixed by their purpose.
The skill declines to file them in the four modes, and says which artefact it is instead.

## Checking these

`evals/` holds the prompts, the fixtures and the assertions.
Each assertion states one of the behaviours above, so a failure is a gap between this page and what the agent did.
`evals/README.md` has the procedure.

No results are recorded here.
A number in this file would only be trustworthy if it were regenerated whenever the skill changed, and nothing enforces that.
Run the evals and read the answers.
