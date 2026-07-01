"""Tests for the step scanner and step catalog formatter."""

from __future__ import annotations

from pathlib import Path

from behave_modern_md_report.step_catalog_formatter import render_step_catalog
from behave_modern_md_report.step_scanner import (
    StepCatalog,
    StepDefinition,
    scan_directory,
    scan_file,
)

# --------------------------------------------------------------------------- #
# Fixtures
# --------------------------------------------------------------------------- #

SAMPLE_STEPS = '''\
from behave import given, when, then, step
import re

@given('a user exists with email "{email}"')
def step_user_exists(context, email):
    """Creates a user via POST and stores the id."""
    pass

@when("I send a GET request to \\"/api/health\\"")
def step_get_health(context):
    """Health check endpoint."""
    pass

@then('the response status should be {status:d}')
def step_status(context, status):
    pass

@step(re.compile(r"^the result should be (.+)$"))
def step_result(context, result):
    """Regex-based step."""
    pass

@given(f"a user named {name}")
def step_named(context, name, email):
    """F-string pattern."""
    pass

def not_a_step(context):
    """This should not be picked up."""
    pass
'''


def _write_sample_steps(tmp_path: Path) -> Path:
    steps_dir = tmp_path / "features" / "steps"
    steps_dir.mkdir(parents=True)
    f = steps_dir / "my_steps.py"
    f.write_text(SAMPLE_STEPS, encoding="utf-8")
    return steps_dir


# --------------------------------------------------------------------------- #
# scan_file tests
# --------------------------------------------------------------------------- #


def test_scan_file_finds_all_step_decorators(tmp_path: Path) -> None:
    f = tmp_path / "steps.py"
    f.write_text(SAMPLE_STEPS, encoding="utf-8")
    defs = scan_file(f, base_dir=tmp_path)
    # 5 decorated steps, 1 plain function excluded
    assert len(defs) == 5


def test_scan_file_extracts_keywords(tmp_path: Path) -> None:
    f = tmp_path / "steps.py"
    f.write_text(SAMPLE_STEPS, encoding="utf-8")
    defs = scan_file(f, base_dir=tmp_path)
    keywords = sorted(d.keyword for d in defs)
    assert keywords == ["given", "given", "step", "then", "when"]


def test_scan_file_extracts_patterns(tmp_path: Path) -> None:
    f = tmp_path / "steps.py"
    f.write_text(SAMPLE_STEPS, encoding="utf-8")
    defs = scan_file(f, base_dir=tmp_path)
    patterns = {d.func_name: d.pattern for d in defs}
    assert patterns["step_user_exists"] == 'a user exists with email "{email}"'
    assert patterns["step_get_health"] == 'I send a GET request to "/api/health"'
    assert patterns["step_status"] == "the response status should be {status:d}"


def test_scan_file_detects_regex(tmp_path: Path) -> None:
    f = tmp_path / "steps.py"
    f.write_text(SAMPLE_STEPS, encoding="utf-8")
    defs = scan_file(f, base_dir=tmp_path)
    regex_def = next(d for d in defs if d.func_name == "step_result")
    assert regex_def.is_regex is True
    non_regex = next(d for d in defs if d.func_name == "step_user_exists")
    assert non_regex.is_regex is False


def test_scan_file_extracts_params_from_pattern(tmp_path: Path) -> None:
    f = tmp_path / "steps.py"
    f.write_text(SAMPLE_STEPS, encoding="utf-8")
    defs = scan_file(f, base_dir=tmp_path)
    user_def = next(d for d in defs if d.func_name == "step_user_exists")
    assert user_def.params == ["email"]


def test_scan_file_extracts_docstring(tmp_path: Path) -> None:
    f = tmp_path / "steps.py"
    f.write_text(SAMPLE_STEPS, encoding="utf-8")
    defs = scan_file(f, base_dir=tmp_path)
    health = next(d for d in defs if d.func_name == "step_get_health")
    assert health.docstring == "Health check endpoint."


def test_scan_file_extracts_fstring_pattern(tmp_path: Path) -> None:
    f = tmp_path / "steps.py"
    f.write_text(SAMPLE_STEPS, encoding="utf-8")
    defs = scan_file(f, base_dir=tmp_path)
    named = next(d for d in defs if d.func_name == "step_named")
    assert named.pattern == "a user named {name}"


def test_scan_file_relative_path(tmp_path: Path) -> None:
    f = tmp_path / "steps.py"
    f.write_text(SAMPLE_STEPS, encoding="utf-8")
    defs = scan_file(f, base_dir=tmp_path)
    assert defs[0].file_path == "steps.py"


def test_scan_file_empty_file(tmp_path: Path) -> None:
    f = tmp_path / "empty.py"
    f.write_text("", encoding="utf-8")
    assert scan_file(f) == []


def test_scan_file_syntax_error(tmp_path: Path) -> None:
    f = tmp_path / "bad.py"
    f.write_text("def broken(:\n", encoding="utf-8")
    assert scan_file(f) == []


# --------------------------------------------------------------------------- #
# scan_directory tests
# --------------------------------------------------------------------------- #


def test_scan_directory_finds_steps(tmp_path: Path) -> None:
    steps_dir = _write_sample_steps(tmp_path)
    catalog = scan_directory(steps_dir)
    assert catalog.total == 5
    assert "given" in catalog.by_keyword
    assert catalog.by_keyword["given"] == 2


def test_scan_directory_skips_dunder_files(tmp_path: Path) -> None:
    steps_dir = _write_sample_steps(tmp_path)
    (steps_dir / "__init__.py").write_text("# noop\n", encoding="utf-8")
    catalog = scan_directory(steps_dir)
    assert catalog.total == 5


def test_scan_directory_aggregate_metrics(tmp_path: Path) -> None:
    steps_dir = _write_sample_steps(tmp_path)
    catalog = scan_directory(steps_dir)
    assert catalog.with_params > 0
    assert catalog.with_docstring > 0
    assert catalog.regex_steps == 1
    assert len(catalog.by_file) == 1


def test_scan_directory_empty_dir(tmp_path: Path) -> None:
    steps_dir = tmp_path / "steps"
    steps_dir.mkdir()
    catalog = scan_directory(steps_dir)
    assert catalog.total == 0
    assert catalog.steps == []


# --------------------------------------------------------------------------- #
# StepCatalog properties
# --------------------------------------------------------------------------- #


def test_step_catalog_by_keyword() -> None:
    cat = StepCatalog(steps=[
        StepDefinition(keyword="given", pattern="", is_regex=False, func_name="a", file_path="f.py", line=1, end_line=1, docstring=""),
        StepDefinition(keyword="given", pattern="", is_regex=False, func_name="b", file_path="f.py", line=2, end_line=2, docstring=""),
        StepDefinition(keyword="when", pattern="", is_regex=False, func_name="c", file_path="f.py", line=3, end_line=3, docstring=""),
    ])
    assert cat.total == 3
    assert cat.by_keyword == {"given": 2, "when": 1}


def test_step_catalog_with_params_and_docstring() -> None:
    cat = StepCatalog(steps=[
        StepDefinition(keyword="given", pattern="", is_regex=False, func_name="a", file_path="f.py", line=1, end_line=1, docstring="", params=["x"]),
        StepDefinition(keyword="when", pattern="", is_regex=False, func_name="b", file_path="f.py", line=2, end_line=2, docstring="docs"),
    ])
    assert cat.with_params == 1
    assert cat.with_docstring == 1


# --------------------------------------------------------------------------- #
# render_step_catalog tests
# --------------------------------------------------------------------------- #


def test_render_step_catalog_basic() -> None:
    cat = StepCatalog(steps=[
        StepDefinition(
            keyword="given",
            pattern='a user exists with email "{email}"',
            is_regex=False,
            func_name="step_user_exists",
            file_path="api_steps.py",
            line=21,
            end_line=34,
            docstring="Creates a user via POST.",
            params=["email"],
            source="def step_user_exists(context, email):\n    pass\n",
        ),
    ])
    md = render_step_catalog(cat, title="Test Catalog")
    assert "# 📋 Test Catalog" in md
    assert "Statistics" in md
    assert "Steps by Keyword" in md
    assert "Steps by File" in md
    assert "Step Definitions" in md
    assert "step_user_exists" in md
    assert "api_steps.py" in md


def test_render_step_catalog_empty() -> None:
    cat = StepCatalog()
    md = render_step_catalog(cat)
    assert "0 step definitions" in md
    assert "Step Definitions" in md


def test_render_step_catalog_contains_collapsible_details() -> None:
    cat = StepCatalog(steps=[
        StepDefinition(
            keyword="when",
            pattern="I do something",
            is_regex=False,
            func_name="step_do",
            file_path="steps.py",
            line=1,
            end_line=2,
            docstring="Does something.",
            params=[],
            source="def step_do(context):\n    pass\n",
        ),
    ])
    md = render_step_catalog(cat)
    assert "<details>" in md
    assert "</details>" in md
    assert "I do something" in md
