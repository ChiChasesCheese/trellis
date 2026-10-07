"""DEPRECATED: the v1 static rule DSL, kept only so the 2025 customer exports still load.

Nothing in the pipeline imports this module any more; detections are ``sentinel.rules``
classes now. Do not extend it and do not route new features through it.

A rule file is one rule per line:   deny if country == RU
                                    deny if user == root@acme.test
"""
from __future__ import annotations

import warnings
from dataclasses import dataclass

warnings.warn("sentinel.legacy.static_rules is deprecated", DeprecationWarning, stacklevel=2)


@dataclass(frozen=True)
class StaticRule:
    field: str
    value: str


def parse(text: str) -> list[StaticRule]:
    rules = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.split()
        if len(parts) != 5 or parts[:2] != ["deny", "if"] or parts[3] != "==":
            raise ValueError(f"bad legacy rule: {line!r}")
        rules.append(StaticRule(field=parts[2], value=parts[4]))
    return rules


def matches(rules: list[StaticRule], event: dict) -> list[StaticRule]:
    return [r for r in rules if str(event.get(r.field)) == r.value]
