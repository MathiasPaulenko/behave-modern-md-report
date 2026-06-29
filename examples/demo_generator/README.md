# Demo Generator

This directory contains a standalone script that generates a synthetic Markdown report without running Behave.

## Purpose

- Preview the report layout and styling without needing a real Behave project.
- Generate screenshots or documentation examples.
- Test renderer changes quickly.

## Files

- `generate_demo.py` — builds a synthetic `Execution` model and renders it to Markdown.
- `demo-report.md` — the generated report (created when you run the script).

## Why no `features/` or `steps/`?

Unlike `examples/behave_project/`, this demo does not use Behave at all. It constructs the report model programmatically, so there are no Gherkin files or step implementations.

## Run

From the repository root:

```bash
python examples/demo_generator/generate_demo.py
```

The script writes `demo-report.md` in this directory and tries to open it in your default browser or Markdown viewer.

## Customize

Edit `generate_demo.py` to change the number of features, scenarios, statuses, or attachment examples. The script uses `MarkdownRenderer` and `RenderOptions` directly, so you can experiment with any rendering option without touching a `behave.ini` file.
