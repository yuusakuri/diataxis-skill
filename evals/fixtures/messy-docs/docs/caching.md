# Caching

Caching exists because our origin is slow and traffic is spiky. We considered a
CDN-only approach but rejected it because invalidation latency was unacceptable
for the pricing pages. Historically we cached in the app tier.

To enable caching:
1. Set CACHE=1 in the environment
2. Restart the workers
3. Verify with `app cache status`

| Option | Type | Default | Description |
|---|---|---|---|
| `CACHE_TTL` | int | 300 | Seconds to retain an entry |
| `CACHE_SIZE` | int | 1000 | Max entries |
| `CACHE_MODE` | string | lru | Eviction policy |

In this guide you will learn to build your first cached endpoint. By the end you
will have a working cache. Let's start by creating a handler.
