# Findings reference

Every finding has a `kind`, a `severity`, and a `path`.
Mode-mixing findings also carry `mode` (the page's own mode) and `intruder` (the foreign one).

## Finding kinds

| Kind | Severity | Meaning |
|---|---|---|
| `missing-mode` | info | No page anywhere uses this mode. |
| `mode-mixing` | warning | The page carries enough material from another mode to hinder its reader. |

A page outside the mode directories is not examined and produces no finding.
The run reports how many there were.
Index and README files are not counted.

## Signals

The auditor counts four kinds of work a passage can be doing.

| Signal | Detected from |
|---|---|
| `action` | Numbered or bulleted imperative steps; `Step N` headings; shell code fences |
| `reference` | Tables whose header names options, parameters, fields, types or defaults; `- \`--flag\`` definitions; code fences declaring a language |
| `explanation` | Words that mark reasoning: why, because, rationale, trade-off, historically, alternative |
| `teaching` | Phrases that address a learner: "in this tutorial", "you will learn", "by the end", "congratulations" |

Lines inside a code fence are not counted as prose.
A fence is counted once, by its language.

## Exit codes with `--strict`

`--strict` exits 1 when a warning was reported, and 0 otherwise.
An `info` finding does not fail the run.

## When mode-mixing is reported

Both conditions must hold:

1. The page has at least 3 foreign signals.
   Fewer is a passing mention, which every mode is allowed.
2. The page's own signal count is less than twice the foreign count.
   A strongly native page is allowed incidental foreign material.

## Which pairs are checked

Not every combination is a problem.
These are:

| Page mode | Foreign signal | Why it matters |
|---|---|---|
| reference | action | A reader scanning for a fact must read past a procedure. |
| reference | explanation | Reference describes the machinery; reasoning belongs in explanation. |
| tutorial | reference | Option tables interrupt a lesson. |
| tutorial | explanation | Extended discussion breaks the flow of doing. |
| how-to | teaching | Teaching asides mean it is drifting into a tutorial. |
| how-to | reference | A how-to is a path, not a catalogue. |
| explanation | action | Procedures absorbed into explanation hide from the people who need them. |

## Limits

The auditor matches the shape of prose.
It cannot read meaning, so it produces candidates, not verdicts.
Check the cited lines before acting.
