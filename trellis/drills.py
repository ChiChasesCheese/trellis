"""Drills: output practice attached to the same skeleton.

Cards recall knowledge, readings feed it in — drills train producing it:
a 40-minute design question, a coding exercise, a mock-interview scenario.
A drill lives under vault/<folder>/drills/, attaches to one or more nodes
(a real design question always spans several), and its body holds the
prompt, constraints, grading points, and your attempt log.

The file format is identical to readings (frontmatter: nodes, optional
title/url/tags), so the parser is shared.
"""

from __future__ import annotations

from pathlib import Path

from .readings import Reading as Drill, load_readings

__all__ = ["Drill", "load_drills"]


def load_drills(drills_dir: str | Path) -> tuple[list[Drill], list[str]]:
    return load_readings(drills_dir)
