"""Behave Markdown Report.

The modern, readable, CI/CD-friendly Markdown report formatter for Behave.

Public API:
    BehaveMarkdownFormatter -- the Behave entry point.
    MarkdownRenderer        -- standalone renderer (Behave-independent).
    Collector               -- builds an execution model from formatter events.
    models                  -- dataclasses representing the execution tree.
    attach_file             -- attach a file to the current step.
    attach_text             -- attach a text snippet to the current step.
    attach_json             -- attach JSON data to the current step.
    attach_screenshot       -- attach a screenshot to the current step.
    log                     -- append a log line to the current step.
"""

from __future__ import annotations

from .attach import (
    attach_file,
    attach_json,
    attach_screenshot,
    attach_text,
    log,
)
from .collector import Collector
from .formatter import BehaveMarkdownFormatter
from .renderer import MarkdownRenderer, RenderOptions

__all__ = [
    "BehaveMarkdownFormatter",
    "MarkdownRenderer",
    "RenderOptions",
    "Collector",
    "attach_file",
    "attach_text",
    "attach_json",
    "attach_screenshot",
    "log",
    "__version__",
]

__version__ = "1.0.0"
