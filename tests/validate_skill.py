#!/usr/bin/env python3
"""Validate SKILL.md against the Agent Skills specification.

Spec: https://agentskills.io/specification

A malformed SKILL.md does not fail loudly at runtime — the skill simply never
triggers — so this runs in CI.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "diataxis" / "SKILL.md"

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
ALLOWED = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}


def main() -> int:
    errors: list[str] = []

    if not SKILL.is_file():
        print(f"error: {SKILL} missing", file=sys.stderr)
        return 1

    text = SKILL.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        print("error: no frontmatter fence", file=sys.stderr)
        return 1
    end = text.find("\n---\n", 3)
    if end == -1:
        print("error: frontmatter not closed", file=sys.stderr)
        return 1
    fm, body = text[4:end], text[end + 5:]

    # The frontmatter is YAML, so read it with a YAML parser. Reading it with
    # regular expressions accepts files no agent can load: an unquoted value
    # containing ": " parses as a nested mapping and the whole block fails.
    try:
        meta = yaml.safe_load(fm)
    except yaml.YAMLError as e:
        print(f"error: frontmatter is not valid YAML — {e}", file=sys.stderr)
        return 1
    if not isinstance(meta, dict):
        print("error: frontmatter is not a mapping", file=sys.stderr)
        return 1

    for k in meta:
        if k not in ALLOWED:
            errors.append(f"unknown frontmatter key {k!r}")

    name = meta.get("name")
    if not isinstance(name, str) or not name:
        errors.append("missing required field 'name'")
        name = ""
    else:
        if not NAME_RE.match(name):
            errors.append(f"name {name!r} must be lowercase alphanumeric with single hyphens")
        if len(name) > 64:
            errors.append(f"name is {len(name)} chars, max 64")
        if name != SKILL.parent.name:
            errors.append(f"name {name!r} != directory {SKILL.parent.name!r}")

    desc = meta.get("description")
    if not isinstance(desc, str) or not desc:
        errors.append("missing required field 'description'")
        desc = ""
    else:
        if not 1 <= len(desc) <= 1024:
            errors.append(f"description is {len(desc)} chars, must be 1-1024")
        if "use " not in desc.lower():
            errors.append("description should say when to use the skill")

    lines = body.count("\n")
    if lines > 500:
        errors.append(f"body is {lines} lines; spec recommends under 500")

    # Every referenced bundled file must exist, or the skill sends the agent
    # to a path that is not there.
    for ref in re.findall(r"`((?:references|scripts|assets)/[\w./-]+)`", body):
        if not (SKILL.parent / ref).exists():
            errors.append(f"SKILL.md references missing file: {ref}")

    for manifest in (ROOT / ".claude-plugin" / "plugin.json",
                     ROOT / ".claude-plugin" / "marketplace.json"):
        try:
            json.loads(manifest.read_text(encoding="utf-8"))
        except FileNotFoundError:
            errors.append(f"{manifest.relative_to(ROOT)}: missing")
        except json.JSONDecodeError as e:
            errors.append(f"{manifest.relative_to(ROOT)}: invalid JSON — {e}")

    if errors:
        print(f"FAIL — {len(errors)} problem(s):", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print(f"OK — SKILL.md valid ({lines} body lines, "
          f"description {len(desc)} chars)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
