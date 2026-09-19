---
type: llm
weight: 2
---

PASS if the proposed layout contains only pages that exist: no empty
tutorials/, how-to/ or explanation/ directory, no placeholder or stub page for
a mode with no content, and no index or landing page listing modes that have
nothing in them. Saying which modes are absent, and that they should be written
only when a reader needs one, is fine and does not fail.

FAIL if the layout creates a directory, an index row or a page for a mode that
has no content, or if the response writes a tutorial or explanation nobody
asked for.
