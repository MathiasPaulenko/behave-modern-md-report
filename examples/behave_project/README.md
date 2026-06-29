# Behave Project Example

A functional Behave project used to test `behave-modern-md-report`.

## Features

- **Login**: background, scenario outline, pending/undefined steps.
- **Checkout**: Gherkin `Rule` grouping, background, passing and failing scenarios.
- **Reporting**: skipped/pending scenario, slow scenario, attachment on failure.

## Requirements

Install the dependencies from this directory:

```bash
pip install -r requirements.txt
```

This installs `behave` and the reporter in editable mode (`-e ../..`).

## Run

From this directory:

```bash
behave
```

This uses `behave.ini` and generates `report.md` with the Markdown formatter.

## View report

Open `report.md` in any Markdown viewer or GitHub.

## Report customization

The example `behave.ini` configures a few reporter options through `userdata`:

```ini
[behave.userdata]
bmr.title = Behave Project Example
bmr.company = Open Source
bmr.include_passed = true
bmr.include_skipped = true
bmr.include_traceback = true
bmr.include_environment = true
```

You can also override them from `environment.py`:

```python
def before_all(context):
    context.config.userdata.set("bmr.title", "My Custom Title")
```

See the main [Configuration](../../docs/configuration.md) docs for the full list of options.

## Advanced

Run a subset of features:

```bash
behave --tags=login
behave --tags=checkout
behave --tags=smoke
```

Run without installing the package (from the repo root):

```bash
PYTHONPATH=. python -m behave examples/behave_project/features
```
