# `audit_docs.py` reference

Scans a documentation tree and reports pages that sit outside the four Diátaxis modes, or that carry material from a mode they do not belong to.

```
python3 audit_docs.py ROOT [--json] [--strict]
```

## Arguments

| Argument | Description |
|---|---|
| `ROOT` | Directory to scan. Required. |

## Options

| Option | Description |
|---|---|
| `--json` | Print machine-readable output: summary, findings, and per-page signal counts. |
| `--strict` | Exit 1 if a warning was reported. An `info` finding does not fail the run. For CI. |

## Exit codes

| Code | Meaning |
|---|---|
| 0 | Completed. With `--strict`, also means no warnings. |
| 1 | With `--strict`, at least one warning. |
| 2 | `ROOT` is not a directory. |

## Files scanned

`.md`, `.rst` and `.mdx` files, at any depth below `ROOT`.

## Directory names recognised as modes

| Mode | Directory names |
|---|---|
| tutorial | `tutorials`, `tutorial`, `getting-started`, `learn` |
| how-to | `how-to`, `how-to-guides`, `howto`, `guides`, `recipes` |
| reference | `reference`, `api`, `api-reference` |
| explanation | `explanation`, `explanations`, `discussion`, `concepts`, `background`, `topics` |

A page takes the mode of the first recognised directory in its path.

## JSON output

```json
{
  "root": "docs",
  "summary": {
    "pages": 4,
    "modes_present": ["explanation", "how-to", "reference", "tutorial"],
    "outside_modes": 0,
    "outside_mode_paths": [],
    "findings": 1
  },
  "findings": [
    {
      "kind": "mode-mixing",
      "severity": "warning",
      "path": "reference/cli.md",
      "message": "reference page carrying 6 action signals. …",
      "evidence": ["line 6", "line 7"],
      "mode": "reference",
      "intruder": "action"
    }
  ],
  "pages": [
    {"path": "reference/cli.md", "mode": "reference",
     "counts": {"action": 6, "reference": 4, "explanation": 0, "teaching": 0},
     "lines": {"action": [6, 7, 8, 9, 10, 12]}}
  ]
}
```

## Requirements

Python 3.9 or later.
No third-party packages.
