# Why Diátaxis

Most documentation problems are not writing problems.
The sentences are fine and the facts are right, but readers still cannot find what they came for.

The usual cause is that one page is serving several readers at once.
A page called "Caching" attracts everything about caching: why it exists, how to turn it on, what the options are, and a lesson for beginners.
Four readers arrive, and each has to read the other three's content.

## The two questions

Diátaxis separates documentation by what the reader needs at the moment they arrive, using two questions:

1. Does the content inform action (doing) or cognition (thinking)?
2. Does it serve acquisition of skill (studying) or application of skill (working)?

| Informs… | Serves… | Mode |
|---|---|---|
| action | acquisition | tutorial |
| action | application | how-to guide |
| cognition | application | reference |
| cognition | acquisition | explanation |

Both questions are about the reader, not the subject.
"Caching" is a subject, so it spans all four.
That is why filing by subject produces the pile.

## Why this framework and not a house style

Two reasons.

It is decidable.
Two questions with two answers each give four boxes, and most content lands in one of them without argument.
A style guide that says "write clearly" gives nobody a way to settle where a page goes.

It is diagnostic.
Because the modes have different shapes, you can see when a page is mixed: a reference page with a "Step 1" in it, an explanation that ends in a numbered list.
That is what the auditor in this repository looks for.

## What it does not cover

Diátaxis organises documentation written for readers.
It does not govern documents whose shape is set by their purpose — an architecture decision record, a product requirements document, an RFC, a runbook, a changelog.
Those have their own conventions, and forcing them into four modes loses what makes them useful.

The skill defers on those rather than classifying them.

## Source

Diátaxis is the work of Daniele Procida.
The authoritative description is at [diataxis.fr](https://diataxis.fr/).
This repository applies it; it does not restate it.
