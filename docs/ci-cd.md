# CI/CD integration

The Markdown report is designed to fit naturally into CI/CD pipelines. It is a single plain-text file that can be archived, uploaded as an artifact, or pasted into CI summaries.

## GitHub Actions

### Basic workflow

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -e ".[dev]"
      - run: behave -f behave_modern_md_report.formatter:BehaveMarkdownFormatter -o report.md
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: behave-report
          path: report.md
```

### Post to a GitHub Actions job summary

```yaml
      - run: behave -f behave_modern_md_report.formatter:BehaveMarkdownFormatter -o report.md
      - run: cat report.md >> "$GITHUB_STEP_SUMMARY"
        if: always()
```

GitHub renders the Markdown directly in the workflow summary page.

### Post to a pull request comment

Use an action such as `peter-evans/create-or-update-comment` to post the report as a comment. Because the report can be long, consider uploading it as an artifact and posting only the executive summary in the comment body.

## GitLab CI

```yaml
test:
  image: python:3.12
  script:
    - pip install -e ".[dev]"
    - behave -f behave_modern_md_report.formatter:BehaveMarkdownFormatter -o report.md
  artifacts:
    when: always
    paths:
      - report.md
```

GitLab renders the Markdown in the job artifacts and can expose it via the merge request widget.

## Azure DevOps

```yaml
steps:
  - script: |
      pip install -e ".[dev]"
      behave -f behave_modern_md_report.formatter:BehaveMarkdownFormatter -o report.md
    displayName: Run Behave tests
  - task: PublishBuildArtifacts@1
    inputs:
      PathtoPublish: report.md
      ArtifactName: behave-report
    condition: always()
```

Azure DevOps can render Markdown artifacts in the build summary.

## Jenkins

Archive the report as an artifact:

```groovy
post {
    always {
        archiveArtifacts artifacts: 'report.md', allowEmptyArchive: true
    }
}
```

Use the HTML Publisher plugin or a Markdown viewer plugin to display the report in the build page.

## Best practices

* **Always archive the report** even when tests fail (`if: always()` in GitHub Actions, `when: always` in GitLab).
* **Keep the report in the workspace** for the shortest path to failure investigation.
* **Use `bmr.include_environment = true`** in CI to capture Python version, OS, and environment variables.
* **For large suites**, set `bmr.max_traceback_lines` to a reasonable number to keep the report readable.
* **Publish the report as a job summary** when the platform supports it; this avoids downloading artifacts for quick checks.
