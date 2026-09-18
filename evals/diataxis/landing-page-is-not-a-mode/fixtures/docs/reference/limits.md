# Limits

| Limit | Value |
|---|---|
| Events per device per minute | 600 |
| Payload size | 64 KiB |
| Retention | 30 days |
| Batch size | 500 events |

Exceeding the per-minute limit returns `429` with a `Retry-After` header.
