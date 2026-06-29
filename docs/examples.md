# Examples

The repository includes two example projects under `examples/`.

## Demo generator

`examples/demo_generator/` contains a standalone script that builds a synthetic
execution and renders it as Markdown. It is useful for design iteration and
quick demos without a real Behave suite.

```bash
python examples/demo_generator/generate_demo.py
```

Output: `examples/demo_generator/demo-report.md`.

## Functional Behave project

`examples/behave_project/` is a complete Behave project with features, steps,
`environment.py` hooks, and `behave.ini` configured to use the Markdown formatter.

Install dependencies:

```bash
cd examples/behave_project
pip install -r requirements.txt
```

Run the suite:

```bash
behave
```

It generates `report.md` in the same directory. The project exercises:

- Backgrounds and scenario outlines.
- Gherkin `Rule` groups (requires Behave 1.3.x).
- Passing, failing, skipped, pending, and undefined scenarios.
- Attachments on failure (text, JSON, and a screenshot).
- Slow scenarios with duration timing.
- Custom `bmr.title` and `bmr.company` userdata.

Run a subset of features:

```bash
behave --tags=login
behave --tags=checkout
behave --tags=smoke
```

## Sample report

A pre-generated example report is committed at `examples/report.md` and linked
from the main README.
