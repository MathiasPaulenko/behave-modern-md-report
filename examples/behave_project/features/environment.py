"""Environment hooks for the example Behave project."""

import base64
import json
import os

from behave_modern_md_report import attach_json, attach_screenshot, attach_text, log

# Minimal 1x1 red PNG to demonstrate image attachments in the report.
_RED_PIXEL_PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
)


def before_all(context):
    """Add custom BMR userdata and report options."""
    context.config.userdata["bmr.title"] = "Behave Project Example"
    context.config.userdata["bmr.company"] = "Open Source"


def before_scenario(_context, scenario):
    """Skip or mark pending scenarios based on tags for the demo."""
    if "skip" in scenario.tags:
        scenario.skip("Scenario tagged with @skip")
    elif "pending" in scenario.tags:
        scenario.skip("Scenario tagged with @pending")


def after_step(context, step):
    """Attach a failure log and screenshot when a step fails."""
    if step.status == "failed":
        log(context, f"Step failed: {step.name}")
        attach_text(
            context,
            f"Step failed: {step.name}\nStatus: {step.status}\nDuration: {step.duration:.3f}s",
            name="failure-log.txt",
        )
        attach_json(
            context,
            {
                "step": step.name,
                "status": step.status,
                "url": getattr(context, "page", {}).get("url", "unknown"),
            },
            name="failure-context.json",
        )
        # Attach a tiny red PNG as a fake screenshot so the report renders an image.
        attach_screenshot(context, _RED_PIXEL_PNG, name="failure-screenshot.png")


def after_all(_context):
    """Write a summary JSON sidecar for debugging."""
    summary = {
        "status": str(_context.failed),
    }
    path = os.path.join(os.path.dirname(__file__), "summary.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
