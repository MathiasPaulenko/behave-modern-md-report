"""Behave formatter entry point.

Register in ``behave.ini``::

    [behave.formatters]
    markdown = behave_modern_md_report.formatter:BehaveMarkdownFormatter

Then run::

    behave -f markdown -o report.md
"""

from __future__ import annotations

import base64
import contextlib
import sys
from pathlib import Path
from typing import Any

try:
    from behave.formatter.base import Formatter
except Exception:  # pragma: no cover - Behave optional at import time
    Formatter = object

from .collector import Collector
from .models import Attachment
from .renderer import MarkdownRenderer, RenderOptions
from .utils import guess_mime


class BehaveMarkdownFormatter(Formatter):  # type: ignore[misc]
    """Behave formatter that produces a Markdown report."""

    name = "markdown"
    description = "Markdown report for Behave"

    def __init__(self, stream_opener: Any, config: Any) -> None:
        """Initialize the formatter with user options and a collector/renderer.

        Args:
            stream_opener: Behave stream opener for the report output.
            config: Behave configuration object.

        """
        super().__init__(stream_opener, config)

        userdata = getattr(config, "userdata", {}) or {}
        options = RenderOptions.from_userdata(userdata)
        self._options = options
        self._collector = Collector(title=options.title)
        self._renderer = MarkdownRenderer(options)

        self._output_path = self._resolve_output_path(stream_opener, config)

    # ------------------------------------------------------------------
    # Behave lifecycle
    # ------------------------------------------------------------------

    def feature(self, feature: Any) -> None:  # noqa: D401 - behave signature
        """Behave hook: a feature has started."""
        self._collector.start_feature(feature)

    def background(self, background: Any) -> None:
        """Behave hook: background steps are handled via the scenario."""
        pass

    def rule(self, rule: Any) -> None:
        """Behave hook: a rule has started (Gherkin v6, Behave 1.3.x)."""
        self._collector.start_rule(rule)

    def scenario(self, scenario: Any) -> None:
        """Behave hook: a scenario has started."""
        self._collector.start_scenario(scenario)

    def step(self, step: Any) -> None:
        """Behave hook: step queued; final state arrives in ``result``."""
        pass

    def match(self, match: Any) -> None:
        """Behave hook: step matched to a step implementation."""
        pass

    def result(self, step: Any) -> None:
        """Behave hook: a step result is available."""
        self._collector.add_step(step)

    def eof(self) -> None:
        """Behave hook: end of feature; finalize current feature/scenario."""
        feature = self._collector._current_feature  # noqa: SLF001 - intentional
        if feature is not None:
            self._collector.end_feature(_FakeFinal(feature))

        scenario = self._collector._current_scenario  # noqa: SLF001
        if scenario is not None:
            self._collector.end_scenario(_FakeFinal(scenario))

    def close(self) -> None:
        """Behave hook: finalize the execution and write the Markdown report."""
        execution = self._collector.finalize()
        markdown = self._renderer.render(execution)
        self._output_path.parent.mkdir(parents=True, exist_ok=True)
        self._output_path.write_text(markdown, encoding="utf-8")
        with contextlib.suppress(Exception):  # pragma: no cover
            sys.stdout.write(f"\nBehave Markdown report written to: {self._output_path}\n")

    # ------------------------------------------------------------------
    # Public attachment API for environment.py hooks.
    # ------------------------------------------------------------------

    def attach(self, attachment: Attachment) -> None:
        """Attach a generic attachment object to the current step.

        This is the low-level entry point used by the high-level helpers in
        ``behave_modern_md_report.attach``.

        Args:
            attachment: The attachment to store.

        """
        self._collector.attach(attachment)

    def attach_file(self, path: str | Path, name: str | None = None) -> None:
        """Attach a file to the current step.

        Args:
            path: Path to the file to attach.
            name: Display name. Defaults to the file name.

        """
        p = Path(path)
        data = base64.b64encode(p.read_bytes()).decode("ascii")
        self._collector.attach(
            Attachment(
                name=name or p.name,
                mime_type=guess_mime(p),
                data_base64=data,
            )
        )

    def attach_text(self, text: str, name: str = "log.txt", mime: str = "text/plain") -> None:
        """Attach a text snippet to the current step.

        Args:
            text: Text content to attach.
            name: Display name. Defaults to ``log.txt``.
            mime: MIME type. Defaults to ``text/plain``.

        """
        self._collector.attach(Attachment(name=name, mime_type=mime, text=text))

    def log(self, message: str) -> None:
        """Append a log line to the current step.

        Args:
            message: Log message to store.

        """
        self._collector.log(message)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _resolve_output_path(stream_opener: Any, config: Any) -> Path:
        """Resolve the output Markdown path from Behave's stream opener or config.

        Args:
            stream_opener: Behave stream opener.
            config: Behave configuration object.

        Returns:
            Output path for the Markdown report.

        """
        candidate = getattr(stream_opener, "name", None) or getattr(stream_opener, "filename", None)
        if candidate:
            return Path(candidate)
        outputs = getattr(config, "outputs", None) or []
        for output in outputs:
            name = getattr(output, "name", None)
            if name and name not in ("<stdout>", "<stderr>"):
                return Path(name)
        return Path("behave-modern-md-report.md")


class _FakeFinal:
    """Wrap a Behave object so the collector's ``end_*`` reads its final status."""

    def __init__(self, source: Any) -> None:
        """Wrap a Behave object to expose its final status and duration.

        Args:
            source: Behave object to wrap.

        """
        self.status = getattr(source, "status", None)
        self.duration = getattr(source, "duration", 0.0)
