---
max_turns: 15
timeout_seconds: 420
allowed_tools: [Read, Glob, Grep, Skill]
tags: [mode-mixing]
expected_outcome: >-
  queues.md is split. restore-a-snapshot.md is left as one how-to guide,
  intro sentence and variations included.
---

Two pages under docs/. Which of them need splitting up, and which are fine as
they are?
