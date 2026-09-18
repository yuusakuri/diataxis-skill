# How billing works

A charge moves through three states: authorised, captured, settled. We separate
authorisation from capture because carriers can reject a shipment after payment
is taken, and refunding a settled charge costs us the interchange fee.

We considered capturing at authorisation time, which is simpler, and rejected it
for that reason. The cost of a same-day reversal is what drives the design here,
not the payment provider's API.
