---
type: llm
weight: 2
---

The reference page contains a `curl` example, a `tiles:read` scope requirement,
a warning that `all=true` is irreversible, a "never call this against `default`
during business hours" line, and `401` / `422` / `404` error behaviour.

PASS if the response keeps all five in the reference page. An item counts as
kept if the response says it stays, or if it appears in the proposed version of
the reference page.

FAIL if the response proposes deleting any of the five from the reference, or
moving any of them to another page — for example on the grounds that a
reference must not instruct, must not warn, or must be purely descriptive.
