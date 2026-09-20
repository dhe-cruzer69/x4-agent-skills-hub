"""Score skills on quality/security dimensions (no star-as-quality)."""
from __future__ import annotations

from pathlib import Path


def _score_skill(skill_dir: Path) -> dict:
    skill_md = skill_dir / "SKILL.md"
    content = skill_md.read_text(encoding="utf-8", errors="replace") if skill_md.exists() else ""
    lines = content.count("\n") + 1
    has_example = "```" in content
    has_security_note = "security" in content.lower() or "permission" in content.lower()

    quality = min(100, 40 + (20 if has_example else 0) + min(40, lines // 5))
    security = 90 if has_security_note else 60
    documentation = min(100, 30 + min(70, lines // 3))
    maintenance = 80  # placeholder until git history is wired

    return {
        "name": skill_dir.name,
        "path": str(skill_dir),
        "quality": quality,
        "security": security,
        "documentation": documentation,
        "maintenance": maintenance,
        "compatibility": {"claude": True, "codex": True, "cursor": True},
        "verified": has_example and skill_md.exists(),
    }


def score_tree(root: Path) -> list[dict]:
    if not root.is_dir():
        return []
    return [
        _score_skill(child)
        for child in sorted(root.iterdir())
        if child.is_dir() and not child.name.startswith(".")
    ]
