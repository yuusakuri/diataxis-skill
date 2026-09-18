# Tiles API

The tiles service renders map tiles from a style bundle.

## `GET /tiles/{z}/{x}/{y}.png`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `z` | int | — | Zoom level, 0 to 22 |
| `x` | int | — | Column index at this zoom level |
| `y` | int | — | Row index at this zoom level |
| `style` | string | `default` | Name of a published style bundle |
| `scale` | int | `1` | Pixel density multiplier, 1 or 2 |

Requires a bearer token with the `tiles:read` scope. Requests without one
return `401` and are not counted against the rate limit.

Example:

```bash
curl -H "Authorization: Bearer $TOKEN" \
  "https://tiles.example.com/tiles/12/2048/1362.png?scale=2"
```

Returns `422` when `z` is outside 0–22, and `404` when the style bundle exists
but has no tile at that coordinate.

## `POST /tiles/purge`

| Parameter | Type | Default | Description |
|---|---|---|---|
| `style` | string | — | Style bundle to purge |
| `all` | bool | `false` | Purge every zoom level |

Warning: `all=true` drops every rendered tile for the bundle. There is no undo,
and the first requests after a purge are served from a cold renderer.

Never call this against `default` during business hours.

## Regenerating tiles after a style change

1. Publish the new style bundle with `tilectl publish <bundle>`.
2. Wait for `tilectl status` to report `ready`.
3. Purge the old tiles with `POST /tiles/purge`.
4. Warm the common zoom levels with `tilectl warm --z 8-12`.
5. Check a handful of tiles in the staging viewer before pointing production at
   the new bundle.
