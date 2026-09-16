#!/usr/bin/env python3
"""Discriminating assertions: what does the SKILL add over a model that
already knows Diátaxis?

The assertions in grade_baseline_assertions.py passed identically with and
without the skill, so they measured the model's prior knowledge of Diátaxis
rather than the skill. These target what the skill actually supplies: citing
the lines a judgement rests on, the subtle tutorial/how-to call, the rule
against building pages to fill empty modes, the restructuring procedure, and
the deferral boundary.
"""
from __future__ import annotations
import json, re
from pathlib import Path

import os, sys

# Directory holding the answers, laid out as <eval>/<config>/outputs/answer.md.
# Pass it as the first argument, or set DIATAXIS_EVAL_RUNS.
WS = Path(sys.argv[1] if len(sys.argv) > 1
          else os.environ.get("DIATAXIS_EVAL_RUNS", "evals/runs"))

def load(ev, cfg):
    p = WS / ev / cfg / "outputs" / "answer.md"
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
   lambda t: not bool(re.search(r"(create|add|write|new)\s+(a\s+)?(`?tutorials?/|tutorial page|tutorial\b)", t))),
  ("does not create an explanation page",
   lambda t: not bool(re.search(r"(create|add|write|new)\s+(a\s+)?(`?explanations?/|explanation page)", t))),
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

rows=[]
for ev, asserts in A.items():
    row={"eval":ev}
    for cfg in ("with_skill","without_skill"):
        t=load(ev,cfg)
        if t is None: row[cfg]=None; continue
        row[cfg]=[(n, bool(f(t))) for n,f in asserts]
    rows.append(row)

print(f"{'eval':<24} {'with skill':>12} {'baseline':>12}")
print("-"*50)
tw=nw=tb=nb=0
for r in rows:
    w,b=r["with_skill"],r["without_skill"]
    ws=f"{sum(p for _,p in w)}/{len(w)}" if w else "—"
    bs=f"{sum(p for _,p in b)}/{len(b)}" if b else "—"
    if w: tw+=sum(p for _,p in w); nw+=len(w)
    if b: tb+=sum(p for _,p in b); nb+=len(b)
    print(f"{r['eval']:<24} {ws:>12} {bs:>12}")
print("-"*50)
print(f"{'TOTAL':<24} {f'{tw}/{nw}':>12} {f'{tb}/{nb}':>12}")
print("\nper-assertion (with / baseline):")
for r in rows:
    print(f"\n  {r['eval']}")
    w,b=r["with_skill"],r["without_skill"]
    for i,(n,_) in enumerate(A[r["eval"]]):
        wm="PASS" if w and w[i][1] else ("FAIL" if w else "—")
        bm="PASS" if b and b[i][1] else ("FAIL" if b else "—")
        mark="  <-- differs" if (w and b and w[i][1]!=b[i][1]) else ""
        print(f"    {wm:<5} {bm:<5} {n}{mark}")
json.dump({r["eval"]:{k:v for k,v in r.items() if k!="eval"} for r in rows},
          open(WS/"grading-discriminating.json","w"), indent=2, default=str)
