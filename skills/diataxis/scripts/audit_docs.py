#!/usr/bin/env python3
"""Audit a documentation tree against the Diátaxis framework.

Diátaxis separates documentation into four modes, because each serves a
different user need:

    informs action    + acquisition of skill  -> tutorial
    informs action    + application of skill  -> how-to guide
    informs cognition + application of skill  -> reference
    informs cognition + acquisition of skill  -> explanation

The characteristic failure is not "missing docs" but *mode-mixing*: a
reference page that drifts into step-by-step instruction, a tutorial that
swells into an exhaustive option table. Mixed pages serve nobody, because a
reader arrives in one mode and is handed another.

This script finds candidates for that failure. It reports evidence with line
numbers; it does not decide. Classification is a judgement about what the
reader needs, and a regex cannot make it — so treat every finding as a
question to answer, not a verdict to obey.

Usage:
    python3 audit_docs.py docs/
    python3 audit_docs.py docs/ --json
    python3 audit_docs.py docs/ --strict      # exit 1 if any warning

No third-party dependencies.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path

# Directory names conventionally used for each mode. Plural and singular are
# both common in the wild, as are a few widespread synonyms.
MODE_DIRS = {
    "tutorial": {"tutorials", "tutorial", "getting-started", "learn"},
    "how-to": {"how-to", "how-to-guides", "howto", "guides", "recipes"},
    "reference": {"reference", "api", "api-reference"},
    "explanation": {"explanation", "explanations", "discussion", "concepts",
                    "background", "topics"},
}

MODE_OF_DIR = {d: mode for mode, dirs in MODE_DIRS.items() for d in dirs}

# Files that describe the tree rather than sitting inside a mode.
INDEX_NAMES = {"index.md", "readme.md", "index.rst", "readme.rst", "_index.md"}

# --- Signals -----------------------------------------------------------------
# Each signal is evidence that a passage is doing a particular kind of work.
# They are deliberately shallow and explainable: a reader should be able to look
# at a flagged line and immediately agree or disagree.

STEP_HEADING = re.compile(r"^#{1,6}\s*(step\s*\d+|\d+[.)]\s+\S)", re.I)
ORDERED_STEP = re.compile(r"^\s{0,3}\d+[.)]\s+[A-Z`]")
IMPERATIVE_START = re.compile(
    r"^\s{0,3}(?:[-*]|\d+[.)])\s+(run|open|click|create|add|install|set|edit|"
    r"copy|paste|navigate|select|type|enter|save|restart|deploy|choose|download|"
    r"configure|remove|delete)\b",
    re.I,
)
SHELL_FENCE = re.compile(r"^```\s*(bash|sh|shell|console|zsh|powershell)\b", re.I)

# Reference work: exhaustive, lookup-shaped, parameter-by-parameter.
TABLE_ROW = re.compile(r"^\s*\|.*\|\s*$")
REFERENCE_TABLE_HEADER = re.compile(
    r"^\s*\|[^|]*\b(option|options|parameter|parameters|argument|arguments|"
    r"field|fields|flag|flags|type|types|default|defaults|returns|property|"
    r"properties|method|methods|attribute|attributes|column|columns)\b",
    re.I,
)
FLAG_DEFINITION = re.compile(r"^\s*[-*]\s+`--?[a-z0-9][\w-]*`")
SIGNATURE_FENCE = re.compile(r"^```\s*(python|typescript|ts|javascript|js|go|"
                             r"rust|java|json|yaml|http)\b", re.I)

# Explanation work: reasons, alternatives, history, trade-offs.
EXPLANATION_WORD = re.compile(
    r"\b(why|because|rationale|trade-?off|trade-?offs|historically|"
    r"design decision|alternative|alternatives|we chose|considered|"
    r"in theory|conceptually|the reason)\b",
    re.I,
)

# Teaching work: second-person guidance through a first experience.
TEACHING_PHRASE = re.compile(
    r"\b(in this tutorial|you will learn|by the end|let's|lets |we will|"
    r"you should see|congratulations|first,? we|now that you)\b",
    re.I,
)

SIGNAL_KINDS = ("action", "reference", "explanation", "teaching")

# Which foreign signals most damage which mode, and the wording to use.
# Keyed by (mode, foreign_signal).
MIXING_RULES = {
    ("reference", "action"):
        "Reference is for looking things up mid-task; step-by-step instruction "
        "belongs in a how-to guide. A reader scanning for a parameter has to "
        "read past a procedure to find it.",
    ("reference", "explanation"):
        "Reference describes the machinery, not the reasoning. Discussion of "
        "why the design is this way belongs in explanation.",
    ("tutorial", "reference"):
        "A tutorial is a lesson the reader completes; exhaustive option tables "
        "interrupt it. Link to reference instead of inlining it.",
    ("tutorial", "explanation"):
        "A tutorial teaches by doing. Extended discussion of why breaks the "
        "flow — move it to explanation and link.",
    ("how-to", "teaching"):
        "A how-to guide serves someone already at work who knows what they "
        "want. Teaching asides ('in this tutorial', 'you will learn') mean it "
        "is drifting into a tutorial.",
    ("how-to", "reference"):
        "A how-to guide shows a path through a problem, not a complete "
        "catalogue. Exhaustive tables belong in reference.",
    ("explanation", "action"):
        "Explanation illuminates; it does not instruct. Procedures absorbed "
        "into explanation hide from the readers who need them.",
}

# A page needs enough foreign material to be worth flagging. Below this it is
# a passing mention, which every mode is allowed.
MIN_FOREIGN_HITS = 3


@dataclass
class Finding:
    kind: str
    severity: str
    path: str
    message: str
    evidence: list[str] = field(default_factory=list)
    # The mode this finding concerns, so consumers can act on it without
    # parsing the prose message.
    mode: str | None = None
    intruder: str | None = None


@dataclass
class PageProfile:
    path: str
    mode: str | None
    counts: dict[str, int]
    lines: dict[str, list[int]]


def classify_dir(parts: tuple[str, ...]) -> str | None:
    """Return the mode a path sits in, by its first recognised directory."""
    for part in parts:
        mode = MODE_OF_DIR.get(part.lower())
        if mode:
            return mode
    return None


def profile_page(path: Path) -> PageProfile:
    """Count the kinds of work a page is doing, remembering where."""
    counts = {k: 0 for k in SIGNAL_KINDS}
    lines: dict[str, list[int]] = {k: [] for k in SIGNAL_KINDS}

    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        text = ""

    in_fence = False
    fence_kind: str | None = None
    table_is_reference = False

    for n, raw in enumerate(text.splitlines(), start=1):
        line = raw.rstrip()

        if line.startswith("```"):
            if in_fence:
                in_fence, fence_kind = False, None
            else:
                in_fence = True
                if SHELL_FENCE.match(line):
                    fence_kind = "action"
                elif SIGNATURE_FENCE.match(line):
                    fence_kind = "reference"
                else:
                    fence_kind = None
                if fence_kind:
                    counts[fence_kind] += 1
                    lines[fence_kind].append(n)
            continue

        # Inside a fence the prose rules do not apply; the fence itself was
        # already counted.
        if in_fence:
            continue

        if STEP_HEADING.match(line) or ORDERED_STEP.match(line) or IMPERATIVE_START.match(line):
            counts["action"] += 1
            lines["action"].append(n)

        if REFERENCE_TABLE_HEADER.match(line):
            table_is_reference = True
            counts["reference"] += 1
            lines["reference"].append(n)
        elif TABLE_ROW.match(line):
            if table_is_reference and not re.match(r"^\s*\|[\s:|-]+\|\s*$", line):
                counts["reference"] += 1
                lines["reference"].append(n)
        else:
            table_is_reference = False

        if FLAG_DEFINITION.match(line):
            counts["reference"] += 1
            lines["reference"].append(n)

        if EXPLANATION_WORD.search(line):
            counts["explanation"] += 1
            lines["explanation"].append(n)

        if TEACHING_PHRASE.search(line):
            counts["teaching"] += 1
            lines["teaching"].append(n)

    return PageProfile(str(path), None, counts, lines)


def evidence_for(profile: PageProfile, kind: str, limit: int = 4) -> list[str]:
    nums = profile.lines[kind][:limit]
    more = len(profile.lines[kind]) - len(nums)
    out = [f"line {n}" for n in nums]
    if more > 0:
        out.append(f"+{more} more")
    return out


def audit(root: Path) -> tuple[list[Finding], list[PageProfile], dict]:
    findings: list[Finding] = []
    profiles: list[PageProfile] = []

    pages = sorted(
        p for p in root.rglob("*")
        if p.is_file() and p.suffix.lower() in {".md", ".rst", ".mdx"}
    )

    modes_present: set[str] = set()
    outside: list[Path] = []

    for page in pages:
        rel = page.relative_to(root)
        mode = classify_dir(rel.parts[:-1])
        prof = profile_page(page)
        prof.path = str(rel)
        prof.mode = mode
        profiles.append(prof)

        if mode:
            modes_present.add(mode)
        elif rel.name.lower() not in INDEX_NAMES:
            outside.append(rel)

    # --- structural findings ---
    # A page outside the mode directories is not examined and not reported.
    # The tool cannot know what a directory is for, and a project's docs tree
    # answers to more than this framework: specifications, decision records,
    # runbooks, translations, per-version trees. Naming those a defect would
    # make the tool an argument about folder names rather than about whether
    # a page serves its reader. The count is in the summary.

    for mode in ("tutorial", "how-to", "reference", "explanation"):
        if mode not in modes_present:
            findings.append(Finding(
                kind="missing-mode",
                severity="info",
                path=str(root),
                mode=mode,
                message=(f"No {mode} content found. A missing mode is not "
                         f"automatically wrong, but it is usually a gap: it "
                         f"means one whole category of reader need is "
                         f"unserved."),
            ))

    # --- mode-mixing findings ---
    for prof in profiles:
        if not prof.mode:
            continue
        native = {"tutorial": "teaching", "how-to": "action",
                  "reference": "reference", "explanation": "explanation"}[prof.mode]
        native_count = prof.counts[native]
        if prof.mode == "tutorial":
            native_count = max(native_count, prof.counts["action"])

        for kind in SIGNAL_KINDS:
            rule = MIXING_RULES.get((prof.mode, kind))
            if not rule:
                continue
            hits = prof.counts[kind]
            if hits < MIN_FOREIGN_HITS:
                continue
            # Allow foreign material that is clearly incidental next to a
            # strong native signal.
            if native_count >= hits * 2:
                continue
            findings.append(Finding(
                kind="mode-mixing",
                severity="warning",
                path=prof.path,
                message=f"{prof.mode} page carrying {hits} {kind} signals. {rule}",
                evidence=evidence_for(prof, kind),
                mode=prof.mode,
                intruder=kind,
            ))

    summary = {
        "pages": len(profiles),
        "modes_present": sorted(modes_present),
        "outside_modes": len(outside),
        "outside_mode_paths": [str(r) for r in outside],
        "findings": len(findings),
    }
    return findings, profiles, summary


def render(findings: list[Finding], summary: dict, root: Path) -> str:
    out = [f"Diátaxis audit: {root}", ""]
    out.append(f"{summary['pages']} pages, "
               f"modes present: {', '.join(summary['modes_present']) or 'none'}")
    if summary.get("outside_modes"):
        out.append(f"{summary['outside_modes']} page(s) outside the mode "
                   f"directories, not examined.")
    out.append("")

    if not findings:
        out.append("No findings. Every page sits in a mode and none of them "
                   "are visibly doing two jobs at once.")
        return "\n".join(out)

    order = {"warning": 0, "info": 1}
    for f in sorted(findings, key=lambda f: (order.get(f.severity, 2), f.path)):
        out.append(f"[{f.severity}] {f.path}")
        out.append(f"  {f.message}")
        if f.evidence:
            out.append(f"  evidence: {', '.join(f.evidence)}")
        out.append("")

    out.append(f"{summary['findings']} finding(s). These are questions, not "
               f"verdicts — confirm each against what the reader actually needs.")
    return "\n".join(out)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("root", help="documentation directory to audit")
    ap.add_argument("--json", action="store_true", dest="as_json",
                    help="machine-readable output")
    ap.add_argument("--strict", action="store_true",
                    help="exit 1 if there is any finding")
    args = ap.parse_args()

    root = Path(args.root).expanduser()
    if not root.is_dir():
        print(f"error: {root} is not a directory", file=sys.stderr)
        return 2

    findings, profiles, summary = audit(root)

    if args.as_json:
        print(json.dumps({
            "root": str(root),
            "summary": summary,
            "findings": [asdict(f) for f in findings],
            "pages": [asdict(p) for p in profiles],
        }, indent=2))
    else:
        print(render(findings, summary, root))

    if args.strict and any(f.severity == "warning" for f in findings):
        return 1
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except BrokenPipeError:
        try:
            sys.stdout.close()
        finally:
            sys.exit(0)
