# `stitch.toml`

| Key | Type | Default | Description |
|---|---|---|---|
| `entry` | string | `src/main` | Entry point |
| `targets` | array | `["web"]` | Build targets |
| `minify` | bool | `true` | Minify output |
| `source_maps` | bool | `false` | Emit source maps |

Unknown keys are an error, not a warning. Paths are resolved relative to the
file, not to the working directory.
