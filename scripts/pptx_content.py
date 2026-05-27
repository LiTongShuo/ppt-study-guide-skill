from dataclasses import dataclass
from pathlib import Path

from pptx import Presentation


@dataclass(frozen=True)
class SlideContent:
    number: int
    title: str
    lines: tuple[str, ...]


def read_slides(path: Path) -> list[SlideContent]:
    presentation = Presentation(str(path))
    slides: list[SlideContent] = []
    for number, slide in enumerate(presentation.slides, start=1):
        paragraphs: list[str] = []
        for shape in slide.shapes:
            if not shape.has_text_frame:
                continue
            for paragraph in shape.text_frame.paragraphs:
                text = paragraph.text.strip()
                if text:
                    paragraphs.append(text)
        if not paragraphs:
            continue
        slides.append(
            SlideContent(number=number, title=paragraphs[0], lines=tuple(paragraphs[1:]))
        )
    return slides

