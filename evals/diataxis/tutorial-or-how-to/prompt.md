---
max_turns: 15
timeout_seconds: 420
allowed_tools: [Read, Glob, Grep, Skill]
tags: [classification]
expected_outcome: >-
  first-flag.md is a tutorial even though it states prerequisites; rollout.md is
  a how-to guide. The stated prerequisites are not treated as disqualifying.
---

I have two pages in docs/: first-flag.md and rollout.md. Which of the four
documentation types is each one, and why? One of my reviewers says
first-flag.md can't be a tutorial because it assumes you already have an
account and the CLI installed — is that right?
