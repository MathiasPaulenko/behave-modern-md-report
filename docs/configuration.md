# Configuration

All rendering options are passed through Behave's `userdata` mechanism. This means the formatter works with any standard Behave configuration source: `behave.ini`, CLI flags, or environment variables.

## Minimal `behave.ini`

```ini
[behave]
format = markdown
outfiles = report.md

[behave.formatters]
markdown = behave_modern_md_report.formatter:BehaveMarkdownFormatter
```

With this file in place, run `behave` and open `report.md`.

## Full `behave.ini` example

```ini
[behave]
format = markdown
outfiles = report.md

[behave.formatters]
markdown = behave_modern_md_report.formatter:BehaveMarkdownFormatter

[behave.userdata]
bmr.title = My Markdown Report
bmr.project_name = My Project
bmr.company = My Company
bmr.include_passed = true
bmr.include_skipped = true
bmr.include_traceback = true
bmr.include_environment = true
bmr.sort_failed_first = true
bmr.max_traceback_lines = 0
bmr.max_summary_features = 0
```

## Options reference

| Option | Type | Default | Description |
| ------ | ---- | ------- | ----------- |
| `bmr.title` | string | `Behave Markdown Report` | Report title shown in the main heading. |
| `bmr.project_name` | string | `""` | Project name shown in the header. |
| `bmr.company` | string | `""` | Company name shown in the header. |
| `bmr.include_passed` | boolean | `true` | Include passed scenarios in the collapsible details section. |
| `bmr.include_skipped` | boolean | `true` | Include skipped scenarios in the collapsible details section. |
| `bmr.include_traceback` | boolean | `true` | Render tracebacks for failed steps. |
| `bmr.include_environment` | boolean | `true` | Render the environment section. |
| `bmr.sort_failed_first` | boolean | `true` | Sort failed features first in the feature summary. |
| `bmr.max_traceback_lines` | integer | `0` | Limit traceback lines; `0` means unlimited. |
| `bmr.max_summary_features` | integer | `0` | Limit feature summary rows; `0` means unlimited. |

Boolean values accept `true`/`false`, `yes`/`no`, `1`/`0`, or `on`/`off`.

## Alternative ways to configure

### Command line

```bash
behave -D bmr.title="Nightly Report" -D bmr.include_environment=false
```

### Environment variables

Behave supports `BEHAVE_USERDATA_bmr_title` style environment variables on most platforms:

```bash
export BEHAVE_USERDATA_bmr_title="Nightly Report"
behave
```

### Programmatically in `environment.py`

```python
def before_all(context):
    context.config.userdata.setdefault("bmr.title", "Custom Report")
```

## Output path

The report is written to the path configured by Behave's `outfiles` option. If no path is provided, the formatter falls back to `behave-modern-md-report.md`.

Examples:

```ini
[behave]
format = markdown
outfiles = reports/behave-report.md
```

```bash
behave -f markdown -o reports/behave-report.md
```

## Disabling sections

Set the corresponding boolean option to `false` to hide a section:

```ini
[behave.userdata]
bmr.include_environment = false
bmr.include_traceback = false
```

This is useful for very large suites where the environment or traceback sections would make the report too long.

## Troubleshooting

### `BAD_FORMAT=markdown (problem: LookupError)`

The formatter is not registered. Add this to `behave.ini` (in the working directory):

```ini
[behave.formatters]
markdown = behave_modern_md_report.formatter:BehaveMarkdownFormatter
```

Alternatively, use the full module path on the CLI:

```bash
behave -f behave_modern_md_report.formatter:BehaveMarkdownFormatter -o report.md
```

### Report is empty or says "Untested"

Ensure the formatter class is used by Behave and not a custom subclass that bypasses the collector. The example project in `examples/behave_project/` demonstrates a working setup.
