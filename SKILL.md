---
name: ppt-study-guide-skill
description: Convert slide presentations into checked study-guide Markdown and knowledge-index Markdown using safe extraction, structured drafting, and output-quality validation. Use when Codex needs to transform a user-provided .pptx into revision notes, a concept index, or review materials while identifying assumptions, excluding unlicensed source redistribution, and avoiding conversational or private-path leakage in deliverables.
---

# PPT Study Guide

将演示文稿转换为可检查的复习指南与知识索引。先提取源内容、再组织结构化文档，最后运行质量检查；不要把未经核实的生成内容表述为正确答案。

## 快速验证

在虚拟环境中对仓库自制示例执行完整流程：

```powershell
python scripts/generate_study_documents.py assets/demo-study-source.pptx --out-dir output/demo
python scripts/validate_outputs.py output/demo/study_guide.md output/demo/knowledge_index.md
```

预期输出：

- `study_guide.md`：按幻灯片章节整理的复习指南，显式收纳假设与待人工复核项。
- `knowledge_index.md`：按主题组织的索引与定位表。

需要查看已核验输出形态时，读取 [`references/demo-output/study_guide.md`](references/demo-output/study_guide.md) 与 [`references/demo-output/knowledge_index.md`](references/demo-output/knowledge_index.md)。

## 工作流

1. 确认公开与使用边界。
   - 判断输入 PPTX 是否由用户拥有或获准处理。
   - 若最终成果将公开，禁止复制发布未获授权的原始课件、题目全文、图片或生成答案集。
   - 读取 [`references/publishing-boundaries.md`](references/publishing-boundaries.md) 处理公开发布任务。
2. 提取内容。
   - 运行 `scripts/extract_pptx.py <input.pptx> --output <extract.md>` 获取可追溯的幻灯片文本提取稿。
   - 标记缺图、缺参数、公式识别不清或只能依赖上下文推断的位置。
3. 生成文档。
   - 对结构清楚的讲解型 PPT，可运行 `scripts/generate_study_documents.py <input.pptx> --out-dir <dir>` 生成基础稿。
   - 对需要解释、归纳或公式校对的内容，以基础稿为骨架人工审查和补写；将不确定内容写入“待人工复核与假设”，不得填造结论。
4. 检查输出。
   - 运行 `scripts/validate_outputs.py <study_guide.md> <knowledge_index.md>`。
   - 修正空输出、重复标题、对话式残留、本机路径泄露，以及未集中标记的假设/待复核内容。
5. 可选导出。
   - 仅在 Markdown 内容复核通过后导出 PDF。
   - PDF 只表示格式化交付物，不证明学科内容、解题答案或资料授权状态。

## 输出约定

| 输出 | 必须包含 | 禁止包含 |
| --- | --- | --- |
| `study_guide.md` | 文档标题、来源说明、章节内容、待人工复核与假设段落 | 对话开场、私有路径、无依据的答案正确性声明 |
| `knowledge_index.md` | 文档标题、主题定位表、复核提示 | 未经授权原件复制、隐私或设备标识 |

## 资源

- `assets/demo-study-source.pptx`：本仓库自制并可公开发布的演示输入，仅用于运行示例和测试。
- `scripts/extract_pptx.py`：将 PPTX 文本提取为可审查 Markdown。
- `scripts/generate_study_documents.py`：从结构化演示内容生成两份基础 Markdown 输出。
- `scripts/validate_outputs.py`：执行发布前的结构与敏感残留检查。
- `references/publishing-boundaries.md`：公开发布与人工复核边界。

## 责任边界

- 将 AI 和脚本用于提取、组织、格式检查和初稿生成。
- 由使用者负责验证专业内容、公式、版权许可和最终发布范围。
- 将缺图、缺参数或推断内容保留为待复核项，不将其包装为已验证答案。

