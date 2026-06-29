# Architecture

Behave Markdown Report is built around a clean, layered architecture that separates the concerns of collecting test data, computing statistics, and rendering Markdown. This design makes the formatter easy to understand, test, and extend.

## Data flow

```text
Behave events
      |
      v
+-----------------+
|   Formatter     |  formatter.py
|  (behaviour.py) |
+--------+--------+
         |
         v
+-----------------+
|    Collector    |  collector.py
|  builds model   |
+--------+--------+
         |
         v
+-----------------+
|     Models      |  models.py
|  (Execution)    |
+--------+--------+
         |
         v
+-----------------+
|   Statistics    |  statistics.py
|  computes stats |
+--------+--------+
         |
         v
+-----------------+
|    Renderer     |  renderer.py
|  -> Markdown    |
+--------+--------+
         |
         v
+-----------------+
|    Markdown     |  markdown.py
|   helpers       |
+-----------------+
         |
         v
     report.md
```

## Layers

| Layer | File | Responsibility |
| ----- | ---- | -------------- |
| **Formatter** | `formatter.py` | Adapts Behave lifecycle events (`feature`, `scenario`, `step`, `eof`) into calls on the collector. Also exposes the attachment API used by `environment.py`. |
| **Collector** | `collector.py` | Builds a pure `Execution` model from Behave objects. Handles status normalization, feature/scenario finalization, and background steps. |
| **Models** | `models.py` | Immutable-style dataclasses that represent the test tree: `Execution`, `Feature`, `Scenario`, `Step`, `Attachment`, `ErrorInfo`, etc. |
| **Statistics** | `statistics.py` | Computes aggregates such as pass rate, duration, slowest scenarios, tag counts, and common exception types. |
| **Renderer** | `renderer.py` | Transforms the `Execution` model into a single Markdown document using `RenderOptions`. |
| **Markdown** | `markdown.py` | Low-level helpers for headings, tables, lists, code blocks, blockquotes, and inline images. |
| **Attach API** | `attach.py` | High-level helpers (`attach_text`, `attach_json`, `attach_screenshot`, `log`) that find the active formatter from the Behave context. |
| **Utilities** | `utils.py` | Small shared helpers such as MIME type guessing and safe string conversion. |

## Key design decisions

### Behave-independent renderer

The renderer only knows the `Execution` model. It does not import Behave, which makes it easy to test and reuse outside of Behave if needed.

### Status derivation

Behave does not always provide a final status for features and scenarios. The collector therefore derives:

* **Scenario status** from its step statuses when Behave leaves it as `untested`.
* **Feature status** from its scenario statuses in the statistics module.

This guarantees that the report always shows meaningful status icons and counts.

### Event-driven collection

The formatter implements the standard Behave formatter API (`feature`, `scenario`, `step`, `result`, `eof`). The collector stores minimal state:

* the current `Execution`
* the current `Feature`
* the current `Scenario`

When a new feature or scenario starts, the previous one is finalized automatically.

### Single-file Markdown output

The renderer produces one Markdown string. The formatter writes it to disk at the end of the run. This makes the report trivial to archive, publish, or paste into CI summaries.

## Extending the report

### Adding a new `bmr.*` option

1. Add a field to `RenderOptions` in `renderer.py`.
2. Read it from `userdata` in `RenderOptions.from_userdata()`.
3. Use it in `MarkdownRenderer` to change rendering behaviour.
4. Document it in `docs/configuration.md`.

### Adding a custom statistic

1. Add a field to `Statistics` in `models.py`.
2. Compute it in `statistics.compute()`.
3. Render it in `renderer.py` if needed.

### Adding a new attachment type

1. If it can be represented as a MIME type, the existing `Attachment` model already supports it.
2. Add a helper in `attach.py` if end users should call it from `environment.py`.
3. Ensure the renderer handles the MIME type in `_render_attachment()`.

## Future extensibility

The architecture supports future features without breaking the core:

* **Multiple Markdown themes**: subclass `MarkdownRenderer` and override rendering methods.
* **Mermaid diagrams**: generate a Markdown code block with language `mermaid` from the execution model.
* **Historical reports**: serialize `Execution` to JSON, store it, and compare runs later.
* **Plugin system**: register custom renderers via a new entry point.
