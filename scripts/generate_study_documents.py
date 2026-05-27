import argparse
from pathlib import Path
import re

from pptx_content import SlideContent, read_slides


REVIEW_MARKERS = ("待人工复核", "假设", "待确认", "需核对")
DECORATIVE_LINES = {"OK", "SELF-AUTHORED DEMO"}


def _section_title(slide: SlideContent) -> str:
    return re.sub(r"^\d+[.、]\s*", "", slide.title).strip()


def _content_lines(slide: SlideContent) -> list[str]:
    return [
        line
        for line in slide.lines
        if line.strip() not in DECORATIVE_LINES
        and not re.fullmatch(r"\d{1,3}", line.strip())
    ]


def _requires_review(line: str) -> bool:
    return any(line.strip().startswith(f"{marker}：") for marker in REVIEW_MARKERS)


def build_study_guide(source: Path, slides: list[SlideContent]) -> str:
    content_slides = slides[1:] if len(slides) > 1 else slides
    review_lines: list[str] = []
    parts = [
        "# 复习指南：传感器信号处理基础",
        "",
        f"来源说明：由自制演示文件 `{source.name}` 生成，仅用于演示文档转换流程。",
        "",
    ]
    for slide in content_slides:
        title = _section_title(slide)
        parts.extend([f"## {title}", ""])
        for line in _content_lines(slide):
            parts.append(f"- {line}")
            if _requires_review(line):
                review_lines.append(f"{title}：{line}")
        parts.append("")
    parts.extend(["## 待人工复核与假设", ""])
    if review_lines:
        parts.extend(f"- {line}" for line in review_lines)
    else:
        parts.append("- 本示例未识别到待复核内容；处理真实材料时仍需人工核对。")
    parts.extend(
        [
            "",
            "## 使用提示",
            "",
            "- 先通过索引定位主题，再回到原始演示内容复核上下文。",
            "- 本文档展示整理流程，不构成设备参数或学科结论验证。",
            "",
        ]
    )
    return "\n".join(parts)


def build_knowledge_index(source: Path, slides: list[SlideContent]) -> str:
    content_slides = slides[1:] if len(slides) > 1 else slides
    rows = [
        "# 知识索引：传感器信号处理基础",
        "",
        f"来源说明：索引来自自制演示文件 `{source.name}`。",
        "",
        "| 主题 | 对应页 | 重点定位 |",
        "| --- | --- | --- |",
    ]
    for slide in content_slides:
        lines = _content_lines(slide)
        summary = lines[0] if lines else "查看原页内容"
        rows.append(f"| {_section_title(slide)} | Slide {slide.number} | {summary} |")
    rows.extend(
        [
            "",
            "## 复核提示",
            "",
            "- 标有“待人工复核”或“假设”的内容应回到实验约束或原始资料核实。",
            "- 本索引提供导航，不替代内容正确性检查。",
            "",
        ]
    )
    return "\n".join(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate baseline study documents from a PPTX.")
    parser.add_argument("source", type=Path)
    parser.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args()
    slides = read_slides(args.source)
    if not slides:
        raise SystemExit("No text-bearing slides were found.")
    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "study_guide.md").write_text(
        build_study_guide(args.source, slides), encoding="utf-8"
    )
    (args.out_dir / "knowledge_index.md").write_text(
        build_knowledge_index(args.source, slides), encoding="utf-8"
    )
    print(args.out_dir)


if __name__ == "__main__":
    main()
