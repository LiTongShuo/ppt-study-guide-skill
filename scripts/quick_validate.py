import argparse
from pathlib import Path
import re
import sys

import yaml


NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def validate_skill(path: Path) -> list[str]:
    errors: list[str] = []
    skill_path = path / "SKILL.md"
    if not skill_path.exists():
        return ["SKILL.md is missing"]
    text = skill_path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        return ["SKILL.md must begin with YAML frontmatter"]
    parts = text.split("---\n", 2)
    if len(parts) < 3:
        return ["SKILL.md frontmatter is not closed"]
    metadata = yaml.safe_load(parts[1]) or {}
    allowed = {"name", "description"}
    extra = sorted(set(metadata) - allowed)
    if extra:
        errors.append(f"unsupported frontmatter field(s): {', '.join(extra)}")
    name = metadata.get("name", "")
    description = metadata.get("description", "")
    if not isinstance(name, str) or not NAME_PATTERN.fullmatch(name):
        errors.append("name must contain lowercase letters, numbers, and hyphens only")
    if name != path.name:
        errors.append("name must match the skill directory name")
    if not isinstance(description, str) or not description.strip():
        errors.append("description is required")
    if isinstance(description, str) and len(description) > 1024:
        errors.append("description must be 1024 characters or fewer")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a public Agent Skill folder.")
    parser.add_argument("skill_dir", type=Path)
    args = parser.parse_args()
    errors = validate_skill(args.skill_dir.resolve())
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("Skill is valid!")
    return 0


if __name__ == "__main__":
    sys.exit(main())
