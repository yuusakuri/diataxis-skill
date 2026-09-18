#!/usr/bin/env python3
"""Repository-specific checks.

Agent Skills spec conformance is not checked here — `claude plugin validate`
does that, and it is the authority on the format. What this script checks is
what is specific to this repository and would otherwise break silently: files
the skill points at, agreement between the two manifests, relative links in the
Markdown, and the shape of the eval suite.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
EVALS = ROOT / "evals"

# Files SKILL.md sends the agent to. Losing one is not a syntax error; the
# agent simply follows a path that is not there.
REQUIRED_BUNDLED = [
    "references/four-modes.md",
    "references/how-to-restructure.md",
]

# SKILL.md is the entry point, not the manual. Anything longer than this belongs
# in references/, which the agent reads only when it needs it.
MAX_BODY_LINES = 120

LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
BUNDLED_REF_RE = re.compile(r"`((?:references|scripts|assets)/[\w./-]+)`")


def skill_dirs() -> list[Path]:
    return sorted(p.parent for p in SKILLS.glob("*/SKILL.md"))


def check_bundled_files(errors: list[str]) -> None:
    for skill in skill_dirs():
        body = (skill / "SKILL.md").read_text(encoding="utf-8")
        for rel in REQUIRED_BUNDLED:
            if not (skill / rel).is_file():
                errors.append(f"{skill.name}: missing bundled file {rel}")
        for rel in BUNDLED_REF_RE.findall(body):
            if not (skill / rel).exists():
                errors.append(f"{skill.name}: SKILL.md points at missing file {rel}")
        lines = body.count("\n")
        if lines > MAX_BODY_LINES:
            errors.append(f"{skill.name}: SKILL.md is {lines} lines, over {MAX_BODY_LINES}")


def check_manifests(errors: list[str]) -> None:
    plugin_path = ROOT / ".claude-plugin" / "plugin.json"
    market_path = ROOT / ".claude-plugin" / "marketplace.json"
    try:
        plugin = json.loads(plugin_path.read_text(encoding="utf-8"))
        market = json.loads(market_path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError) as e:
        errors.append(f"manifest unreadable — {e}")
        return

    entries = {p.get("name"): p for p in market.get("plugins", [])}
    entry = entries.get(plugin.get("name"))
    if entry is None:
        errors.append(
            f"marketplace.json has no entry for plugin {plugin.get('name')!r}"
        )
        return
    for field in ("version", "license", "homepage", "repository"):
        if plugin.get(field) != entry.get(field):
            errors.append(
                f"{field}: plugin.json {plugin.get(field)!r} "
                f"!= marketplace.json {entry.get(field)!r}"
            )


def check_links(errors: list[str]) -> None:
    for md in ROOT.rglob("*.md"):
        if ".git" in md.parts or "results" in md.parts:
            continue
        for target in LINK_RE.findall(md.read_text(encoding="utf-8")):
            if target.startswith(("http://", "https://", "#", "mailto:")):
                continue
            path = (md.parent / target.split("#", 1)[0]).resolve()
            if not path.exists():
                errors.append(f"{md.relative_to(ROOT)}: broken link {target}")


def check_evals(errors: list[str]) -> None:
    if not EVALS.is_dir():
        errors.append("evals/ missing")
        return
    if (SKILLS / "diataxis" / "evals").exists():
        errors.append("eval cases must not live under skills/ — the runner refuses them")

    cases = [c for c in sorted(EVALS.glob("*/*/")) if "results" not in c.parts]
    if not cases:
        errors.append("evals/ holds no cases")
    for case in cases:
        rel = case.relative_to(ROOT)
        if not (case / "prompt.md").is_file() and not (case / "case.yaml").is_file():
            errors.append(f"{rel}: neither prompt.md nor case.yaml")
        graders = list((case / "graders").glob("*.md"))
        if not graders:
            errors.append(f"{rel}: no graders")
        for grader in graders:
            text = grader.read_text(encoding="utf-8")
            if not text.startswith("---\n") or "\ntype:" not in text.split("\n---", 1)[0]:
                errors.append(f"{rel}/graders/{grader.name}: no type in frontmatter")
        case_yaml = case / "case.yaml"
        if case_yaml.is_file():
            text = case_yaml.read_text(encoding="utf-8")
            m = re.search(r"^name:\s*(\S+)", text, re.M)
            if m and m.group(1) != case.name:
                errors.append(f"{rel}: case.yaml name {m.group(1)!r} != directory name")
            s = re.search(r"scaffold_script:\s*(\S+)", text)
            if s and not (case / s.group(1)).is_file():
                errors.append(f"{rel}: scaffold_script {s.group(1)} missing")


def main() -> int:
    errors: list[str] = []
    if not skill_dirs():
        print("error: no skills found under skills/", file=sys.stderr)
        return 1
    check_bundled_files(errors)
    check_manifests(errors)
    check_links(errors)
    check_evals(errors)

    if errors:
        print(f"FAIL — {len(errors)} problem(s):", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    cases = [c for c in EVALS.glob("*/*/") if "results" not in c.parts]
    print(f"OK — {len(skill_dirs())} skill(s), {len(cases)} eval case(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
