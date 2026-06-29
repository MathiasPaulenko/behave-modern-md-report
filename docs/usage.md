# Usage

## Installation

```bash
pip install behave-modern-md-report
```

## Basic configuration

Register the formatter in your `behave.ini`:

```ini
[behave.formatters]
markdown = behave_modern_md_report.formatter:BehaveMarkdownFormatter
```

Then run Behave as usual:

```bash
behave -f markdown -o report.md
```

You can also use it via `setup.cfg` or `tox.ini` with the same `[behave.formatters]` section.

## Using a single feature file

```bash
behave -f markdown -o report.md features/login.feature
```

## Combining with other formatters

Behave supports multiple formatters at once. For example, keep the console
output while generating the Markdown report:

```bash
behave -f pretty -o /dev/null -f markdown -o report.md
```

On Windows use `NUL` instead of `/dev/null`:

```powershell
behave -f pretty -o NUL -f markdown -o report.md
```

## Using the fully qualified formatter name

If you do not want to register the short name, use the full module path:

```bash
behave -f behave_modern_md_report.formatter:BehaveMarkdownFormatter -o report.md
```

## Generating a demo report

If you want to see the report without a real Behave suite, use the demo
generator:

```bash
python examples/demo_generator/generate_demo.py
```

This writes `examples/demo_generator/demo-report.md` with a realistic-looking
execution and opens it in the default Markdown viewer.

## Publishing in CI

The report is a single Markdown file. In GitHub Actions you can publish it as a
job summary:

```bash
behave -f markdown -o report.md
cat report.md >> "$GITHUB_STEP_SUMMARY"
```

See [docs/ci-cd.md](ci-cd.md) for more CI/CD integrations.
