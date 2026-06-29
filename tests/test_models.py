"""Tests for the execution models."""

from __future__ import annotations

from behave_modern_md_report.models import (
    Attachment,
    DataTable,
    Execution,
    Feature,
    Scenario,
    Statistics,
    normalize_status,
)


def test_normalize_status():
    assert normalize_status("passed") == "passed"
    assert normalize_status("FAILED") == "failed"
    class Enum:
        name = "skipped"
    assert normalize_status(Enum()) == "skipped"
    assert normalize_status(None) == "untested"
    assert normalize_status("unknown") == "untested"


def test_attachment_is_image():
    assert Attachment("x", mime_type="image/png").is_image
    assert not Attachment("x", mime_type="text/plain").is_image


def test_scenario_unique_id():
    scenario = Scenario(name="Login with valid user", feature_name="Authentication")
    assert scenario.unique_id == "authentication-login-with-valid-user"


def test_execution_overall_status():
    execution = Execution(
        features=[
            Feature(name="A", status="passed"),
            Feature(name="B", status="failed"),
        ]
    )
    assert execution.overall_status == "failed"


def test_statistics_pass_rate():
    stats = Statistics(total_scenarios=10, by_status={"passed": 8, "failed": 2})
    assert stats.pass_rate == 80.0
    assert stats.passed == 8
    assert stats.failed == 2


def test_datatable():
    table = DataTable(headings=["name", "age"], rows=[["Ada", "30"], ["Bob", "25"]])
    assert table.headings == ["name", "age"]
    assert len(table.rows) == 2
