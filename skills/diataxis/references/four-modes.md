# The four modes in depth

Read this when a page is hard to place, or when rewriting one from one mode into
another. `SKILL.md` has the compass; this has the detail and worked examples.

## Contents

- [Tutorial](#tutorial)
- [How-to guide](#how-to-guide)
- [Reference](#reference)
- [Explanation](#explanation)
- [The four confusions](#the-four-confusions)
- [Before and after](#before-and-after)

---

## Tutorial

The reader is a beginner who does not yet know what they need to know. They cannot
tell you what they want, because they do not know the vocabulary yet. Your job is to
give them an experience of success.

- Promise one concrete outcome and deliver exactly that.
- Every step produces a visible result. "You should see…" is the load-bearing sentence
  of a tutorial: it lets the reader confirm they are still on the path.
- One path only. No "you could also…", no conditional branches, no alternatives. Every
  choice you offer is a chance to get lost.
- Minimum explanation. Where the reader will wonder why, link to explanation and
  carry on.
- It must work, every time, from a clean state. A tutorial that fails at step 7 is
  worse than no tutorial, because it teaches the reader the project is unreliable.

Tutorials are the most expensive documentation to maintain, which is why most projects
should have very few. One that works beats five that rot.

## How-to guide

The reader is competent and at work. They have a goal and a real, messy situation.

- Titled by the goal: "How to restore a backup to a new region."
- Starts at the problem, not the tool. The machinery is means, not subject.
- Allows for variation, because real situations vary: "if you are using the managed
  service, do X instead."
- Omits teaching. The reader does not want to learn the system; they want to finish.
- Not exhaustive. A how-to guide is a path, not a map. Completeness belongs to
  reference.

The commonest failure is writing tool-centred guides — "Using the export command" —
which leave the reader to work out for themselves whether that command solves their
problem.

## Reference

The reader is mid-task and needs a fact. They arrive, take one thing, and leave.

- Describe the machinery. State what is. Never instruct.
- Structure it to mirror the thing described, so a reader can predict where to look.
  If the code has modules, so does the reference.
- Be consistent above all: same order, same headings, same level of detail for every
  entry. A reader learns the shape once and then reads fast.
- Be austere. Reference is allowed to be boring. Personality here costs scanning speed.
- Generate it from source where you can; hand-written reference drifts from reality,
  and reference that is wrong is worse than reference that is missing.

## Explanation

The reader is trying to understand, probably not at the keyboard.

- Bound it with a question or topic: "Why deployments are immutable", "How caching and
  invalidation fit together."
- Discuss why. History, constraints, trade-offs, the alternatives that were rejected
  and the reason.
- Admit opinion and multiple viewpoints. This is the one mode where that is correct.
- Connect things. Explanation is where the reader builds a mental model that the other
  three modes assume.

Explanation is the mode teams skip, and skipping it is expensive: the reasoning gets
re-derived in code review, in incident retrospectives, and in arguments about decisions
nobody recorded.

---

## The four confusions

| Confusion | Symptom | Fix |
|---|---|---|
| Tutorial ↔ how-to | "Getting started" that assumes competence, or a how-to that teaches basics | Ask whether the reader knows what they want. If yes, how-to. |
| Reference ↔ how-to | A reference entry with a procedure in it | Move the procedure to a how-to guide, link from the entry |
| Explanation ↔ reference | Discussion of why buried in an API description | Reference states what is; move the reasoning out |
| Explanation ↔ how-to | An essay that ends in a numbered list | Split; the instructions are hiding from the people who need them |

---

## Before and after

Before — one file, `docs/caching.md`, doing four jobs:

```markdown
# Caching
Caching exists because our origin is slow and traffic is spiky.  <- explanation
We considered a CDN-only approach but rejected it because...     <- explanation
To enable caching: 1. set CACHE=1  2. restart the workers        <- how-to
| Option | Default | -------- | TTL | 300 |                       <- reference
In this guide you will build your first cached endpoint...        <- tutorial
```

After — four files, each with one reader in mind:

```
docs/explanation/why-we-cache.md      why it exists, what was rejected and why
docs/how-to/enable-caching.md         "How to enable caching for a service"
docs/reference/cache-options.md       the options table, nothing else
docs/tutorials/first-cached-endpoint.md  a lesson that works end to end
```

Nothing was deleted. Each piece simply went where its reader is.
