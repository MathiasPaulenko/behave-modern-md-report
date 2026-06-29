# Attachments and logs

The formatter can embed diagnostic artifacts directly into the Markdown report. This is useful for debugging failures in CI or for preserving evidence from a test run.

## Available helpers

Import the helpers in your `features/environment.py`:

```python
from behave_modern_md_report import (
    attach_file,
    attach_json,
    attach_screenshot,
    attach_text,
    log,
)
```

| Helper | Purpose |
| ------ | ------- |
| `log(context, message)` | Append a plain text line to the current step. |
| `attach_text(context, text, name="note.txt")` | Attach a text snippet. |
| `attach_json(context, data, name="data.json")` | Attach any JSON-serializable object. |
| `attach_file(context, path, name=None)` | Attach a file from disk. |
| `attach_screenshot(context, source, name="screenshot.png")` | Attach a screenshot image. |

All helpers are safe to call even when the Markdown formatter is not active: they simply do nothing.

## Typical failure hook

A common pattern is to attach evidence only when a step fails:

```python
def after_step(context, step):
    if step.status == "failed":
        log(context, f"Step failed: {step.name}")
        attach_text(context, f"URL at failure: {getattr(context, 'url', 'unknown')}")
        attach_json(context, {"status_code": getattr(context, 'status_code', None)})
        attach_screenshot(context, context.driver, name="failure.png")
```

## Screenshot sources

`attach_screenshot` accepts several source types:

* **Selenium WebDriver**: `attach_screenshot(context, context.driver)`
* **Playwright Page**: `attach_screenshot(context, context.page)`
* **PIL Image**: `attach_screenshot(context, image)`
* **Raw bytes**: `attach_screenshot(context, png_bytes)`
* **File path**: `attach_screenshot(context, "screenshots/failure.png")`

The MIME type is inferred from the file extension or the source object.

## Supported attachment types in the report

The renderer displays attachments based on their MIME type:

| MIME type | Rendering |
| --------- | --------- |
| `image/png`, `image/jpeg`, `image/webp`, `image/gif` | Inline base64 image |
| `application/json` | Fenced `json` code block |
| `application/xml`, `application/xhtml+xml` | Fenced `xml` code block |
| `text/html` | Fenced `html` code block |
| `text/plain` | Fenced `text` code block |
| Other | Fenced `text` code block |

## Logs

Logs are rendered as a `text` code block inside the failed step. They are also counted in the report statistics.
