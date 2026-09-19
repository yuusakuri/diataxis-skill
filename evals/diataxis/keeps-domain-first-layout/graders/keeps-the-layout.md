---
type: llm
weight: 2
---

PASS if the response keeps the existing per-area layout (billing/, shipping/)
as its recommendation, and says in some form that Diátaxis modes classify what
a page is for and do not require a particular directory structure.

FAIL if the recommended plan relocates the pages into top-level mode
directories (docs/tutorials/, docs/how-to/, docs/reference/, docs/explanation/),
or if the response treats the per-area layout as itself the problem to fix.
A restructure mentioned only as an option the author may decline, after saying
the current layout works, does not fail.
