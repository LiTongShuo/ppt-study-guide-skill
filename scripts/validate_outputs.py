import argparse
from pathlib import Path
import re


DIALOGUE_MARKERS = ("好的，根据您的要求", "以下为您", "这里是为您", "为您整理")
REVIEW_MARKERS = ("假设", "待人工复核", "待确认", "需核对")
LOCAL_PATH_PATTERN = re.compile(r"(?:[A-Za-z]:\\|/Users/|/home/)")


def validate_document(path: Path, required_heading: str) -> list[str]:
    errors: list[str] = []
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    if not text.strip():
        return [f"{path.name}: output is empty or missing"]
    if required_heading not in text:
        errors.append(f"{path.name}: missing required heading {required_heading!r}")
    headings = [
        line.strip().casefold() for line in text.splitlines() if line.startswith("## ")
    ]
    duplicates = sorted({heading for heading in headings if headings.count(heading) > 1})
    if duplicates:
        errors.append(f"{path.name}: duplicate section heading(s): {', '.join(duplicates)}")
    for marker in DIALOGUE_MARKERS:
        if marker in text:
            errors.append(f"{path.name}: conversational residue found: {marker}")
    if LOCAL_PATH_PATTERN.search(text):
        errors.append(f"{path.name}: local filesystem path found")
    return errors


def validate_outputs(study_guide: Path, knowledge_index: Path) -> list[str]:
    errors = validate_document(study_guide, "# 复习指南")
    errors.extend(validate_document(knowledge_index, "# 知识索引"))
    study_text = study_guide.read_text(encoding="utf-8") if study_guide.exists() else ""
    index_text = knowledge_index.read_text(encoding="utf-8") if knowledge_index.exists() else ""
    if any(marker in study_text + index_text for marker in REVIEW_MARKERS):
        if "## 待人工复核与假设" not in study_text:
            errors.append("study_guide.md: identified review markers require a review section")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate generated study-document outputs.")
    parser.add_argument("study_guide", type=Path)
    parser.add_argument("knowledge_index", type=Path)
    args = parser.parse_args()
    errors = validate_outputs(args.study_guide, args.knowledge_index)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("Output validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
