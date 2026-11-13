"""Exercise installation and automation boundaries without calling a model."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import tomllib
import unittest


REPO = Path(__file__).resolve().parents[2]


class InstallationTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="codex-install-test-")
        self.addCleanup(self.temporary.cleanup)
        self.codex_home = Path(self.temporary.name) / "personal config"
        self.env = {**os.environ, "CODEX_HOME": str(self.codex_home)}

    def install(self, *arguments):
        return subprocess.run(
            ["bash", str(REPO / "scripts/install.sh"), *arguments],
            env=self.env, text=True, capture_output=True, check=False,
        )

    def test_check_does_not_create_a_missing_destination(self):
        result = self.install("--check")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("story-analysis", result.stdout)
        self.assertIn("backend-investigator.toml", result.stdout)
        self.assertFalse(self.codex_home.exists())

    def test_install_is_repeatable_and_preserves_unmanaged_files(self):
        for _ in range(2):
            result = self.install()
            self.assertEqual(result.returncode, 0, result.stderr)
        for source in (REPO / "agents").glob("*.toml"):
            self.assertEqual(source.read_bytes(), (self.codex_home / "agents" / source.name).read_bytes())
        skill = self.codex_home / "skills/story-analysis/SKILL.md"
        self.assertEqual(skill.read_bytes(), (REPO / ".agents/skills/story-analysis/SKILL.md").read_bytes())
        custom = self.codex_home / "agents/my-agent.toml"
        custom.write_text('name = "my-agent"\n')
        extra = self.codex_home / "skills/story-analysis/personal-notes.md"
        extra.write_text("Personal notes\n")
        self.assertEqual(self.install().returncode, 0)
        self.assertEqual(custom.read_text(), 'name = "my-agent"\n')
        self.assertEqual(extra.read_text(), "Personal notes\n")
        self.assertEqual(self.install("--check").returncode, 0)
        self.assertFalse((self.codex_home / "AGENTS.md").exists())
        self.assertFalse((self.codex_home / "config.toml").exists())

    def test_check_reports_drift_without_repairing_it(self):
        self.assertEqual(self.install().returncode, 0)
        agent = self.codex_home / "agents/backend-investigator.toml"
        skill = self.codex_home / "skills/story-analysis/SKILL.md"
        agent.write_text("local agent\n")
        skill.write_text("local skill\n")
        result = self.install("--check")
        self.assertEqual(result.returncode, 1)
        self.assertIn("backend-investigator.toml", result.stdout)
        self.assertIn("story-analysis", result.stdout)
        self.assertEqual(agent.read_text(), "local agent\n")
        self.assertEqual(skill.read_text(), "local skill\n")

    def test_global_conflict_prevents_partial_installation(self):
        self.codex_home.mkdir()
        global_file = self.codex_home / "AGENTS.md"
        global_file.write_text("Personal instructions\n")
        result = self.install("--with-global-agents")
        self.assertEqual(result.returncode, 1)
        self.assertFalse((self.codex_home / "skills").exists())
        self.assertFalse((self.codex_home / "agents").exists())
        self.assertEqual(global_file.read_text(), "Personal instructions\n")
        self.assertEqual(self.install("--force-global-agents").returncode, 0)
        self.assertEqual(global_file.read_bytes(), (REPO / "global/AGENTS.md").read_bytes())
        self.assertEqual(self.install("--check", "--with-global-agents").returncode, 0)

    def test_invalid_flag_does_not_create_destination(self):
        self.assertEqual(self.install("--unknown").returncode, 2)
        self.assertFalse(self.codex_home.exists())

    def test_custom_agent_configs_parse_and_inherit_runtime_settings(self):
        names = set()
        for source in (REPO / "agents").glob("*.toml"):
            config = tomllib.loads(source.read_text())
            self.assertEqual(set(config), {"name", "description", "developer_instructions"})
            self.assertEqual(config["name"], source.stem)
            self.assertNotIn(config["name"], names)
            names.add(config["name"])
            self.assertTrue(config["description"])
            self.assertTrue(config["developer_instructions"])
        self.assertEqual(names, {"backend-investigator", "frontend-investigator",
                                 "persistence-reviewer", "security-reviewer"})


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="codex-workflow-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.project = self.root / "project with spaces"
        self.project.mkdir()
        self.git("init", "--quiet")
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid",
                 "-c", "commit.gpgsign=false", "-c", "core.hooksPath=/dev/null",
                 "commit", "--allow-empty", "--quiet", "-m", "fixture")
        self.codex_home = self.root / "personal config"
        self.capture = self.root / "captured.json"
        bin_dir = self.root / "bin"
        bin_dir.mkdir()
        fake_codex = bin_dir / "codex"
        fake_codex.write_text(
            f"#!{sys.executable}\n"
            "import json, os, pathlib, sys\n"
            "pathlib.Path(os.environ['WORKFLOW_CAPTURE']).write_text(\n"
            "    json.dumps({'args': sys.argv[1:], 'prompt': sys.stdin.read()}))\n"
            "if '--output-last-message' in sys.argv:\n"
            "    pathlib.Path(sys.argv[sys.argv.index('--output-last-message') + 1]).write_text('Final report\\n')\n"
            "if 'WORKFLOW_COMPETING_REPORT' in os.environ:\n"
            "    pathlib.Path(os.environ['WORKFLOW_COMPETING_REPORT']).write_text('Other run\\n')\n"
            "sys.exit(int(os.environ.get('WORKFLOW_EXIT_CODE', '0')))\n"
        )
        fake_codex.chmod(0o755)
        self.env = {
            **os.environ, "CODEX_HOME": str(self.codex_home),
            "PATH": str(bin_dir) + os.pathsep + os.environ["PATH"],
            "WORKFLOW_CAPTURE": str(self.capture),
        }
        for name in ("story-analysis", "parallel-review", "security-review", "story-workflow"):
            path = self.codex_home / "skills" / name / "SKILL.md"
            path.parent.mkdir(parents=True)
            path.write_text("fixture skill\n")

    def git(self, *arguments):
        return subprocess.run(["git", "-C", str(self.project), *arguments],
                              check=True, capture_output=True, text=True).stdout.strip()

    def run_workflow(self, workflow="story-analysis", *arguments):
        return subprocess.run(
            ["bash", str(REPO / "scripts/run-workflow.sh"), workflow,
             str(self.project), *arguments], env=self.env,
            text=True, capture_output=True, check=False,
        )

    def test_dry_run_does_not_execute_codex_or_write_report(self):
        output = self.root / "report.md"
        result = self.run_workflow("parallel-review", "--base", "HEAD", "--request",
                                   "Review local changes", "--output", str(output), "--dry-run")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(self.git("rev-parse", "HEAD"), result.stdout)
        self.assertIn("$parallel-review", result.stdout)
        self.assertFalse(self.capture.exists())
        self.assertFalse(output.exists())

    def test_request_is_literal_and_sandbox_is_read_only(self):
        sentinel = self.root / "must-not-exist"
        request = f"Analyze #42\n$(touch '{sentinel}') `touch '{sentinel}'` $HOME"
        output = self.root / "report with spaces.md"
        result = self.run_workflow("story-analysis", "--request", request, "--output", str(output))
        self.assertEqual(result.returncode, 0, result.stderr)
        captured = json.loads(self.capture.read_text())
        self.assertEqual(captured["args"][:6], ["exec", "--cd", str(self.project.resolve()),
                         "--sandbox", "read-only", "--output-last-message"])
        self.assertEqual(captured["args"][-1], "-")
        self.assertTrue(captured["args"][6].startswith(str(output.resolve()) + ".tmp."))
        self.assertFalse(Path(captured["args"][6]).exists())
        self.assertEqual(output.read_text(), "Final report\n")
        self.assertIn(request, captured["prompt"])
        self.assertFalse(sentinel.exists())

    def test_review_resolves_base_commit_before_execution(self):
        base = self.git("rev-parse", "HEAD")
        self.git("branch", "review-base")
        result = self.run_workflow("parallel-review", "--base", "review-base", "--request", "Review")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(f"Resolved base commit: {base}", json.loads(self.capture.read_text())["prompt"])

    def test_full_workflow_defaults_to_read_only_planning(self):
        result = self.run_workflow("story-workflow", "--request", "Add a feature")
        self.assertEqual(result.returncode, 0, result.stderr)
        captured = json.loads(self.capture.read_text())
        self.assertEqual(captured["args"][3:5], ["--sandbox", "read-only"])
        self.assertIn("$story-workflow", captured["prompt"])
        self.assertIn(f"Resolved base commit: {self.git('rev-parse', 'HEAD')}", captured["prompt"])

    def test_security_review_is_read_only_and_keeps_literal_scope(self):
        request = "Review private document access and tenant isolation"
        result = self.run_workflow("security-review", "--request", request)
        self.assertEqual(result.returncode, 0, result.stderr)
        captured = json.loads(self.capture.read_text())
        self.assertEqual(captured["args"][3:5], ["--sandbox", "read-only"])
        self.assertIn("$security-review", captured["prompt"])
        self.assertIn(request, captured["prompt"])
        self.assertIn("focused source-only security review", captured["prompt"])

    def test_security_review_resolves_explicit_base(self):
        self.git("branch", "security-base")
        result = self.run_workflow("security-review", "--base", "security-base", "--request", "Review this diff")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Requested base reference: security-base", json.loads(self.capture.read_text())["prompt"])

    def test_full_workflow_implementation_is_opt_in(self):
        result = self.run_workflow("story-workflow", "--request", "Add a feature", "--implement")
        self.assertEqual(result.returncode, 0, result.stderr)
        captured = json.loads(self.capture.read_text())
        self.assertEqual(captured["args"][3:5], ["--sandbox", "workspace-write"])
        self.assertNotIn("--dangerously-bypass-approvals-and-sandbox", captured["args"])

    def test_mixed_requirement_sources_are_passed_literally(self):
        for request in ["#4521", "https://example.invalid/spec?version=2&mode=full",
                        str(self.root / "Requirements document.docx"),
                        "Add a filter.\nKeep the existing pagination."]:
            with self.subTest(request=request):
                result = self.run_workflow("story-workflow", "--request", request, "--implement")
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn(request, json.loads(self.capture.read_text())["prompt"])

    def test_full_workflow_accepts_an_explicit_base(self):
        self.git("branch", "feature-base")
        result = self.run_workflow("story-workflow", "--base", "feature-base", "--request", "Add a feature")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Requested base reference: feature-base", json.loads(self.capture.read_text())["prompt"])

    def test_implementation_dry_run_does_not_execute_codex(self):
        result = self.run_workflow("story-workflow", "--request", "Implement #42", "--implement", "--dry-run")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Requested mode: complete local development", result.stdout)
        self.assertFalse(self.capture.exists())

    def test_invalid_or_missing_base_prevents_execution(self):
        for arguments in [("--request", "Review"),
                          ("--base", "missing-branch", "--request", "Review")]:
            with self.subTest(arguments=arguments):
                self.assertEqual(self.run_workflow("parallel-review", *arguments).returncode, 2)
                self.assertFalse(self.capture.exists())

    def test_missing_skill_prevents_execution(self):
        (self.codex_home / "skills/story-analysis/SKILL.md").unlink()
        result = self.run_workflow("story-analysis", "--request", "Analyze #42")
        self.assertEqual(result.returncode, 2)
        self.assertIn("not installed", result.stderr)
        self.assertFalse(self.capture.exists())

    def test_existing_report_is_preserved(self):
        output = self.root / "report.md"
        output.write_text("existing report\n")
        result = self.run_workflow("story-analysis", "--request", "Analyze #42", "--output", str(output))
        self.assertEqual(result.returncode, 2)
        self.assertEqual(output.read_text(), "existing report\n")
        self.assertFalse(self.capture.exists())

    def test_codex_failure_is_propagated(self):
        self.env["WORKFLOW_EXIT_CODE"] = "7"
        output = self.root / "failed-report.md"
        self.assertEqual(self.run_workflow("story-analysis", "--request", "Analyze #42", "--output", str(output)).returncode, 7)
        self.assertFalse(output.exists())
        self.assertEqual(list(self.root.glob("failed-report.md.tmp.*")), [])

    def test_report_created_during_execution_is_not_overwritten(self):
        output = self.root / "report.md"
        self.env["WORKFLOW_COMPETING_REPORT"] = str(output)
        result = self.run_workflow("story-analysis", "--request", "Analyze #42", "--output", str(output))
        self.assertEqual(result.returncode, 1)
        self.assertEqual(output.read_text(), "Other run\n")
        self.assertEqual(list(self.root.glob("report.md.tmp.*")), [])

    def test_invalid_options_prevent_execution(self):
        for workflow, arguments in [
            ("unsupported", ("--request", "Analyze")),
            ("story-analysis", ("--request",)),
            ("story-analysis", ("--request", "Analyze", "--base", "HEAD")),
            ("story-analysis", ("--request", "Analyze", "--implement")),
            ("parallel-review", ("--base", "HEAD", "--request", "Review", "--implement")),
            ("security-review", ("--request", "Review", "--implement")),
            ("story-workflow", ("--base", "missing-branch", "--request", "Implement")),
        ]:
            with self.subTest(workflow=workflow, arguments=arguments):
                self.assertEqual(self.run_workflow(workflow, *arguments).returncode, 2)
                self.assertFalse(self.capture.exists())


if __name__ == "__main__":
    unittest.main()
