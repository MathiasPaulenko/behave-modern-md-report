# Contributing

Thanks for your interest in making **Behave Markdown Report** better!

## Local setup

```bash
git clone https://github.com/MathiasPaulenko/behave-modern-md-report.git
cd behave-modern-md-report
python -m venv .venv
. .venv/Scripts/activate   # PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
pip install -e .
```

Or use the provided `Makefile`:

```bash
make install-dev
```

## Releasing

Releases are **fully automatic**. To cut a new version:

1. Bump the `version` field in `pyproject.toml`.
2. Update `CHANGELOG.md`.
3. Commit and push to `main`.

The `Release` GitHub Actions workflow detects the version bump, creates the
matching `vX.Y.Z` tag, builds the distribution, publishes to PyPI via
Trusted Publishing, and creates a GitHub Release with auto-generated notes.

If the version was not changed, the workflow exits cleanly without releasing.

## Running checks

```bash
make test
make lint
make typecheck
```

Equivalently:

```bash
python -m pytest -ra
python -m ruff check .
python -m mypy behave_modern_md_report
python -m black --check .
```

## Iterating on the report

The fastest loop is to regenerate the demo report and inspect it:

```bash
python examples/demo_generator/generate_demo.py
```

Open `examples/demo_generator/demo-report.md` in any Markdown viewer and refresh after each change.

You can also run the example Behave project:

```bash
cd examples/behave_project
behave
```

## Project conventions

- Python 3.11+, type hints everywhere, Google-style docstrings.
- Dataclasses for models (no Pydantic dependency).
- No external CSS/JS — the report is plain Markdown.
- Keep layers separated: formatter ↔ collector ↔ models ↔ statistics ↔ renderer.

## Adding a new `bmr.*` option

1. Add a field to `RenderOptions` in `renderer.py`.
2. Read it from `userdata` in `RenderOptions.from_userdata()`.
3. Use it in `MarkdownRenderer` to change rendering behaviour.
4. Document it in `docs/configuration.md`.
5. Add a unit test if the logic is non-trivial.

## Adding a new model field

1. Add the field to the dataclass in `models.py`.
2. Populate it in `collector.py`.
3. Surface it in the renderer.
4. Add a unit test.
