"""Tests for the event collector."""

from __future__ import annotations

from behave_modern_md_report.collector import Collector
from behave_modern_md_report.models import STATUS_FAILED, STATUS_PASSED, Attachment


class FakeFeature:
    name = "Login"
    description = ["As a user", "I want to log in"]
    location = "features/login.feature:1"
    tags = ["@ui"]
    background = None


class FakeScenario:
    name = "Valid credentials"
    description = []
    location = "features/login.feature:3"
    tags = ["@smoke"]
    type = "scenario"
    status = "passed"
    duration = 0.5


class FakeStep:
    keyword = "Given"
    name = "the user is on the login page"
    status = "passed"
    duration = 0.5
    location = "features/steps.py:10"
    text = None
    table = None
    error_message = ""
    exception = None
    exc_traceback = ""
    embeddings = []
    log = []


class FakeFailedStep(FakeStep):
    name = "the user clicks login"
    status = "failed"
    duration = 1.2
    error_message = "Expected 200, got 500"
    exception = AssertionError("Expected 200, got 500")
    exc_traceback = "Traceback line 1\nTraceback line 2"


def test_collector_builds_execution():
    collector = Collector(title="Test Report")
    collector.start_feature(FakeFeature())
    collector.start_scenario(FakeScenario())
    collector.add_step(FakeStep())
    collector.end_scenario(FakeScenario())
    collector.end_feature(FakeFeature())
    execution = collector.finalize()

    assert execution.title == "Test Report"
    assert len(execution.features) == 1
    assert len(execution.features[0].scenarios) == 1
    assert execution.features[0].scenarios[0].status == STATUS_PASSED


def test_collector_captures_error():
    collector = Collector()
    collector.start_feature(FakeFeature())
    collector.start_scenario(FakeScenario())
    failed = FakeFailedStep()
    collector.add_step(failed)
    collector.end_scenario(FakeScenario())
    collector.end_feature(FakeFeature())
    execution = collector.finalize()

    step = execution.features[0].scenarios[0].steps[0]
    assert step.status == STATUS_FAILED
    assert step.error is not None
    assert step.error.exception_type == "AssertionError"
    assert "Expected 200" in step.error.message


def test_collector_attach():
    collector = Collector()
    collector.start_feature(FakeFeature())
    collector.start_scenario(FakeScenario())
    collector.add_step(FakeStep())
    collector.attach(Attachment(name="log.txt", mime_type="text/plain", text="hello"))
    collector.end_scenario(FakeScenario())
    collector.end_feature(FakeFeature())
    execution = collector.finalize()

    step = execution.features[0].scenarios[0].steps[0]
    assert len(step.attachments) == 1
    assert step.attachments[0].name == "log.txt"


def test_collector_log():
    collector = Collector()
    collector.start_feature(FakeFeature())
    collector.start_scenario(FakeScenario())
    collector.add_step(FakeStep())
    collector.log("a log message")
    collector.end_scenario(FakeScenario())
    collector.end_feature(FakeFeature())
    execution = collector.finalize()

    step = execution.features[0].scenarios[0].steps[0]
    assert step.logs == ["a log message"]
