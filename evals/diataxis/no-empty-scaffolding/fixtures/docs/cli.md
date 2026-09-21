# `stitch` command line

## `stitch build`

| Flag | Type | Default | Description |
|---|---|---|---|
| `--out` | path | `dist/` | Output directory |
| `--watch` | bool | `false` | Rebuild on change |
| `--jobs` | int | CPU count | Parallel workers |

Exits `2` when the manifest is missing, `3` on a compile error.

## `stitch check`

| Flag | Type | Default | Description |
|---|---|---|---|
| `--strict` | bool | `false` | Treat warnings as errors |

Prints nothing and exits `0` when the project is valid.
