from pathlib import Path
from x4_skills_hub.validate import validate_tree, validate_skill


def test_example_skill_valid():
    root = Path(__file__).resolve().parents[1] / "skills"
    errors = validate_tree(root)
    assert errors == []


def test_missing_skill_md(tmp_path):
    d = tmp_path / "broken"
    d.mkdir()
    errors = validate_skill(d)
    assert any("missing SKILL.md" in e for e in errors)
