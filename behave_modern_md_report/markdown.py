"""Low-level Markdown building helpers.

The renderer uses these helpers to emit valid, portable GitHub Flavored
Markdown. This module has no dependency on Behave or the execution model.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class MarkdownBuilder:
    """Incremental Markdown document builder."""

    lines: list[str] = field(default_factory=list)

    def text(self, content: str) -> MarkdownBuilder:
        """Append a plain text line."""
        self.lines.append(content)
        return self

    def blank(self) -> MarkdownBuilder:
        """Append a blank line."""
        self.lines.append("")
        return self

    def heading(self, level: int, text: str) -> MarkdownBuilder:
        """Append a Markdown heading."""
        self.lines.append(f"{'#' * level} {text}")
        return self

    def paragraph(self, text: str) -> MarkdownBuilder:
        """Append a paragraph."""
        self.lines.append(text)
        self.lines.append("")
        return self

    def bold(self, text: str) -> str:
        """Return bold text."""
        return f"**{text}**"

    def italic(self, text: str) -> str:
        """Return italic text."""
        return f"*{text}*"

    def code_inline(self, text: str) -> str:
        """Return inline code."""
        return f"`{text}`"

    def code_block(self, code: str, language: str = "") -> MarkdownBuilder:
        """Append a fenced code block."""
        self.lines.append(f"```{language}")
        for line in code.splitlines():
            self.lines.append(line)
        self.lines.append("```")
        return self

    def blockquote(self, text: str | list[str]) -> MarkdownBuilder:
        """Append a blockquote."""
        if isinstance(text, list):
            text = "\n".join(text)
        for line in text.splitlines():
            self.lines.append(f"> {line}")
        self.lines.append("")
        return self

    def horizontal_rule(self) -> MarkdownBuilder:
        """Append a horizontal rule."""
        self.lines.append("---")
        return self

    def table(self, headers: list[str], rows: list[list[str]]) -> MarkdownBuilder:
        """Append a Markdown table with aligned numeric columns."""
        if not headers:
            return self
        widths = [len(h) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                if i < len(widths):
                    widths[i] = max(widths[i], len(cell))
        # Make each column at least 3 characters wide so the separator renders.
        widths = [max(w, 3) for w in widths]

        def _row(cells: list[str]) -> str:
            parts = [cell.ljust(widths[i]) for i, cell in enumerate(cells)]
            return f"| {' | '.join(parts)} |"

        def _sep() -> str:
            parts = ["-" * w for w in widths]
            return f"| {' | '.join(parts)} |"

        self.lines.append(_row(headers))
        self.lines.append(_sep())
        for row in rows:
            padded = row + [""] * (len(headers) - len(row))
            self.lines.append(_row(padded))
        return self

    def task_list(self, items: list[tuple[str, bool]]) -> MarkdownBuilder:
        """Append a task list."""
        for label, checked in items:
            marker = "[x]" if checked else "[ ]"
            self.lines.append(f"- {marker} {label}")
        self.lines.append("")
        return self

    def bullet(self, items: list[str]) -> MarkdownBuilder:
        """Append a bullet list."""
        for item in items:
            self.lines.append(f"- {item}")
        self.lines.append("")
        return self

    def ordered(self, items: list[str]) -> MarkdownBuilder:
        """Append an ordered list."""
        for i, item in enumerate(items, 1):
            self.lines.append(f"{i}. {item}")
        self.lines.append("")
        return self

    def link(self, text: str, anchor: str) -> str:
        """Return an internal Markdown link."""
        anchor = anchor.lower().strip().replace(" ", "-").replace("_", "-")
        anchor = "".join(c for c in anchor if c.isalnum() or c == "-")
        return f"[{text}](#{anchor})"

    def external_link(self, text: str, url: str) -> str:
        """Return an external Markdown link."""
        return f"[{text}]({url})"

    def image(self, alt: str, src: str) -> str:
        """Return a Markdown image."""
        return f"![{alt}]({src})"

    def details(self, summary: str, content_lines: list[str], open_: bool = False) -> MarkdownBuilder:
        """Append an HTML details block.

        Native Markdown cannot represent collapsible sections, so this is the
        only place where we intentionally use HTML.

        """
        open_attr = " open" if open_ else ""
        self.lines.append(f"<details{open_attr}>")
        self.lines.append(f"<summary>{summary}</summary>")
        self.lines.append("")
        for line in content_lines:
            self.lines.append(line)
        self.lines.append("")
        self.lines.append("</details>")
        return self

    def escape(self, text: str) -> str:
        """Escape Markdown special characters in a text fragment."""
        chars = ("\\", "`", "*", "_", "{", "}", "[", "]", "(", ")", "#", "+", "-", ".", "!", "|")
        for char in chars:
            text = text.replace(char, f"\\{char}")
        return text

    def join(self, separator: str = "\n") -> str:
        """Return the assembled Markdown document."""
        return separator.join(self.lines).strip() + separator


def markdown_table(rows: list[dict[str, Any]]) -> str:
    """Render a list of dicts as a Markdown table.

    Args:
        rows: List of dictionaries, each representing a row. All rows must share
            the same keys. The first row's keys define the headers.

    Returns:
        Markdown table string.

    """
    if not rows:
        return ""
    headers = list(rows[0].keys())
    str_rows = [[str(row.get(h, "")) for h in headers] for row in rows]
    builder = MarkdownBuilder()
    builder.table(headers, str_rows)
    return builder.join()
