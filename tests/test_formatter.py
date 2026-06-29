"""Tests for the Behave formatter entry point."""

from __future__ import annotations

import io
from pathlib import Path

from behave_modern_md_report.formatter import BehaveMarkdownFormatter, _FakeFinal


class FakeStreamOpener:
    name = "report.md"
    stream = io.StringIO()


class FakeConfig:
    userdata = {}
    outputs = []


class FakeFormatterContext:
    """Minimal stub for Behave formatter context."""

    def __init__(self) -> None:
        self._runner = type("Runner", (), {"formatters": []})()


def test_formatter_init():
    formatter = BehaveMarkdownFormatter(FakeStreamOpener(), FakeConfig())
    assert formatter._output_path == Path("report.md")


def test_formatter_resolve_output_path():
    formatter = BehaveMarkdownFormatter
    assert formatter._resolve_output_path(FakeStreamOpener(), FakeConfig()) == Path("report.md")


def test_fake_final():
    source = type("Source", (), {"status": "passed", "duration": 1.0})()
    final = _FakeFinal(source)
    assert final.status == "passed"
    assert final.duration == 1.0


def test_formatter_attachment_methods():
    formatter = BehaveMarkdownFormatter(FakeStreamOpener(), FakeConfig())
    formatter._collector.start_feature(type("Feature", (), {"name": "F", "description": [], "location": "", "tags": []})())
    formatter._collector.start_scenario(type("Scenario", (), {"name": "S", "description": [], "location": "", "tags": [], "type": "scenario"})())
    formatter._collector.add_step(type("Step", (), {"keyword": "Given", "name": "x", "status": "passed", "duration": 0.0, "location": "", "text": None, "table": None, "error_message": "", "exception": None, "exc_traceback": "", "embeddings": [], "log": []})())

    formatter.attach_text("hello", name="note.txt")
    formatter.log("log line")
    step = formatter._collector._current_scenario.steps[0]
    assert len(step.attachments) == 1
    assert step.logs == ["log line"]
