---
type: llm
weight: 2
---

The response classifies two documentation pages.

PASS if ALL of these hold:
- first-flag.md is classified as a tutorial.
- rollout.md is classified as a how-to guide.
- The reviewer's claim is rejected: the response says stated prerequisites do
  not stop a page from being a tutorial (a tutorial needs its starting
  conditions stated, not absent).

FAIL if ANY of these hold:
- first-flag.md is classified as a how-to guide, reference or explanation.
- The response agrees that prerequisites, prior knowledge or an existing
  account disqualify a page from being a tutorial.
- The response says a tutorial requires a complete beginner, a blank machine,
  or starting from nothing.
