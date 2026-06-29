"""Tests for the Markdown builder helpers."""

from __future__ import annotations

from behave_modern_md_report.markdown import MarkdownBuilder, markdown_table


def test_heading():
    md = MarkdownBuilder()
    md.heading(1, "Title")
    assert md.lines == ["# Title"]


def test_table_basic():
    md = MarkdownBuilder()
    md.table(["A", "B"], [["1", "2"], ["3", "4"]])
    output = md.join()
    assert "| A   | B   |" in output
    assert "| --- | --- |" in output
    assert "| 1   | 2   |" in output


def test_table_pads_short_columns():
    md = MarkdownBuilder()
    md.table(["X", "Y"], [["a", "b"]])
    output = md.join()
    assert "| X   | Y   |" in output
    assert "| --- | --- |" in output


def test_details():
    md = MarkdownBuilder()
    md.details("Summary", ["line 1", "line 2"])
    output = md.join()
    assert "<details>" in output
    assert "<summary>Summary</summary>" in output
    assert "line 1" in output


def test_markdown_table_from_dicts():
    rows = [{"name": "A", "value": "1"}, {"name": "B", "value": "2"}]
    output = markdown_table(rows)
    assert "| name | value |" in output
    assert "| A    | 1     |" in output


def test_escape():
    md = MarkdownBuilder()
    assert md.escape("*bold*") == "\\*bold\\*"
