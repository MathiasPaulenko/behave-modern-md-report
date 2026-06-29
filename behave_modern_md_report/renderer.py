"""Renders an :class:`Execution` into a Markdown report.

The renderer is intentionally decoupled from Behave so it can also be used by
tooling that reads pre-existing JSON reports or builds execution models by hand.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from . import statistics as stats_mod
from .markdown import MarkdownBuilder
from .models import (
    FAILED_STATUSES,
    STATUS_FAILED,
    STATUS_PASSED,
    STATUS_PENDING,
    STATUS_SKIPPED,
    STATUS_UNDEFINED,
    Attachment,
    DataTable,
    Execution,
    Scenario,
    Step,
    as_dict,
)
from .utils import format_duration, safe_str


@dataclass
class RenderOptions:
    """User-facing rendering options."""

    title: str = ""
    project_name: str = ""
    company: str = ""
    include_passed_scenarios: bool = True
    include_skipped_scenarios: bool = True
    include_traceback: bool = True
    include_environment: bool = True
    sort_failed_first: bool = True
    max_traceback_lines: int = 0
    max_summary_features: int = 0
    extra: dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_userdata(cls, userdata: dict[str, Any]) -> RenderOptions:
        """Build options from Behave ``userdata`` dictionary.

        Recognized keys:
            ``bmr.title``, ``bmr.project_name``, ``bmr.company``,
            ``bmr.include_passed``, ``bmr.include_skipped``,
            ``bmr.include_traceback``, ``bmr.include_environment``,
            ``bmr.sort_failed_first``, ``bmr.max_traceback_lines``,
            ``bmr.max_summary_features``.

        """

        def _parse_bool(value: Any) -> bool:
            return str(value).lower() not in {"false", "0", "no", "", "none"}

        return cls(
            title=userdata.get("bmr.title", "Behave Markdown Report"),
            project_name=userdata.get("bmr.project_name", ""),
            company=userdata.get("bmr.company", ""),
            include_passed_scenarios=_parse_bool(userdata.get("bmr.include_passed", "true")),
            include_skipped_scenarios=_parse_bool(userdata.get("bmr.include_skipped", "true")),
            include_traceback=_parse_bool(userdata.get("bmr.include_traceback", "true")),
            include_environment=_parse_bool(userdata.get("bmr.include_environment", "true")),
            sort_failed_first=_parse_bool(userdata.get("bmr.sort_failed_first", "true")),
            max_traceback_lines=int(userdata.get("bmr.max_traceback_lines", 0) or 0),
            max_summary_features=int(userdata.get("bmr.max_summary_features", 0) or 0),
            extra={k: v for k, v in userdata.items() if k.startswith("bmr.extra.")},
        )


_STATUS_ICONS = {
    STATUS_PASSED: "✅",
    STATUS_FAILED: "❌",
    STATUS_SKIPPED: "⏭",
    STATUS_UNDEFINED: "⚠️",
    STATUS_PENDING: "🚧",
    "untested": "⚪",
    "error": "❌",
    "hook_error": "❌",
    "cleanup_error": "❌",
    "xfailed": "❌",
    "xpassed": "✅",
    "pending_warn": "🚧",
}

_STATUS_LABELS = {
    STATUS_PASSED: "Passed",
    STATUS_FAILED: "Failed",
    STATUS_SKIPPED: "Skipped",
    STATUS_UNDEFINED: "Undefined",
    STATUS_PENDING: "Pending",
    "untested": "Untested",
    "error": "Error",
    "hook_error": "Hook Error",
    "cleanup_error": "Cleanup Error",
    "xfailed": "Expected Failure",
    "xpassed": "Unexpected Pass",
    "pending_warn": "Pending",
}


class MarkdownRenderer:
    """Renders an :class:`Execution` into a single Markdown document."""

    def __init__(self, options: RenderOptions | None = None) -> None:
        """Initialize the renderer with options.

        Args:
            options: Rendering options. Defaults to a fresh RenderOptions
                instance.

        """
        self.options = options or RenderOptions()

    def render(self, execution: Execution) -> str:
        """Render an execution into a single Markdown report.

        Args:
            execution: Execution tree to render.

        Returns:
            Markdown document as a string.

        """
        stats_mod.compute(execution)
        md = MarkdownBuilder()

        self._render_header(md, execution)
        self._render_toc(md, execution)
        self._render_executive_summary(md, execution)
        self._render_statistics(md, execution)
        self._render_feature_summary(md, execution)
        self._render_tags(md, execution)
        self._render_failed_scenarios(md, execution)
        self._render_slowest_scenarios(md, execution)
        self._render_scenario_details(md, execution)
        if self.options.include_environment:
            self._render_environment(md, execution)
        self._render_footer(md, execution)

        return md.join()

    def render_to_file(self, execution: Execution, path: str | Path) -> Path:
        """Render the report and write it to the given path.

        Args:
            execution: Execution tree to render.
            path: Output path for the Markdown report.

        Returns:
            Path to the written Markdown report.

        """
        text = self.render(execution)
        out = Path(path)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        return out

    def render_json(self, execution: Execution) -> str:
        """Return a JSON representation of the execution and derived stats.

        Args:
            execution: Execution tree to serialize.

        Returns:
            Pretty-printed JSON document.

        """
        import json

        stats_mod.compute(execution)
        data = as_dict(execution)
        return json.dumps(
            {
                "execution": data,
                "slowest": [as_dict(s) for s in stats_mod.slowest_scenarios(execution, limit=10)],
                "buckets": stats_mod.duration_buckets(execution),
                "tags": stats_mod.tag_ranking(execution),
            },
            default=str,
            indent=2,
        )

    # ------------------------------------------------------------------
    # Sections
    # ------------------------------------------------------------------

    def _render_header(self, md: MarkdownBuilder, execution: Execution) -> None:
        title = self.options.title or execution.title
        if self.options.project_name:
            title = f"{self.options.project_name} - {title}"
        md.heading(1, f"{_status_icon(execution.overall_status)} {title}")
        md.blank()
        if self.options.company:
            md.paragraph(f"**Company:** {self.options.company}")
        generated = execution.generated_at.strftime("%Y-%m-%d %H:%M:%S")
        duration = format_duration(execution.statistics.duration)
        md.paragraph(
            f"**Status:** {_status_label(execution.overall_status)}  \n"
            f"**Generated:** {generated}  \n"
            f"**Duration:** {duration}"
        )
        md.horizontal_rule()

    def _render_toc(self, md: MarkdownBuilder, execution: Execution) -> None:
        md.heading(2, "Table of Contents")
        items = [
            md.link("Executive Summary", "executive-summary"),
            md.link("Statistics", "statistics"),
            md.link("Feature Summary", "feature-summary"),
            md.link("Tags", "tags"),
        ]
        if execution.statistics.failed:
            items.append(md.link("Failed Scenarios", "failed-scenarios"))
        items.append(md.link("Slowest Scenarios", "slowest-scenarios"))
        items.append(md.link("Scenario Details", "scenario-details"))
        if self.options.include_environment:
            items.append(md.link("Environment", "environment"))
        md.bullet(items)
        md.horizontal_rule()

    def _render_executive_summary(self, md: MarkdownBuilder, execution: Execution) -> None:
        md.heading(2, "Executive Summary")
        md.blank()
        stats = execution.statistics
        headers = ["Status", "Count", "Icon"]
        rows = []
        for status in (STATUS_PASSED, STATUS_FAILED, STATUS_SKIPPED, STATUS_UNDEFINED, STATUS_PENDING):
            count = stats.by_status.get(status, 0)
            if count:
                rows.append([_status_label(status), str(count), _status_icon(status)])
        if not rows:
            rows.append(["No scenarios executed", "0", "-"])
        md.table(headers, rows)
        md.blank()

    def _render_statistics(self, md: MarkdownBuilder, execution: Execution) -> None:
        md.heading(2, "Statistics")
        md.blank()
        stats = execution.statistics
        headers = ["Metric", "Value"]
        rows = [
            ["Features", str(stats.total_features)],
            ["Scenarios", str(stats.total_scenarios)],
            ["Steps", str(stats.total_steps)],
            ["Pass rate", f"{stats.pass_rate:.2f}%"],
            ["Total duration", format_duration(stats.duration)],
            ["Attachments", str(stats.total_attachments)],
            ["Log lines", str(stats.total_logs)],
        ]
        if stats.common_exception_type:
            rows.append(["Common exception", stats.common_exception_type])
        md.table(headers, rows)
        md.blank()

    def _render_feature_summary(self, md: MarkdownBuilder, execution: Execution) -> None:
        md.heading(2, "Feature Summary")
        md.blank()
        features = execution.features
        if self.options.sort_failed_first:
            features = sorted(features, key=lambda f: (0 if f.status == STATUS_FAILED else 1, f.name))
        if self.options.max_summary_features and len(features) > self.options.max_summary_features:
            features = features[: self.options.max_summary_features]
            note = f"Showing first {self.options.max_summary_features} features."
        else:
            note = ""
        headers = ["Feature", "Status", "Scenarios", "Duration"]
        rows = []
        for feature in features:
            link = md.link(feature.name, f"feature-{feature.unique_id}")
            rows.append([
                link,
                f"{_status_icon(feature.status)} {_status_label(feature.status)}",
                str(len(feature.scenarios)),
                format_duration(feature.duration),
            ])
        md.table(headers, rows)
        if note:
            md.paragraph(f"*{note}*")
        md.blank()

    def _render_tags(self, md: MarkdownBuilder, execution: Execution) -> None:
        if not execution.statistics.by_tag:
            return
        md.heading(2, "Tags")
        md.blank()
        tags = stats_mod.tag_ranking(execution)
        headers = ["Tag", "Count", "Passed", "Failed", "Duration", "Pass rate"]
        rows = []
        for tag in tags:
            rows.append([
                md.code_inline(tag["name"]),
                str(tag["count"]),
                str(tag["passed"]),
                str(tag["failed"]),
                format_duration(tag["duration"]),
                f"{tag['pass_rate']:.2f}%",
            ])
        md.table(headers, rows)
        md.blank()

    def _render_failed_scenarios(self, md: MarkdownBuilder, execution: Execution) -> None:
        failed = [s for f in execution.features for s in f.scenarios if s.status in FAILED_STATUSES]
        if not failed:
            return
        md.heading(2, "Failed Scenarios")
        md.blank()
        headers = ["Scenario", "Feature", "Status", "Reason", "Location"]
        rows = []
        for scenario in failed:
            error = self._first_error(scenario)
            reason = error.exception_type or error.message.splitlines()[0] if error else ""
            rows.append([
                md.link(scenario.name, f"scenario-{scenario.unique_id}"),
                scenario.feature_name,
                _status_icon(scenario.status),
                reason,
                scenario.location,
            ])
        md.table(headers, rows)
        md.blank()
        for scenario in failed:
            self._render_failed_scenario_details(md, scenario)
        md.blank()

    def _render_failed_scenario_details(self, md: MarkdownBuilder, scenario: Scenario) -> None:
        md.details(
            summary=f"{_status_icon(scenario.status)} {scenario.name} ({scenario.feature_name})",
            content_lines=self._failed_scenario_content(scenario),
        )

    def _failed_scenario_content(self, scenario: Scenario) -> list[str]:
        content = MarkdownBuilder()
        content.paragraph(f"**Location:** `{scenario.location}`")
        if scenario.tags:
            content.paragraph("**Tags:** " + " ".join(f"`{t}`" for t in scenario.tags))
        error = self._first_error(scenario)
        if error:
            content.heading(4, "Error")
            content.code_block(error.message, "text")
            if self.options.include_traceback and error.traceback:
                tb = self._truncate_traceback(error.traceback)
                content.heading(4, "Traceback")
                content.code_block(tb, "python")
        return content.lines

    def _render_slowest_scenarios(self, md: MarkdownBuilder, execution: Execution) -> None:
        md.heading(2, "Slowest Scenarios")
        md.blank()
        slowest = stats_mod.slowest_scenarios(execution, limit=10)
        if not slowest:
            md.paragraph("No scenario duration data available.")
            return
        headers = ["Rank", "Scenario", "Feature", "Duration"]
        rows = []
        for i, scenario in enumerate(slowest, 1):
            rows.append([
                str(i),
                md.link(scenario.name, f"scenario-{scenario.unique_id}"),
                scenario.feature_name,
                format_duration(scenario.duration),
            ])
        md.table(headers, rows)
        md.blank()

    def _render_scenario_details(self, md: MarkdownBuilder, execution: Execution) -> None:
        md.heading(2, "Scenario Details")
        md.blank()
        for feature in execution.features:
            summary = f"Feature: {feature.name}"
            content = MarkdownBuilder()
            if feature.description:
                content.blockquote(feature.description)
            if feature.tags:
                content.paragraph("Tags: " + " ".join(f"`{t}`" for t in feature.tags))
            content.heading(4, md.link(feature.name, f"feature-{feature.unique_id}"))
            for scenario in feature.scenarios:
                if not self._should_show_scenario(scenario):
                    continue
                self._render_scenario(content, scenario)
            md.details(summary=summary, content_lines=content.lines, open_=False)
        md.horizontal_rule()

    def _render_scenario(self, md: MarkdownBuilder, scenario: Scenario) -> None:
        summary = f"{_status_icon(scenario.status)} Scenario: {scenario.name}"
        content = MarkdownBuilder()
        content.paragraph(f"**Status:** {_status_icon(scenario.status)} {_status_label(scenario.status)}")
        content.paragraph(f"**Duration:** {format_duration(scenario.duration)}")
        if scenario.location:
            content.paragraph(f"**Location:** `{scenario.location}`")
        if scenario.tags:
            content.paragraph("**Tags:** " + " ".join(f"`{t}`" for t in scenario.tags))
        if scenario.description:
            content.blockquote(scenario.description)
        if scenario.background and scenario.background.steps:
            content.heading(5, "Background")
            for step in scenario.background.steps:
                self._render_step(content, step)
        if scenario.examples:
            content.heading(5, "Examples")
            self._render_data_table(content, scenario.examples)
        content.heading(5, "Steps")
        for step in scenario.steps:
            self._render_step(content, step)
        md.details(summary=summary, content_lines=content.lines, open_=scenario.status == STATUS_FAILED)

    def _render_step(self, md: MarkdownBuilder, step: Step) -> None:
        icon = _status_icon(step.status)
        label = _status_label(step.status)
        md.paragraph(f"{icon} **{step.keyword}** {step.name} — `{format_duration(step.duration)}` ({label})")
        if step.location:
            md.text(f"<sub>Location: `{step.location}`</sub>")
        if step.text:
            md.code_block(step.text, "gherkin")
        if step.table:
            self._render_data_table(md, step.table)
        if step.error:
            md.blockquote(f"**{step.error.exception_type}**  \n{step.error.message}")
            if self.options.include_traceback and step.error.traceback:
                tb = self._truncate_traceback(step.error.traceback)
                md.code_block(tb, "python")
        if step.logs:
            md.heading(6, "Logs")
            md.code_block("\n".join(step.logs), "text")
        for attachment in step.attachments:
            self._render_attachment(md, attachment)

    def _render_data_table(self, md: MarkdownBuilder, table: DataTable) -> None:
        if not table.headings:
            return
        rows = [[safe_str(cell) for cell in row] for row in table.rows]
        md.table([safe_str(h) for h in table.headings], rows)
        md.blank()

    def _render_attachment(self, md: MarkdownBuilder, attachment: Attachment) -> None:
        if attachment.is_image and attachment.data_base64:
            src = f"data:{attachment.mime_type};base64,{attachment.data_base64}"
            md.paragraph(f"**Attachment:** {attachment.name}")
            md.paragraph(md.image(attachment.name, src))
        elif attachment.is_text or attachment.text:
            language = "text"
            if attachment.mime_type == "application/json":
                language = "json"
            elif attachment.mime_type in ("application/xml", "application/xhtml+xml"):
                language = "xml"
            elif attachment.mime_type == "text/html":
                language = "html"
            md.paragraph(f"**Attachment:** `{attachment.name}` ({attachment.mime_type})")
            md.code_block(attachment.text or "", language)
        elif attachment.data_base64:
            md.paragraph(f"**Attachment:** `{attachment.name}` ({attachment.mime_type}) — base64 encoded")
        else:
            md.paragraph(f"**Attachment:** `{attachment.name}` ({attachment.mime_type})")

    def _render_environment(self, md: MarkdownBuilder, execution: Execution) -> None:
        md.heading(2, "Environment")
        md.blank()
        env = execution.environment
        headers = ["Variable", "Value"]
        rows = [
            ["Python version", env.python_version],
            ["Behave version", env.behave_version],
            ["Operating system", env.platform],
            ["Hostname", env.hostname],
            ["Working directory", f"`{env.cwd}`"],
            ["Execution command", f"`{env.command}`"],
            ["User", env.user or "unknown"],
            ["CPU count", str(env.cpu_count)],
            ["Memory (MB)", str(env.memory_mb) if env.memory_mb else "unknown"],
        ]
        if env.git_branch:
            rows.append(["Git branch", env.git_branch])
        if env.git_commit:
            rows.append(["Git commit", env.git_commit])
        if env.git_remote:
            rows.append(["Git remote", env.git_remote])
        md.table(headers, rows)
        if env.env_vars:
            md.blank()
            md.heading(3, "CI / Environment Variables")
            var_headers = ["Variable", "Value"]
            var_rows = [[k, safe_str(v)] for k, v in sorted(env.env_vars.items())]
            md.table(var_headers, var_rows)
        md.blank()

    def _render_footer(self, md: MarkdownBuilder, execution: Execution) -> None:
        md.horizontal_rule()
        generated = execution.generated_at.strftime("%Y-%m-%d %H:%M:%S")
        md.paragraph(
            f"*Report generated by {execution.title} on {generated}.*"
        )

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _should_show_scenario(self, scenario: Scenario) -> bool:
        return not (
            (scenario.status == STATUS_PASSED and not self.options.include_passed_scenarios)
            or (scenario.status == STATUS_SKIPPED and not self.options.include_skipped_scenarios)
        )

    def _first_error(self, scenario: Scenario) -> Any:
        for step in scenario.steps:
            if step.error:
                return step.error
        return None

    def _truncate_traceback(self, traceback: str) -> str:
        lines = traceback.splitlines()
        if self.options.max_traceback_lines and len(lines) > self.options.max_traceback_lines:
            lines = lines[: self.options.max_traceback_lines]
            lines.append(f"... ({len(traceback.splitlines()) - self.options.max_traceback_lines} more lines)")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Status helpers
# ---------------------------------------------------------------------------


def _status_icon(status: str) -> str:
    return _STATUS_ICONS.get(status, "⚪")


def _status_label(status: str) -> str:
    return _STATUS_LABELS.get(status, status.title())
