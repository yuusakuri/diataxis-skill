# 12. One active signing key at a time

Status: accepted
Date: 2026-02-11

## Context

We considered keeping two active signing keys so rotation would need no
coordination window. Verifiers in the field cache JWKS for up to 10 minutes and
some vendored SDKs pick the first key in the document rather than matching on
`kid`.

## Decision

Exactly one key signs at a time. A second key may be published but not promoted.

## Consequences

Rotation needs a coordination window of one token lifetime. Vendored SDKs that
ignore `kid` keep working. If we later move to verifiers we control, this
decision is worth revisiting.
