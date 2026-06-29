"""Collects Behave events and builds an :class:`Execution` tree.

The collector is intentionally decoupled from Behave's internals: it accepts
loosely-typed objects with the well-known attributes Behave exposes, which
keeps this layer easy to unit-test with simple stubs.
"""

from __future__ import annotations

import getpass
import os
import platform
import socket
import subprocess
import sys
import traceback as traceback_module
import types
from datetime import datetime
from typing import Any

from . import statistics as stats_mod
from .models import (
    FAILED_STATUSES,
    STATUS_FAILED,
    STATUS_PASSED,
    STATUS_SKIPPED,
    STATUS_UNTESTED,
    Attachment,
    Background,
    DataTable,
    Environment,
    ErrorInfo,
    Execution,
    Feature,
    Scenario,
    Statistics,
    Step,
    normalize_status,
)
from .utils import safe_str


def _derive_scenario_status(scenario: Scenario) -> str:
    """Derive a scenario's status from its step statuses.

    Behave does not always provide a final scenario status to the formatter.
    When the collector's scenario is still untested, this helper derives the
    effective status from the step results.

    """
    statuses = [step.status for step in scenario.steps]
    if any(s in FAILED_STATUSES for s in statuses):
        return STATUS_FAILED
    if statuses and all(s == STATUS_PASSED for s in statuses):
        return STATUS_PASSED
    if any(s == STATUS_SKIPPED for s in statuses):
        return STATUS_SKIPPED
    return statuses[0] if statuses else STATUS_UNTESTED


class Collector:
    """Builds an :class:`Execution` from formatter events.

    The collector keeps minimal state: the root :class:`Execution`, the
    current feature, the current rule (Gherkin v6 / Behave 1.3.x) and the
    current scenario.
    """

    def __init__(self, title: str = "Behave Markdown Report") -> None:
        """Initialize a collector with an empty execution tree.

        Args:
            title: Execution title. Defaults to "Behave Markdown Report".

        """
        self.execution = Execution(title=title)
        self.execution.environment = self._capture_environment()
        self.execution.statistics = Statistics(start_time=datetime.now())
        self._current_feature: Feature | None = None
        self._current_rule_name: str = ""
        self._current_scenario: Scenario | None = None

    # ------------------------------------------------------------------
    # Environment
    # ------------------------------------------------------------------

    @staticmethod
    def _capture_environment() -> Environment:
        """Capture runtime environment metadata (Python, Behave, host).

        Returns:
            Populated environment record.

        """
        try:
            from behave import __version__ as behave_version
        except Exception:  # pragma: no cover
            behave_version = "unknown"

        try:
            cpu_count = os.cpu_count() or 0
        except Exception:  # pragma: no cover
            cpu_count = 0

        memory_mb = 0
        try:
            import psutil
            memory_mb = int(psutil.virtual_memory().total / (1024 * 1024))
        except Exception:  # pragma: no cover
            pass

        try:
            user = getpass.getuser()
        except Exception:  # pragma: no cover
            user = ""

        git_info = Collector._capture_git_info()

        env_vars: dict[str, str] = {}
        for key in os.environ:
            if (
                any(
                    key.upper().startswith(prefix)
                    for prefix in (
                        "CI",
                        "GITHUB",
                        "GITLAB",
                        "BITBUCKET",
                        "JENKINS",
                        "TRAVIS",
                        "CIRCLE",
                        "BUILD",
                        "AGENT",
                        "TF_",
                        "AZURE",
                    )
                )
                or key.upper()
                in {"PATH", "HOME", "USER", "USERPROFILE", "SHELL", "LANG", "TERM"}
            ):
                env_vars[key] = safe_str(os.environ[key])

        return Environment(
            python_version=sys.version.split()[0],
            behave_version=behave_version,
            platform=f"{platform.system()} {platform.release()} ({platform.machine()})",
            hostname=socket.gethostname(),
            cwd=safe_str(os.getcwd()),
            command=" ".join(sys.argv),
            user=user,
            cpu_count=cpu_count,
            memory_mb=memory_mb,
            git_branch=git_info.get("branch", ""),
            git_commit=git_info.get("commit", ""),
            git_remote=git_info.get("remote", ""),
            env_vars=env_vars,
        )

    @staticmethod
    def _capture_git_info() -> dict[str, str]:
        """Capture git branch, commit and remote if available."""
        info: dict[str, str] = {}
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                capture_output=True,
                text=True,
                timeout=2,
                check=False,
            )
            if result.returncode == 0:
                info["branch"] = result.stdout.strip()
            result = subprocess.run(
                ["git", "rev-parse", "--short", "HEAD"],
                capture_output=True,
                text=True,
                timeout=2,
                check=False,
            )
            if result.returncode == 0:
                info["commit"] = result.stdout.strip()
            result = subprocess.run(
                ["git", "remote", "get-url", "origin"],
                capture_output=True,
                text=True,
                timeout=2,
                check=False,
            )
            if result.returncode == 0:
                info["remote"] = result.stdout.strip()
        except Exception:  # pragma: no cover
            pass
        return info

    # ------------------------------------------------------------------
    # Feature
    # ------------------------------------------------------------------

    def _make_background(self, behave_background: Any) -> Background:
        """Convert a Behave background object into a Background model."""
        bg = Background(
            name=getattr(behave_background, "name", "") or "",
            keyword=(getattr(behave_background, "keyword", "Background") or "Background"),
            location=safe_str(getattr(behave_background, "location", "")),
        )
        for behave_step in getattr(behave_background, "steps", []) or []:
            bg.steps.append(self._make_step(behave_step))
        return bg

    def _make_step(self, behave_step: Any) -> Step:
        """Convert a Behave step object into a Step model."""
        step = Step(
            keyword=(getattr(behave_step, "keyword", "") or "").strip(),
            name=getattr(behave_step, "name", "") or "",
            status=normalize_status(getattr(behave_step, "status", None)),
            duration=float(getattr(behave_step, "duration", 0.0) or 0.0),
            location=safe_str(getattr(behave_step, "location", "")),
            text=getattr(behave_step, "text", None),
        )

        table = getattr(behave_step, "table", None)
        if table is not None:
            try:
                step.table = DataTable(
                    headings=[safe_str(h) for h in getattr(table, "headings", []) or []],
                    rows=[[safe_str(c) for c in row.cells] for row in table.rows],
                )
            except Exception:  # pragma: no cover - defensive
                step.table = None

        error_message = getattr(behave_step, "error_message", None) or ""
        exception = getattr(behave_step, "exception", None)
        if error_message or exception:
            exc_traceback = getattr(behave_step, "exc_traceback", None)
            if isinstance(exc_traceback, types.TracebackType):
                traceback_text = "".join(traceback_module.format_tb(exc_traceback))
            else:
                traceback_text = safe_str(exc_traceback or error_message)
            step.error = ErrorInfo(
                message=safe_str(error_message or exception),
                traceback=traceback_text,
                exception_type=type(exception).__name__ if exception else "",
            )

        for behave_att in getattr(behave_step, "embeddings", []) or []:
            step.attachments.append(self._make_attachment(behave_att))

        step.logs = [safe_str(line) for line in getattr(behave_step, "log", []) or []]
        return step

    def _make_attachment(self, behave_att: Any) -> Attachment:
        """Convert a Behave embedding into an Attachment model."""
        mime = getattr(behave_att, "mime_type", "") or "application/octet-stream"
        data = getattr(behave_att, "data", "") or ""
        name = getattr(behave_att, "name", "") or "attachment"
        if isinstance(data, bytes):
            import base64

            return Attachment(name=name, mime_type=mime, data_base64=base64.b64encode(data).decode("ascii"))
        return Attachment(name=name, mime_type=mime, text=safe_str(data))

    def start_feature(self, behave_feature: Any) -> Feature:
        """Start a new feature and add it to the execution tree.

        Args:
            behave_feature: Behave feature object.

        Returns:
            Created feature model.

        """
        if self._current_scenario is not None:
            self.end_scenario(self._current_scenario)
        if self._current_feature is not None:
            self.end_feature(self._current_feature)
        feature = Feature(
            name=getattr(behave_feature, "name", "") or "",
            description="\n".join(getattr(behave_feature, "description", []) or []),
            location=safe_str(getattr(behave_feature, "location", "")),
            tags=[safe_str(t) for t in getattr(behave_feature, "tags", []) or []],
        )
        behave_background = getattr(behave_feature, "background", None)
        if behave_background:
            feature.background = self._make_background(behave_background)
        self._current_feature = feature
        self.execution.features.append(feature)
        return feature

    def end_feature(self, behave_feature: Any) -> None:
        """Finalize the current feature with its final status and duration.

        Args:
            behave_feature: Behave feature object with final state.

        """
        if self._current_feature is None:
            return
        self._current_feature.status = normalize_status(getattr(behave_feature, "status", None))
        self._current_feature.duration = float(getattr(behave_feature, "duration", 0.0) or 0.0)
        self._current_feature = None
        self._current_rule_name = ""

    # ------------------------------------------------------------------
    # Rule
    # ------------------------------------------------------------------

    def start_rule(self, behave_rule: Any) -> None:
        """Start a new rule under the current feature.

        Args:
            behave_rule: Behave rule object.

        """
        self._current_rule_name = getattr(behave_rule, "name", "") or ""

    def end_rule(self) -> None:
        """Finalize the current rule."""
        self._current_rule_name = ""

    # ------------------------------------------------------------------
    # Scenario
    # ------------------------------------------------------------------

    def start_scenario(self, behave_scenario: Any) -> Scenario:
        """Start a new scenario under the current feature.

        Args:
            behave_scenario: Behave scenario object.

        Returns:
            Created scenario model.

        """
        if self._current_scenario is not None:
            self.end_scenario(self._current_scenario)
        scenario_type = safe_str(getattr(behave_scenario, "type", ""))
        is_outline = scenario_type in ("scenario_outline", "outline")
        outline_name = ""
        examples = None
        if is_outline:
            outline_name = getattr(behave_scenario, "outline_name", "") or getattr(behave_scenario, "name", "") or ""
            examples = self._make_examples(getattr(behave_scenario, "examples", None))

        scenario = Scenario(
            name=getattr(behave_scenario, "name", "") or "",
            description="\n".join(getattr(behave_scenario, "description", []) or []),
            location=safe_str(getattr(behave_scenario, "location", "")),
            tags=[safe_str(t) for t in getattr(behave_scenario, "tags", []) or []],
            feature_name=self._current_feature.name if self._current_feature else "",
            rule_name=self._current_rule_name,
            is_outline=is_outline,
            outline_name=outline_name,
            examples=examples,
        )
        if self._current_feature and self._current_feature.background:
            scenario.background = self._current_feature.background
        self._current_scenario = scenario
        if self._current_feature is not None:
            self._current_feature.scenarios.append(scenario)
        return scenario

    def _make_examples(self, behave_examples: Any) -> DataTable | None:
        """Convert Behave examples tables into a DataTable model."""
        if not behave_examples:
            return None
        tables = getattr(behave_examples, "tables", None)
        if not tables:
            return None
        table = tables[0] if isinstance(tables, list) else behave_examples
        try:
            headings = [safe_str(h) for h in getattr(table, "headings", []) or []]
            rows = [[safe_str(c) for c in row.cells] for row in table.rows]
            return DataTable(headings=headings, rows=rows)
        except Exception:
            return None

    def end_scenario(self, behave_scenario: Any) -> None:
        """Finalize the current scenario with its final status and duration.

        Args:
            behave_scenario: Behave scenario object with final state.

        """
        if self._current_scenario is None:
            return
        status = normalize_status(getattr(behave_scenario, "status", None))
        if status == STATUS_UNTESTED:
            status = _derive_scenario_status(self._current_scenario)
        self._current_scenario.status = status
        self._current_scenario.duration = float(getattr(behave_scenario, "duration", 0.0) or 0.0)
        self._current_scenario = None

    # ------------------------------------------------------------------
    # Steps
    # ------------------------------------------------------------------

    def add_step(self, behave_step: Any) -> Step | None:
        """Add a step result to the current scenario.

        Args:
            behave_step: Behave step object with final state.

        Returns:
            Created step model, or None if no scenario is active.

        """
        if self._current_scenario is None:
            return None
        step = self._make_step(behave_step)
        self._current_scenario.steps.append(step)
        return step

    # ------------------------------------------------------------------
    # Attachments / logs (extension API for environment.py hooks)
    # ------------------------------------------------------------------

    def attach(self, attachment: Attachment) -> None:
        """Attach a file to the current step (last step) or scenario.

        Args:
            attachment: Attachment to store.

        """
        if self._current_scenario is None:
            return
        if self._current_scenario.steps:
            self._current_scenario.steps[-1].attachments.append(attachment)
        else:  # pragma: no cover - rare
            self._current_scenario.steps.append(
                Step(keyword="", name="(attachment)", attachments=[attachment])
            )

    def log(self, message: str) -> None:
        """Append a log line to the current step.

        Args:
            message: Log message to store.

        """
        if self._current_scenario and self._current_scenario.steps:
            self._current_scenario.steps[-1].logs.append(message)

    # ------------------------------------------------------------------
    # Finalize
    # ------------------------------------------------------------------

    def finalize(self) -> Execution:
        """Finalize the execution tree and compute statistics.

        Returns:
            Fully populated execution model.

        """
        self.execution.statistics.end_time = datetime.now()
        stats_mod.compute(self.execution)
        return self.execution
