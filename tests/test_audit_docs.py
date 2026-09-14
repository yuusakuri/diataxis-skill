#!/usr/bin/env python3
"""Tests for the Diátaxis auditor.

Two properties matter more than any individual rule:

  * a correctly organised tree produces no mode-mixing findings, or the tool
    is noise and will be ignored;
  * a tree with the characteristic failure produces a finding that names the
    right page and the right reason.

Run:  python3 -m unittest discover -s tests -v
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "skills" / "diataxis" / "scripts" / "audit_docs.py"
FIXTURES = ROOT / "tests" / "fixtures"

sys.path.insert(0, str(SCRIPT.parent))
import audit_docs  # noqa: E402


def run_cli(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(SCRIPT), *args],
                          capture_output=True, text=True)


def audit_fixture(name: str):
    return audit_docs.audit(FIXTURES / name)


def findings_of(name: str, kind: str):
    findings, _, _ = audit_fixture(name)
    return [f for f in findings if f.kind == kind]


class TestCleanTree(unittest.TestCase):
    """A well-organised tree must come back quiet."""

    def test_no_mode_mixing(self):
        self.assertEqual(findings_of("clean", "mode-mixing"), [],
                         "a correct tree must not be flagged, or the tool is noise")

    def test_no_unclassified_pages(self):
        self.assertEqual(findings_of("clean", "unclassified"), [])

    def test_all_four_modes_detected(self):
        _, _, summary = audit_fixture("clean")
        self.assertEqual(summary["modes_present"],
                         ["explanation", "how-to", "reference", "tutorial"])

    def test_no_missing_mode_findings(self):
        self.assertEqual(findings_of("clean", "missing-mode"), [])


class TestModeMixing(unittest.TestCase):
    """The characteristic Diátaxis failure must be caught, with reasons."""

    def test_reference_page_with_procedure_is_flagged(self):
        paths = [f.path for f in findings_of("mixed", "mode-mixing")]
        self.assertIn("reference/cli.md", paths)

    def test_reference_finding_names_action_as_the_intruder(self):
        f = next(f for f in findings_of("mixed", "mode-mixing")
                 if f.path == "reference/cli.md")
        self.assertEqual(f.mode, "reference")
        self.assertEqual(f.intruder, "action")
        self.assertIn("how-to guide", f.message,
                      "the finding should say where the content belongs")

    def test_tutorial_stuffed_with_options_is_flagged(self):
        paths = [f.path for f in findings_of("mixed", "mode-mixing")]
        self.assertIn("tutorials/getting-started.md", paths)

    def test_explanation_with_procedure_is_flagged(self):
        paths = [f.path for f in findings_of("mixed", "mode-mixing")]
        self.assertIn("explanation/architecture.md", paths)

    def test_findings_carry_line_number_evidence(self):
        for f in findings_of("mixed", "mode-mixing"):
            self.assertTrue(f.evidence, f"{f.path} has no evidence")
            self.assertTrue(any(e.startswith("line ") for e in f.evidence))


class TestFlatTree(unittest.TestCase):
    """Docs with no mode structure at all."""

    def test_pages_outside_any_mode_are_reported(self):
        paths = {f.path for f in findings_of("flat", "unclassified")}
        self.assertEqual(paths, {"install.md", "api.md"})

    def test_index_files_are_not_treated_as_unclassified(self):
        paths = {f.path for f in findings_of("flat", "unclassified")}
        self.assertNotIn("README.md", paths,
                         "a landing page describes the tree; it is not misfiled")

    def test_all_four_modes_reported_missing(self):
        modes = {f.mode for f in findings_of("flat", "missing-mode")}
        self.assertEqual(modes, {"tutorial", "how-to", "reference", "explanation"})


class TestSignalDetection(unittest.TestCase):
    """The heuristics must fire on what they claim to detect."""

    def _profile(self, body: str):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "page.md"
            p.write_text(body, encoding="utf-8")
            return audit_docs.profile_page(p)

    def test_numbered_imperative_steps_count_as_action(self):
        prof = self._profile("1. Run `x`\n2. Open the file\n3. Click Save\n")
        self.assertGreaterEqual(prof.counts["action"], 3)

    def test_option_table_counts_as_reference(self):
        prof = self._profile(
            "| Option | Type |\n|---|---|\n| `--a` | int |\n| `--b` | int |\n")
        self.assertGreaterEqual(prof.counts["reference"], 3)

    def test_prose_table_is_not_reference(self):
        prof = self._profile(
            "| Name | Favourite colour |\n|---|---|\n| Ada | green |\n")
        self.assertEqual(prof.counts["reference"], 0,
                         "an ordinary table is not a parameter reference")

    def test_reasoning_words_count_as_explanation(self):
        prof = self._profile("We chose this because of a trade-off.\n"
                             "Historically the rationale was different.\n")
        self.assertGreaterEqual(prof.counts["explanation"], 2)

    def test_shell_fence_counts_as_action(self):
        prof = self._profile("```bash\nnpm install\n```\n")
        self.assertEqual(prof.counts["action"], 1)

    def test_prose_inside_a_fence_is_not_double_counted(self):
        prof = self._profile("```text\n1. Run this\n2. Open that\n3. Click it\n```\n")
        self.assertEqual(prof.counts["action"], 0,
                         "lines inside a non-shell fence are sample output, not steps")

    def test_incidental_mention_does_not_trigger_a_finding(self):
        """One aside in an otherwise native page must stay quiet."""
        with tempfile.TemporaryDirectory() as tmp:
            ref = Path(tmp) / "reference"
            ref.mkdir()
            (ref / "api.md").write_text(
                "| Option | Type |\n|---|---|\n"
                + "".join(f"| `--o{i}` | int |\n" for i in range(20))
                + "\n1. Run `x` to regenerate this table\n",
                encoding="utf-8")
            findings, _, _ = audit_docs.audit(Path(tmp))
            self.assertEqual([f for f in findings if f.kind == "mode-mixing"], [])


class TestDirectoryNaming(unittest.TestCase):
    def test_common_synonyms_map_to_modes(self):
        cases = {
            ("tutorials",): "tutorial",
            ("getting-started",): "tutorial",
            ("how-to-guides",): "how-to",
            ("guides",): "how-to",
            ("api",): "reference",
            ("concepts",): "explanation",
            ("background",): "explanation",
        }
        for parts, expected in cases.items():
            self.assertEqual(audit_docs.classify_dir(parts), expected, parts)

    def test_unknown_directory_has_no_mode(self):
        self.assertIsNone(audit_docs.classify_dir(("misc", "notes")))

    def test_mode_is_found_at_any_depth(self):
        self.assertEqual(audit_docs.classify_dir(("docs", "reference", "v2")),
                         "reference")


class TestCLI(unittest.TestCase):
    def test_clean_tree_exits_zero_under_strict(self):
        r = run_cli(str(FIXTURES / "clean"), "--strict")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_mixed_tree_exits_one_under_strict(self):
        r = run_cli(str(FIXTURES / "mixed"), "--strict")
        self.assertEqual(r.returncode, 1)

    def test_json_output_is_valid_and_structured(self):
        r = run_cli(str(FIXTURES / "mixed"), "--json")
        data = json.loads(r.stdout)
        self.assertIn("findings", data)
        self.assertIn("summary", data)
        self.assertTrue(all("severity" in f for f in data["findings"]))

    def test_missing_directory_exits_two(self):
        r = run_cli("/nonexistent/path/xyz")
        self.assertEqual(r.returncode, 2)
        self.assertIn("not a directory", r.stderr)

    def test_human_output_explains_findings_are_not_verdicts(self):
        r = run_cli(str(FIXTURES / "mixed"))
        self.assertIn("not verdicts", r.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
