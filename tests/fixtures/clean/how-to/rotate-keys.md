# How to rotate API keys
1. Run `app keys rotate --env prod`
2. Update the secret in your deployment
3. Restart the workers
If rotation fails mid-way, re-run the command; it is idempotent.
