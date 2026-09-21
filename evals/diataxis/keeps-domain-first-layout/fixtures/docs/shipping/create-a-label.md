# How to create a shipping label

Use this when an order is packed and ready to leave the warehouse.

1. `ledger ship label create --order <id> --carrier <carrier>`.
2. Print the returned PDF.

If the destination is outside the carrier's zone, the command fails with
`zone_unsupported`. Pick another carrier from `ledger ship carriers`.
