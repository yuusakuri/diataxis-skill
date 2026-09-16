#!/usr/bin/env python3
"""Grade an agent's answers against what the skill requires of them.

Each assertion states a behaviour the skill asks for: citing the lines a
judgement rests on, the subtle tutorial/how-to call, the rule against building
pages to fill empty modes, the restructuring procedure, the deferral boundary,
and not inventing pages nobody asked for.

A failing assertion is a gap between what SKILL.md says and what the agent did.
"""
from __future__ import annotations
import json, re
from pathlib import Path

import os, sys

# Directory holding the answers, laid out as <eval>/outputs/answer.md.
# Pass it as the first argument, or set DIATAXIS_EVAL_RUNS.
WS = Path(sys.argv[1] if len(sys.argv) > 1
          else os.environ.get("DIATAXIS_EVAL_RUNS", "evals/runs"))

def load(ev):
    p = WS / ev / "outputs" / "answer.md"
    return p.read_text(encoding="utf-8").lower() if p.is_file() else None

A = {
 "eval-0-restructure": [
  ("cites concrete line ranges as evidence",
   lambda t: len(re.findall(r"lines?\s*\d+\s*[-–]\s*\d+", t)) >= 3),
  ("classifies setup.md as a tutorial (not how-to) - the subtle call",
   lambda t: bool(re.search(r"setup\.md[^\n]{0,300}?tutorial|tutorial[^\n]{0,300}?setup\.md", t))
             and not bool(re.search(r"setup\.md is a how-to", t))),
  ("refuses to create an empty/placeholder tutorial page",
   lambda t: bool(re.search(r"empty (director|tutorial|mode)|don'?t create|not create|"
                            r"advertis\w+ a (lesson|tutorial) that", t))),
  ("gives a move procedure (separate commits / links / redirects)",
   lambda t: bool(re.search(r"commit", t)) and
             bool(re.search(r"redirect|stub|inbound link|grep", t))),
  ("warns the subject-named file will re-accumulate junk",
   lambda t: bool(re.search(r"magnet|attract|accumulat|becomes? the next|grow", t))),
 ],
 "eval-1-diagnose": [
  ("cites concrete line ranges as evidence",
   lambda t: len(re.findall(r"lines?\s*\d+\s*[-–]\s*\d+", t)) >= 3),
  ("names all four modes present in the one page", 
   lambda t: all(re.search(rf"\b{m}s?\b", t) for m in ("tutorial","how-to","reference","explanation"))),
  ("does not offer 'add headings' as an acceptable fix",
   lambda t: not bool(re.search(r"add (four )?(`?##`?|h2|headings)|just add headings", t))),
  ("gives an incremental restructuring plan",
   lambda t: bool(re.search(r"step 1|first,|one commit|incremental|one page at a time", t))),
 ],
 "eval-3-no-invented-pages": [
  ("does not create a tutorial page",
   lambda t: not bool(re.search(r"(create|add|write|new|introduce)\s+(an?\s+)?(`?tutorials?/|tutorial page|tutorial\b)", t))),
  ("does not create an explanation page",
   lambda t: not bool(re.search(r"(create|add|write|new|introduce)\s+(an?\s+)?(`?explanations?/|explanation page)", t))),
  ("says the absent modes are not a gap here",
   lambda t: bool(re.search(r"not (a )?gap|nothing here (asks|needs|calls)|no reader|don'?t (add|create)|"
                            r"only (add|create) .{0,40}(when|if) (a reader|someone)", t))),
  ("files both pages as how-to guides",
   lambda t: bool(re.search(r"install\.md[^\n]{0,200}how-?to", t))
             and bool(re.search(r"configure\.md[^\n]{0,200}how-?to", t))),
 ],
 "eval-2-defer-adr": [
  ("defers: names ADR as the artefact", lambda t: bool(re.search(r"\badr\b|decision record", t))),
  ("does not force the four modes", 
   lambda t: not bool(re.search(r"this (is|belongs in) an? (tutorial|reference|how-to)\b", t))),
  ("still names explanation as the legitimate follow-on",
   lambda t: bool(re.search(r"explanation", t))),
  ("points at an existing ADR convention rather than inventing one",
   lambda t: bool(re.search(r"existing convention|match (any )?existing|docs?/(decisions?|adr)", t))),
 ],
}

rows = []
for ev, asserts in A.items():
    t = load(ev)
    rows.append({"eval": ev,
                 "results": None if t is None else [(n, bool(f(t))) for n, f in asserts]})

print(f"{'eval':<28} {'passed':>10}")
print("-" * 40)
total = count = 0
for r in rows:
    res = r["results"]
    if res is None:
        print(f"{r['eval']:<28} {'no answer':>10}")
        continue
    passed = sum(p for _, p in res)
    total += passed
    count += len(res)
    print(f"{r['eval']:<28} {f'{passed}/{len(res)}':>10}")
print("-" * 40)
print(f"{'TOTAL':<28} {f'{total}/{count}':>10}")

print("\nper assertion:")
for r in rows:
    print(f"\n  {r['eval']}")
    if r["results"] is None:
        print("    no answer found")
        continue
    for name, ok in r["results"]:
        print(f"    {'PASS' if ok else 'FAIL':<5} {name}")

missing = [r["eval"] for r in rows if r["results"] is None]
json.dump({r["eval"]: r["results"] for r in rows},
          open(WS / "grading.json", "w"), indent=2, default=str)
sys.exit(1 if missing or total < count else 0)
