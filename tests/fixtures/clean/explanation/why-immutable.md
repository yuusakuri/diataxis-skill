# Why deployments are immutable
The reason we chose immutable deployments is rollback safety.
Historically the system mutated servers in place, which made a trade-off
between speed and recoverability. We considered a hybrid alternative.
