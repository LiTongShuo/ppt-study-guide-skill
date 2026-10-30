# PPT Study Guide Skill

中文 | [English](README.en.md)

[![Validate PPT Study Guide Skill](https://github.com/LiTongShuo-edu/ppt-study-guide-skill/actions/workflows/validate.yml/badge.svg)](https://github.com/LiTongShuo-edu/ppt-study-guide-skill/actions/workflows/validate.yml)

`ppt-study-guide-skill` 是一个将 `.pptx` 演示文稿转换为结构化 Markdown 资料的 Agent Skill。它从幻灯片中提取文字，生成复习指南与知识索引，并在输出发布前检查常见的结构和内容卫生问题。

仓库内提供一份自制演示 PPT 与对应输出，所有示例材料均可公开使用，不依赖第三方课程课件。

## 功能

- 从 PPTX 文件中提取按页组织的文本内容。
- 根据标题与正文生成 `study_guide.md` 和 `knowledge_index.md`。
- 集中标记包含假设或需要人工复核的内容。
- 检查空输出、重复章节、对话式残留和本机路径泄露。
- 通过自制示例与自动测试展示完整处理流程。

## 目录结构

| 路径 | 内容 |
| --- | --- |
| [`SKILL.md`](./SKILL.md) | Skill 工作流、输入输出约定和使用边界 |
| [`assets/demo-study-source.pptx`](./assets/demo-study-source.pptx) | 自制的演示输入文件 |
| [`references/demo-output/`](./references/demo-output/) | 由演示输入生成并检查通过的示例输出 |
| [`references/publishing-boundaries.md`](./references/publishing-boundaries.md) | 来源授权与公开发布注意事项 |
| [`scripts/extract_pptx.py`](./scripts/extract_pptx.py) | 提取幻灯片文本 |
| [`scripts/generate_study_documents.py`](./scripts/generate_study_documents.py) | 生成两份 Markdown 文档 |
| [`scripts/validate_outputs.py`](./scripts/validate_outputs.py) | 校验输出结构与敏感残留 |
| [`tests/`](./tests/) | 示例流程和负面校验测试 |

## 安装

在 Python 3.12 虚拟环境中安装依赖：

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

若需要运行测试和 Skill 元数据校验，请安装测试依赖：

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-test.txt
```

## 使用流程

### 1. 提取幻灯片文本

```powershell
.\.venv\Scripts\python.exe scripts\extract_pptx.py .\assets\demo-study-source.pptx --output .\output\demo\source_extract.md
```

### 2. 生成结构化文档

```powershell
.\.venv\Scripts\python.exe scripts\generate_study_documents.py .\assets\demo-study-source.pptx --out-dir .\output\demo
```

输出文件：

- `output/demo/study_guide.md`：按主题整理的复习指南。
- `output/demo/knowledge_index.md`：主题与幻灯片位置索引。

### 3. 检查输出

```powershell
.\.venv\Scripts\python.exe scripts\validate_outputs.py .\output\demo\study_guide.md .\output\demo\knowledge_index.md
```

检查通过后，可进一步人工修订 Markdown，或在确认内容无误后导出为其他格式。

## 运行演示与测试

```powershell
.\.venv\Scripts\python.exe scripts\generate_study_documents.py .\assets\demo-study-source.pptx --out-dir .\output\demo
.\.venv\Scripts\python.exe scripts\validate_outputs.py .\output\demo\study_guide.md .\output\demo\knowledge_index.md
.\.venv\Scripts\python.exe scripts\quick_validate.py .
.\.venv\Scripts\python.exe -m pytest
```

GitHub Actions 会在 Windows 环境中新建虚拟环境，并运行相同的 Skill 校验与测试流程。

## 使用边界

- 脚本用于提取、组织和检查文本输出，不验证专业知识或题目答案的正确性。
- 处理真实材料时，应确认输入文件的使用与发布权限。
- 输出中被标为假设或待人工复核的内容，需要回到原始资料和相关知识进行确认。
- 仓库不包含未获授权的课程 PPT、习题答案、图片或派生文档。
