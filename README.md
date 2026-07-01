# Behave Markdown Report

[![PyPI](https://img.shields.io/badge/pypi-behave--modern--md--report-blue)](https://pypi.org/p/behave-modern-md-report)
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/)
[![CI](https://img.shields.io/badge/CI-GitHub%20Actions-brightgreen)](.github/workflows/ci.yml)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

A modern, readable, CI/CD-friendly Markdown report formatter for the [Behave](https://github.com/behave/behave) BDD framework.

It generates a single `report.md` that you can publish directly to GitHub, GitHub Actions Summaries, GitLab, Azure DevOps, Jenkins, Bitbucket, wikis, or any Markdown viewer.

See a generated example report at [`examples/report.md`](examples/report.md).

## Table of Contents

- [Why Markdown?](#why-markdown)
- [Features](#features)
- [Installation](#installation)
- [Quick start](#quick-start)
- [Configuration](#configuration)
- [Attachments](#attachments)
- [Examples](#examples)
- [Report layout](#report-layout)
- [Architecture](#architecture)
- [Documentation](#documentation)
- [Development](#development)
- [Changelog](#changelog)
- [License](#license)

## Why Markdown?

- **Works everywhere** — no JavaScript, no external assets, no HTML sanitization issues.
- **CI-native** — GitHub Actions, GitLab, and Azure DevOps render Markdown summaries out of the box.
- **Diff-friendly** — line-based changes make PR reviews easier.
- **Portable** — one file, easy to archive, email, or paste into an issue.

## Features

- **Single-file Markdown output** with a table of contents and internal links.
- **Executive summary** showing passed, failed, and skipped counts with status icons.
- **Feature summary** table with links and durations.
- **Tag statistics** table with pass rate per tag.
- **Failed scenarios** section with error messages and tracebacks.
- **Slowest scenarios** top-10 list.
- **Scenario details** with collapsible sections, Gherkin backgrounds, data tables, and doc strings.
- **Environment section** with Python, Behave, OS, Git, and CI environment details.
- **Step catalog** formatter that statically analyses `features/steps/` and produces a Markdown catalog with patterns, parameters, docstrings, source code, and statistics.
- **Attachments** rendered inline: images, JSON, XML, HTML, logs, and plain text.
- **No heavy dependencies** — only the Python standard library and `behave`.

## Installation

Install from PyPI:

```bash
pip install behave-modern-md-report
```

Or install from source:

```bash
git clone https://github.com/MathiasPaulenko/behave-modern-md-report.git
cd behave-modern-md-report
pip install -e .
```

For development, install with the extra dependencies:

```bash
pip install -e ".[dev]"
```

## Quick start

### Markdown report

1. Create or update `behave.ini` in your Behave project root:

```ini
[behave]
format = markdown
outfiles = report.md

[behave.formatters]
markdown = behave_modern_md_report.formatter:BehaveMarkdownFormatter
```

2. Run Behave:

```bash
behave
```

3. Open `report.md` in any Markdown viewer.

If you prefer not to register the short name, use the full formatter path:

```bash
behave -f behave_modern_md_report.formatter:BehaveMarkdownFormatter -o report.md
```

### Step catalog

1. Register the formatter in `behave.ini`:

```ini
[behave.formatters]
stepcatalog = behave_modern_md_report.step_catalog_formatter:StepCatalogMarkdownFormatter
```

2. Run Behave with the `stepcatalog` formatter:

```bash
behave -f stepcatalog -o step_catalog.md --no-skipped
```

3. Open `step_catalog.md` — it contains a table of all step definitions, their patterns, parameters, docstrings, source code, and aggregate statistics.

You can also combine both formatters in a single run:

```ini
[behave]
format = markdown
    stepcatalog
outfiles = report.md
    step_catalog.md
```

## Configuration

All options are passed through Behave's `userdata` mechanism. Add a `[behave.userdata]` section to `behave.ini`:

```ini
[behave.userdata]
bmr.title = My Report
bmr.project_name = My Project
bmr.company = My Company
bmr.include_passed = true
bmr.include_skipped = true
bmr.include_traceback = true
bmr.include_environment = true
bmr.sort_failed_first = true
bmr.max_traceback_lines = 0
bmr.steps_dir = features/steps
```

You can also override options from the command line:

```bash
behave -D bmr.title="Nightly Report" -D bmr.include_environment=false
```

See [docs/configuration.md](docs/configuration.md) for the full reference and troubleshooting.

## Attachments

Capture screenshots, logs, JSON, or files directly from your `features/environment.py` hooks:

```python
from behave_modern_md_report import attach_screenshot, log

def after_step(context, step):
    if step.status == "failed":
        log(context, f"URL at failure: {getattr(context, 'url', 'unknown')}")
        attach_screenshot(context, getattr(context, "driver", None), name="failure.png")
```

See [docs/attachments.md](docs/attachments.md) for the full attachment API and supported MIME types.

## Examples

The repository includes two examples:

- `examples/behave_project/` — a complete Behave project that exercises all report sections.
- `examples/demo_generator/` — a script that generates a synthetic `demo-report.md` without running Behave.

Run the example project:

```bash
cd examples/behave_project
behave
```

Generate the demo report:

```bash
python examples/demo_generator/generate_demo.py
```

## Report layout

A generated report contains the following sections in order:

```markdown
# My Report

## Table of Contents
## Executive Summary
## Statistics
## Feature Summary
## Tags
## Failed Scenarios
## Slowest Scenarios
## Scenario Details
## Environment
```

Each section is linked from the table of contents. Scenario details are wrapped in collapsible `<details>` blocks so the report stays readable even for large suites.

## Architecture

Behave Markdown Report uses a clean, layered architecture:

| Layer | File | Responsibility |
| ----- | ---- | -------------- |
| Formatter | `formatter.py` | Adapts Behave events to the collector. |
| Collector | `collector.py` | Builds the `Execution` model from Behave objects. |
| Models | `models.py` | Pure dataclasses representing the test tree. |
| Statistics | `statistics.py` | Computes aggregates and derived metrics. |
| Renderer | `renderer.py` | Turns the `Execution` model into Markdown. |
| Markdown | `markdown.py` | Low-level Markdown document helpers. |
| Attach API | `attach.py` | Convenience helpers for `environment.py`. |

See [docs/architecture.md](docs/architecture.md) for the full architecture and data flow.

## Documentation

- [docs/configuration.md](docs/configuration.md) — all `bmr.*` options and troubleshooting.
- [docs/attachments.md](docs/attachments.md) — attaching screenshots, JSON, files, and logs.
- [docs/ci-cd.md](docs/ci-cd.md) — GitHub Actions, GitLab CI, Azure DevOps, and Jenkins examples.
- [docs/customizing.md](docs/customizing.md) — subclassing the renderer and building custom themes.
- [docs/architecture.md](docs/architecture.md) — project structure and data flow.

## Development

Install the development dependencies:

```bash
pip install -e ".[dev]"
```

Run the test suite:

```bash
pytest
```

Run the linter:

```bash
ruff check behave_modern_md_report tests
```

Run the type checker:

```bash
mypy behave_modern_md_report
```

Build the package:

```bash
python -m build
```

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for the release history.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
