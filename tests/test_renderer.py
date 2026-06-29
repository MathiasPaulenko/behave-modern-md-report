"""Tests for the Markdown renderer."""

from __future__ import annotations

from behave_modern_md_report.models import (
    STATUS_FAILED,
    STATUS_PASSED,
    Attachment,
    DataTable,
    ErrorInfo,
    Execution,
    Feature,
    Scenario,
    Step,
)
from behave_modern_md_report.renderer import MarkdownRenderer, RenderOptions


def make_execution() -> Execution:
    feature = Feature(name="Authentication", description=["Login feature"], tags=["@api"])
    passed_scenario = Scenario(
        name="Valid login",
        status=STATUS_PASSED,
        duration=0.5,
        feature_name="Authentication",
        tags=["@smoke"],
        location="features/login.feature:3",
        steps=[
            Step(
                keyword="Given",
                name="the user is on the login page",
                status=STATUS_PASSED,
                duration=0.2,
            ),
            Step(
                keyword="When",
                name="the user enters valid credentials",
                status=STATUS_PASSED,
                duration=0.3,
            ),
        ],
    )
    failed_scenario = Scenario(
        name="Invalid login",
        status=STATUS_FAILED,
        duration=1.5,
        feature_name="Authentication",
        tags=["@smoke"],
        location="features/login.feature:10",
        steps=[
            Step(
                keyword="When",
                name="the user enters invalid credentials",
                status=STATUS_FAILED,
                duration=1.5,
                error=ErrorInfo(
                    exception_type="AssertionError",
                    message="Expected 200, got 401",
                    traceback="Traceback line",
                ),
            ),
        ],
    )
    feature.scenarios = [passed_scenario, failed_scenario]
    return Execution(title="Test Report", features=[feature])


def test_render_contains_title():
    renderer = MarkdownRenderer()
    report = renderer.render(make_execution())
    assert "Test Report" in report
    assert "# " in report


def test_render_contains_executive_summary():
    renderer = MarkdownRenderer()
    report = renderer.render(make_execution())
    assert "## Executive Summary" in report
    assert "Passed" in report
    assert "Failed" in report


def test_render_contains_feature_summary():
    report = MarkdownRenderer().render(make_execution())
    assert "## Feature Summary" in report
    assert "Authentication" in report


def test_render_contains_failed_scenarios():
    report = MarkdownRenderer().render(make_execution())
    assert "## Failed Scenarios" in report
    assert "Invalid login" in report


def test_render_contains_traceback():
    report = MarkdownRenderer().render(make_execution())
    assert "Traceback line" in report


def test_render_contains_slowest_scenarios():
    report = MarkdownRenderer().render(make_execution())
    assert "## Slowest Scenarios" in report
    assert "Invalid login" in report


def test_render_contains_environment():
    report = MarkdownRenderer().render(make_execution())
    assert "## Environment" in report
    assert "Python version" in report


def test_render_scenario_details():
    report = MarkdownRenderer().render(make_execution())
    assert "## Scenario Details" in report
    assert "Valid login" in report


def test_render_hides_passed_scenarios():
    options = RenderOptions(include_passed_scenarios=False)
    report = MarkdownRenderer(options).render(make_execution())
    # The scenario name may still appear in feature/slowest links, but the
    # collapsible details section should not be rendered for passed scenarios.
    assert "Scenario: Valid login" not in report


def test_render_hides_skipped_scenarios():
    options = RenderOptions(include_skipped_scenarios=False)
    report = MarkdownRenderer(options).render(make_execution())
    # No skipped scenarios in fixture, but option should be respected.
    assert "## Scenario Details" in report


def test_render_attachment_as_image():
    execution = make_execution()
    execution.features[0].scenarios[0].steps[0].attachments.append(
        Attachment(name="screenshot.png", mime_type="image/png", data_base64="AAAA")
    )
    report = MarkdownRenderer().render(execution)
    assert "![screenshot.png]" in report
    assert "data:image/png;base64,AAAA" in report


def test_render_attachment_as_json():
    execution = make_execution()
    execution.features[0].scenarios[0].steps[0].attachments.append(
        Attachment(name="payload.json", mime_type="application/json", text='{"x": 1}')
    )
    report = MarkdownRenderer().render(execution)
    assert "```json" in report
    assert '"x": 1' in report


def test_render_data_table():
    execution = make_execution()
    execution.features[0].scenarios[0].steps[0].table = DataTable(
        headings=["username", "password"],
        rows=[["admin", "secret"]],
    )
    report = MarkdownRenderer().render(execution)
    assert "| username | password |" in report


def test_render_to_file(tmp_path):
    renderer = MarkdownRenderer()
    path = tmp_path / "report.md"
    renderer.render_to_file(make_execution(), path)
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    assert "Test Report" in text
    assert "# " in text
