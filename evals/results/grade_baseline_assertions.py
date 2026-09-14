#!/usr/bin/env python3
"""Grade the Diátaxis eval outputs against objective assertions.

Every assertion is checked programmatically so the result is reproducible and
not a matter of my opinion about my own skill.
"""
from __future__ import annotations
import json, re, sys
from pathlib import Path

WS = Path("/home/user/diataxis-workspace/iteration-1")
MODES = ("tutorial", "how-to", "reference", "explanation")


def load(eval_dir: str, config: str) -> str | None:
    p = WS / eval_dir / config / "outputs" / "answer.md"
    return p.read_text(encoding="utf-8").lower() if p.is_file() else None


def names_all_modes(t: str) -> bool:
    return all(re.search(rf"\b{re.escape(m)}s?\b", t) for m in MODES)


def count_modes(t: str) -> int:
    return sum(bool(re.search(rf"\b{re.escape(m)}s?\b", t)) for m in MODES)


ASSERTIONS = {
    "eval-0-restructure": [
        ("names all four Diátaxis modes", names_all_modes),
        ("proposes splitting caching.md into multiple destinations",
         lambda t: "caching.md" in t and (t.count("caching") >= 3) and
                   bool(re.search(r"split|four|separate|break (it |this )?(up|apart)", t))),
        ("routes api.md to reference",
         lambda t: bool(re.search(r"api\.md[^\n]{0,200}?reference|reference[^\n]{0,200}?api\.md", t))),
        ("routes setup.md to tutorial or how-to",
         lambda t: bool(re.search(r"setup\.md[^\n]{0,200}?(tutorial|how-to)|"
                                  r"(tutorial|how-to)[^\n]{0,200}?setup\.md", t))),
        ("justifies placement by reader need, not topic",
         lambda t: bool(re.search(r"reader|user needs?|someone who|learning|at work|"
                                  r"look(ing)? up|beginner", t))),
        ("proposes a concrete directory layout",
         lambda t: bool(re.search(r"docs?/\s*(tutorials?|how-to|reference|explanation)|"
                                  r"(tutorials?|how-to|reference|explanation)/", t))),
    ],
    "eval-1-diagnose": [
        ("diagnoses mixing of modes rather than prose quality",
         lambda t: bool(re.search(r"four (different )?(things|modes|kinds|documents)|"
                                  r"mode[- ]mixing|mixes|mixing|doing (two|several|multiple|four)|"
                                  r"serves? (two|several|multiple|different) (readers?|audiences?|needs?)", t))),
        ("names at least three of the four modes", lambda t: count_modes(t) >= 3),
        ("proposes splitting the page",
         lambda t: bool(re.search(r"split|separate|break (it |this )?(up|apart)|four (files|pages)", t))),
        ("attributes the problem to structure, not accuracy",
         lambda t: bool(re.search(r"accurate|accuracy|correct", t)) and
                   bool(re.search(r"structure|organis|organiz|where|find", t))),
    ],
    "eval-2-defer-adr": [
        ("recognises this as a decision record / ADR",
         lambda t: bool(re.search(r"\badr\b|architecture decision record|decision record", t))),
        ("does not force it into the four modes as the answer",
         lambda t: not bool(re.search(r"this (is|belongs in) (a )?(tutorial|reference|how-to)\b", t))),
        ("mentions a dedicated location such as docs/decisions or docs/adr",
         lambda t: bool(re.search(r"docs?/(decisions?|adr)|adr/|decisions?/", t))),
    ],
}


def main() -> int:
    results = {}
    for eval_dir, asserts in ASSERTIONS.items():
        results[eval_dir] = {}
        for config in ("with_skill", "without_skill"):
            text = load(eval_dir, config)
            if text is None:
                results[eval_dir][config] = None
                continue
            checks = []
            for name, fn in asserts:
                try:
                    passed = bool(fn(text))
                except Exception as e:  # a broken assertion must not look like a fail
                    passed = False
                    name += f" (assertion error: {e})"
                checks.append({"text": name, "passed": passed, "evidence": ""})
            results[eval_dir][config] = {
                "passed": sum(c["passed"] for c in checks),
                "total": len(checks),
                "expectations": checks,
                "chars": len(text),
            }

    (WS / "grading.json").write_text(json.dumps(results, indent=2), encoding="utf-8")

    print(f"{'eval':<24} {'with skill':>12} {'baseline':>12}")
    print("-" * 50)
    tw = tb = nw = nb = 0
    for ev, cfgs in results.items():
        w, b = cfgs.get("with_skill"), cfgs.get("without_skill")
        ws = f"{w['passed']}/{w['total']}" if w else "—"
        bs = f"{b['passed']}/{b['total']}" if b else "—"
        if w: tw += w["passed"]; nw += w["total"]
        if b: tb += b["passed"]; nb += b["total"]
        print(f"{ev:<24} {ws:>12} {bs:>12}")
    print("-" * 50)
    print(f"{'TOTAL':<24} {f'{tw}/{nw}':>12} {f'{tb}/{nb}':>12}")

    print("\nper-assertion detail (with_skill / baseline):")
    for ev, cfgs in results.items():
        print(f"\n  {ev}")
        w, b = cfgs.get("with_skill"), cfgs.get("without_skill")
        n = len(ASSERTIONS[ev])
        for i in range(n):
            name = ASSERTIONS[ev][i][0]
            wm = "PASS" if w and w["expectations"][i]["passed"] else ("FAIL" if w else "—")
            bm = "PASS" if b and b["expectations"][i]["passed"] else ("FAIL" if b else "—")
            print(f"    {wm:<5} {bm:<5} {name}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
