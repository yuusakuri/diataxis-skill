---
type: llm
weight: 2
---

These four items are facts about the API itself:

- the `curl` usage example
- the `tiles:read` scope requirement
- the warning that `all=true` drops every tile with no undo
- the `401` / `422` / `404` error behaviour

PASS if the response keeps all four in the reference page. An item counts as
kept if the response says it stays, or if it appears in the proposed version of
the reference page.

FAIL if the response proposes deleting any of the four, or moving any of them
to another page — for example on the grounds that a reference must not
instruct, must not warn, or must be purely descriptive.

Ignore whatever the response does with the "never call this against `default`
during business hours" line. Another grader covers it.
