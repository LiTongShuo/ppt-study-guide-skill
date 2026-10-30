# PPT Study Guide Skill

English | [中文](README.zh-CN.md)

[![Validate PPT Study Guide Skill](https://github.com/LiTongShuo-edu/ppt-study-guide-skill/actions/workflows/validate.yml/badge.svg)](https://github.com/LiTongShuo-edu/ppt-study-guide-skill/actions/workflows/validate.yml)

`ppt-study-guide-skill` is an Agent Skill that converts `.pptx` presentations into structured Markdown. It extracts slide text, generates a study guide and knowledge index, and checks common structural and content hygiene issues before publication.

The repository includes a self-made presentation and its output. The examples are suitable for public use and do not depend on third-party course slides.

## Features

- Extract slide text organized by page.
- Generate `study_guide.md` and `knowledge_index.md` from titles and body text.
- Flag assumptions and material requiring human review.
- Check for empty output, duplicate sections, conversational residue, and local path leaks.
- Demonstrate the workflow with a self-made example and automated tests.

## Repository structure

| Path | Contents |
| --- | --- |
| [`SKILL.md`](./SKILL.md) | Workflow, input/output conventions, and limitations |
| [`assets/demo-study-source.pptx`](./assets/demo-study-source.pptx) | Self-made demo input |
| [`references/demo-output/`](./references/demo-output/) | Validated example output |
| [`references/publishing-boundaries.md`](./references/publishing-boundaries.md) | Source permissions and publication considerations |
| [`scripts/extract_pptx.py`](./scripts/extract_pptx.py) | Extract slide text |
| [`scripts/generate_study_documents.py`](./scripts/generate_study_documents.py) | Generate both Markdown documents |
| [`scripts/validate_outputs.py`](./scripts/validate_outputs.py) | Validate structure and sensitive residue |
| [`tests/`](./tests/) | Demo workflow and negative validation tests |

## Installation

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
# For tests and skill metadata validation:
.\.venv\Scripts\python.exe -m pip install -r requirements-test.txt
```

## Workflow

Extract the slide text:

```powershell
.\.venv\Scripts\python.exe scripts\extract_pptx.py .\assets\demo-study-source.pptx --output .\output\demo\source_extract.md
```

Generate the documents:

```powershell
.\.venv\Scripts\python.exe scripts\generate_study_documents.py .\assets\demo-study-source.pptx --out-dir .\output\demo
```

This produces `output/demo/study_guide.md`, organized by topic, and `output/demo/knowledge_index.md`, an index of topics and slide locations.

Validate the output:

```powershell
.\.venv\Scripts\python.exe scripts\validate_outputs.py .\output\demo\study_guide.md .\output\demo\knowledge_index.md
```

After validation, review and edit the Markdown manually as needed before exporting it.

## Demo and tests

```powershell
.\.venv\Scripts\python.exe scripts\generate_study_documents.py .\assets\demo-study-source.pptx --out-dir .\output\demo
.\.venv\Scripts\python.exe scripts\validate_outputs.py .\output\demo\study_guide.md .\output\demo\knowledge_index.md
.\.venv\Scripts\python.exe scripts\quick_validate.py .
.\.venv\Scripts\python.exe -m pytest
```

GitHub Actions creates a virtual environment on Windows and runs the same skill validation and tests.

## Limitations

- The scripts extract, organize, and check text; they do not verify subject matter or answers.
- Confirm usage and publication rights before processing real materials.
- Check flagged assumptions and items requiring review against the source and relevant knowledge.
- The repository does not contain unauthorized course slides, answers, images, or derivative documents.
