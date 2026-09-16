---
name: diataxis
description: Organise documentation with the Diátaxis framework - decide whether a page is a tutorial, how-to guide, reference, or explanation, scaffold a docs tree around those four modes, audit existing docs for mode-mixing, and write each page in the mode it belongs to. Use whenever documentation structure is in question: starting a docs/ directory, deciding where a new page goes, a docs folder that has grown into a pile of unrelated markdown, a README that has swollen past what anyone reads, or a request to reorganise, split, restructure, or audit documentation. Use it even when Diátaxis is not named - "where should this doc live", "our docs are a mess", "split up this guide" are all this skill.
license: MIT
metadata:
  framework: "Diátaxis (https://diataxis.fr/)"
  version: "1.0"
---

# Diátaxis

Most documentation problems are not writing problems.
They are classification problems: a page is trying to serve two readers at once, so it serves neither.

Diátaxis solves this by separating documentation into four modes, each answering a different need.
Your job with this skill is to put every piece of content in exactly one of them, and keep it there.

## The compass

Two questions settle nearly every case.
Ask them about the reader at the moment they arrive, not about the subject matter:

1. Does this inform action (doing) or cognition (thinking)?
2. Does it serve acquisition of skill (study) or application of skill (work)?

| If the content informs… | …and serves… | …it belongs in |
|---|---|---|
| action | acquisition of skill | tutorial |
| action | application of skill | how-to guide |
| cognition | application of skill | reference |
| cognition | acquisition of skill | explanation |

When you cannot decide, the usual cause is that the content is genuinely two things.
Split it and link the halves — that is the answer, not a compromise.

## What each mode owes its reader

| Mode | The reader is… | So the page must… | And must not… |
|---|---|---|---|
| Tutorial | learning by doing, with no prior context | guarantee success on a single concrete path; hold their hand | branch, discuss alternatives, or list every option |
| How-to guide | at work, already knows what they want | show a route through a real problem, allowing for variation | teach, explain, or try to be exhaustive |
| Reference | mid-task, needs a fact now | be accurate, complete, and boring; describe the machinery | instruct, persuade, or explain why |
| Explanation | trying to understand, away from the keyboard | discuss why, connect ideas, admit alternatives and trade-offs | instruct or catalogue |

## Working with an existing docs tree

Read the pages before proposing anything.
For each one, name the reader it serves and what they were doing when they opened it.
A page you cannot answer that for is the page to look at first.

Say which lines led you to each conclusion, so the author can disagree with the evidence rather than with you.
Judgements about what a reader needs are yours to make and to defend; do not present them as measurements.

Then, for each finding:

1. Unclassified page — apply the compass and move it.
   If it resists classification, that is the signal it is two pages.
2. Mode-mixing — cut the foreign material out and move it to its own mode, leaving a link.
   The commonest case by far is instruction absorbed into reference or explanation; procedures hide there, where nobody looking for a procedure will look.
3. Missing mode — only a gap when a reader needs it.
   Say what that reader would have come for, and leave the mode absent until someone does.
   Missing explanation is worth raising, because teams skip it and then re-derive it in every code review.

Restructure incrementally.
A docs tree is read while it is being rearranged, so move one page at a time and keep links working.
`references/how-to-restructure.md` covers doing this on a large tree without a flag day.

## Starting a new docs tree

```
docs/
├── index.md              what this is, and a link into each mode
├── tutorials/            numbered lessons; usually very few
├── how-to/               one file per real task, named "How to …"
├── reference/            mirrors the structure of the thing it describes
└── explanation/          one file per topic, named as a question or theme
```

Templates for each mode's index page and a first page are in `assets/templates/`.

Two naming rules carry most of the weight, because a name is what a reader navigates by: a how-to guide is titled by the reader's goal ("How to rotate API keys"), never by the machinery ("The rotate command").
An explanation is titled by its question or topic ("Why deployments are immutable"), never as a task.

## Scope

Organise what you were given.
A request to sort out a docs folder is not a request to write the pages it does not have.

Do not create a page to complete the set.
Four half-filled modes serve nobody better than two good ones: an empty `tutorials/` advertises a lesson that does not exist, and a tutorial written to fill a slot teaches nothing anybody asked to learn.

If a mode is missing and you think a reader wants it, name that reader and say what they would have come for.
Then let the author decide whether to write it.

## Writing in a mode

Before writing, say which mode the page is and why.
If that sentence is hard to write, stop — the page is not yet one thing.

- Tutorial — write in the first person plural ("we'll create…"), promise a concrete outcome up front, and make every step produce a visible result the reader can check against.
  Never explain more than the step needs; link out instead.
  The reader must finish it and feel it worked.
- How-to guide — start from the problem, not the tool.
  Assume competence.
  Cover the variations a real user hits ("if you are on a managed instance, instead…").
  Omit everything that is not on the path.
- Reference — be austere and consistent.
  State what is, not what to do.
  Structure it to mirror the code or the API, so a reader can predict where a fact lives.
  Consistency matters more than prose quality here.
- Explanation — bound it by a question ("Why X?", "How does Y fit with Z?").
  Admit opinion, history, and alternatives — that is what makes it explanation rather than reference with adjectives.

`references/four-modes.md` has fuller per-mode guidance and worked before/after examples; read it when a page is hard to place or you are rewriting one in a new mode.

## A note on this skill's own files

The bundle uses the directory names the Agent Skills spec defines — `references/`, `assets/` — so they are not mode names.
The files inside are named by mode instead: `four-modes.md` is reference, `how-to-restructure.md` is a how-to.

## Where this skill defers

Diátaxis governs documentation for readers.
It is not the right frame for documents whose structure is fixed by their purpose — an ADR, a PRD, an RFC, a runbook, a changelog.
Those have their own skills and their own shapes; do not force them into the four modes.
If the project has a skill for the artefact in question, use that instead and leave the docs tree alone.

## Red flags

- A page you cannot name a mode for.
  It is two pages wearing one filename.
- "Getting started" that is really an option catalogue.
  A tutorial that stopped teaching.
- A reference page with a Step 1.
  The procedure is hidden where nobody looks for it.
- An explanation that ends with instructions.
  The instructions will rot, because nobody maintains procedures they did not expect to find there.
- Four empty mode directories.
  The structure is not the goal; serving the four needs is.
  An empty `tutorials/` is worse than no `tutorials/`.
- Reorganising without reading the pages.
  Classification is about what the reader needs from the content, which you cannot know from the filename.
