"""Validate skill directory structure."""
from __future__ import annotations

from pathlib import Path


def validate_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return [f"{skill_dir.name}: missing SKILL.md"]
    content = skill_md.read_text(encoding="utf-8", errors="replace")
    if not content.lstrip().startswith("# "):
        errors.append(f"{skill_dir.name}: SKILL.md must start with '# Title'")
    if "```" not in content:
        errors.append(f"{skill_dir.name}: SKILL.md must include at least one code example")
    return errors


def validate_tree(root: Path) -> list[str]:
    if not root.is_dir():
        return [f"skills root missing: {root}"]
    errors: list[str] = []
    for child in sorted(root.iterdir()):
        if child.is_dir() and not child.name.startswith("."):
            errors.extend(validate_skill(child))
    return errors
