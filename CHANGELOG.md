# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-06-29

### Added

- Initial release of `behave-modern-md-report`.
- Behave formatter producing a single Markdown file.
- Executive summary, statistics, feature summary, and scenario details.
- Collapsible scenario details using HTML `<details>` tags.
- Failed scenarios section with error messages and tracebacks.
- Slowest scenarios top 10 list.
- Environment section with Python, Behave, OS, and CI variables.
- Support for tags, data tables, doc strings, and attachments.
- Image attachments rendered as inline base64 images.
- Text, JSON, XML, and HTML attachments rendered as fenced code blocks.
- Configuration through Behave `userdata` options.
- Attachment and log helpers for `environment.py`.
- Unit tests and example Behave project.
