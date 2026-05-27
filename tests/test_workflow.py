import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "assets" / "demo-study-source.pptx"


def test_demo_workflow_generates_checked_outputs(tmp_path):
    command = [
        sys.executable,
        str(ROOT / "scripts" / "generate_study_documents.py"),
        str(SAMPLE),
        "--out-dir",
        str(tmp_path),
    ]
    subprocess.run(command, check=True)
    subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts" / "validate_outputs.py"),
            str(tmp_path / "study_guide.md"),
            str(tmp_path / "knowledge_index.md"),
        ],
        check=True,
    )
    guide = (tmp_path / "study_guide.md").read_text(encoding="utf-8")
    assert "## 待人工复核与假设" in guide
    assert "传感器信号处理基础" in guide
    assert "SELF-AUTHORED DEMO" not in guide
    assert "\n- OK\n" not in guide
    assert "\n- 01\n" not in guide


def test_validator_rejects_dialogue_and_local_paths(tmp_path):
    study = tmp_path / "study_guide.md"
    index = tmp_path / "knowledge_index.md"
    study.write_text("# 复习指南\n\n## 待人工复核与假设\n\n以下为您 C:\\private\\file\n", encoding="utf-8")
    index.write_text("# 知识索引\n", encoding="utf-8")
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "validate_outputs.py"), str(study), str(index)],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1
    assert "conversational residue" in result.stdout
    assert "local filesystem path" in result.stdout
