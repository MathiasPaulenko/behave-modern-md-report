# Customizing the report

You can change the report content through configuration options, or you can extend the renderer for deeper customization.

## Configuration-driven changes

The easiest way to change the report is through `behave.ini` options. See [configuration.md](configuration.md) for the full list.

Examples:

```ini
[behave.userdata]
bmr.title = Nightly Regression Report
bmr.include_environment = true
bmr.include_passed = false
bmr.max_traceback_lines = 20
```

This changes the report without writing any Python code.

## Customizing via `RenderOptions`

If you use the renderer outside of Behave, build a `RenderOptions` object:

```python
from behave_modern_md_report import MarkdownRenderer, RenderOptions

options = RenderOptions(
    title="Custom Report",
    project_name="My Project",
    company="My Company",
    include_passed_scenarios=False,
    include_traceback=True,
)
renderer = MarkdownRenderer(options)
markdown = renderer.render(execution)
```

## Subclassing the renderer

For full control over the Markdown output, subclass `MarkdownRenderer` and override the methods that generate each section.

```python
from behave_modern_md_report.renderer import MarkdownRenderer
from behave_modern_md_report.markdown import MarkdownBuilder

class CompactRenderer(MarkdownRenderer):
    def _render_environment(self, md, execution):
        # Skip the environment section entirely.
        return

    def _render_executive_summary(self, md, stats):
        # Render a single-line summary instead of a table.
        md.heading(f"{stats.passed_scenario_count} passed, {stats.failed_scenario_count} failed", level=2)
```

Then use it in a custom formatter or standalone script:

```python
renderer = CompactRenderer(options)
markdown = renderer.render(execution)
```

## Adding custom sections

Override `_render_body` or call the renderer methods in your own order:

```python
class CustomRenderer(MarkdownRenderer):
    def _render_body(self, md, execution):
        self._render_header(md, execution)
        self._render_executive_summary(md, execution.statistics)
        self._render_feature_summary(md, execution)
        self._render_failed_scenarios(md, execution)
        md.heading("Custom notes", level=2)
        md.paragraph("This section is added by a custom renderer.")
        self._render_environment(md, execution)
        self._render_footer(md, execution)
```

## Custom status icons

The status icon mapping is defined in `renderer.py` as `_STATUS_ICONS`. You can replace it by overriding the renderer or by monkey-patching before rendering:

```python
from behave_modern_md_report import renderer

renderer._STATUS_ICONS["passed"] = "✔"
renderer._STATUS_ICONS["failed"] = "✘"
```

## Custom themes

A "theme" is just a renderer subclass. You can ship multiple themes in the same package by exposing them as entry points or class aliases:

```ini
[behave.formatters]
markdown_compact = my_package.renderers:CompactRenderer
```

## When to customize

* Use **configuration options** for common changes (title, sections, limits).
* Use **renderer subclassing** for layout changes, new sections, or custom Markdown formatting.
* Keep custom renderers in your own project or a separate package to avoid forking the formatter.
