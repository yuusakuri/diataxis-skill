---
type: llm
weight: 1
---

Judge only what the response does with this line from the reference page:
"Never call this against `default` during business hours."

That line is advice about when to run an operation, not a fact about what the
endpoint does.

PASS if the response moves it out of the reference and into the how-to guide
alongside the purge step, or otherwise treats it as belonging with the
procedure rather than with the endpoint's description.

FAIL if the response keeps it in the reference as an API fact, or deletes it
altogether.
