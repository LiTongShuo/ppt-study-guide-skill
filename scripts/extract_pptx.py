import argparse
from pathlib import Path

from pptx_content import read_slides


def extract_markdown(source: Path) -> str:
    slides = read_slides(source)
    lines = ["# 幻灯片文本提取", "", f"来源文件：`{source.name}`", ""]
    for slide in slides:
        lines.extend([f"## Slide {slide.number}: {slide.title}", ""])
        lines.extend([f"- {line}" for line in slide.lines] or ["- （无正文文本）"])
        lines.append("")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract reviewable text from a PPTX.")
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(extract_markdown(args.source), encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()

