# Rolling a flag out to a percentage of traffic

Use this when a flag is ready for real users but you do not want it on for
everyone at once.

1. Put the flag into percentage mode:

   ```bash
   flagctl set checkout-banner --rollout 5
   ```

2. Watch the error rate for the cohort in the dashboard.
3. Raise the percentage in steps you are willing to roll back from.

If your project uses sticky bucketing, set `--bucket-by user_id` as well, or the
same user will see the flag flip between requests.

If you are on a self-hosted collector, percentages are evaluated in the SDK
rather than the service, so a rollout change takes effect only after the SDK
refreshes its cache (60 seconds by default).

To roll back, set `--rollout 0`. Do not delete the flag: deleting it makes the
code path fall through to the default, which is not the same thing.
