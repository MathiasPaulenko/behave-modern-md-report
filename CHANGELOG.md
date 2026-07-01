# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.2.0] - 2026-07-01

### Added

- New `stepcatalog` formatter that statically analyses `features/steps/` and produces a Markdown step catalog with patterns, parameters, docstrings, source code, and aggregate statistics.
- `StepCatalogMarkdownFormatter` exported from the public API.
- `bmr.steps_dir` configuration option to customise the steps directory path.
- `examples/step_catalog.md` example file tracked in Git.
- 19 unit tests covering the step scanner and catalog renderer.

## [1.1.0] - 2026-06-29

### Added

- Features in the Scenario Details section are now collapsible (`<details>` blocks), grouping scenarios per feature.

### Changed

- `examples/report.md` is now tracked in Git so the README example link works on GitHub.

### Fixed

- Markdown spacing around horizontal rules, headings, tables, and `<details>` blocks so the report renders correctly in all Markdown viewers.
- Missing blank lines before the "CI / Environment Variables" heading.
- Warning status icon (`⚠️`) now uses the emoji variant for consistent rendering with other status icons.

## [1.0.0] - 2026-06-29

### Added

- Initial release of `behave-modern-md-report`.
- Behave formatter producing a single Markdown file.
- Executive summary with status counts and icons.
- Statistics section with pass rate, duration, and error distribution.
- Feature summary table with internal links and durations.
- Tag statistics table with pass rate per tag.
- Failed scenarios section with error messages and tracebacks.
- Slowest scenarios top 10 list.
- Scenario details wrapped in collapsible HTML `<details>` blocks.
- Gherkin background and scenario outline support with `Examples` tables.
- Gherkin `Rule` support (requires Behave 1.3.x).
- Environment section with Python, Behave, OS, hostname, user, git, CPU, memory, and CI variables.
- Inline attachments: images as base64, JSON, XML, HTML, and plain text as fenced code blocks.
- Log helpers that append text lines to the current step.
- Configuration through Behave `userdata` options (`bmr.*`).
- Attachment and log helpers for `environment.py` (`attach_text`, `attach_json`, `attach_screenshot`, `attach_file`, `log`).
- Full unit test suite for models, collector, formatter, renderer, and Markdown builder.
- Functional Behave example project under `examples/behave_project/`.
- Demo generator under `examples/demo_generator/`.
- GitHub Actions CI workflow for linting, testing, and coverage.
- GitHub Actions Release workflow for automatic PyPI publishing and GitHub releases.
- Documentation: `docs/architecture.md`, `docs/configuration.md`, `docs/attachments.md`, `docs/ci-cd.md`, `docs/customizing.md`, `docs/usage.md`, `docs/examples.md`, and `docs/contributing.md`.
- Repository tooling: `Makefile`, `.editorconfig`, and `.pre-commit-config.yaml`.
