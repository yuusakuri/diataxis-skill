# How to refund a charge

Use this when a customer has been charged for an order that will not ship.

1. Find the charge: `ledger charges find --order <id>`.
2. Refund it: `ledger charges refund <charge-id> --reason not_shipped`.
3. Confirm the state is `refunded`.

If the charge has not settled yet, void it instead with `ledger charges void`.
A void costs nothing; a refund on a settled charge does not return the fee.

If the order used store credit, refund the credit portion separately in the
admin console — the CLI only touches card charges.
