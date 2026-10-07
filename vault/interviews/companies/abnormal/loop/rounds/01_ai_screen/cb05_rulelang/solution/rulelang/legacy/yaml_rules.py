"""DEPRECATED: the v0 rule format from the 2024 pilot. Half-finished, unused, and staying that way.

Nothing imports this module. Customers who wrote ``rules.yaml`` files were migrated by hand and the
format was dropped before ``and`` / ``or`` were ever implemented. Do not extend it and do not route
new features through it.

    name: young-domain
    when: sender_domain_age < 7
    then: flag
"""
from __future__ import annotations

import re
import warnings
from dataclasses import dataclass

warnings.warn("rulelang.legacy.yaml_rules is deprecated", DeprecationWarning, stacklevel=2)

_COMPARISON = re.compile(r"^(?P<field>[a-z_]+)\s*(?P<op><=|>=|<|>|==)\s*(?P<value>\S+)$")


@dataclass(frozen=True)
class YamlRule:
    name: str
    field: str
    op: str
    value: float | str


def parse_rule(text: str) -> YamlRule:
    """Parse one rule block. Only a single comparison is supported."""
    # TODO: boolean operators, parentheses, string quoting, error positions.
    lines = {k.strip(): v.strip() for k, _, v in (ln.partition(":") for ln in text.splitlines() if ":" in ln)}
    match = _COMPARISON.match(lines.get("when", ""))
    if match is None:
        raise ValueError(f"unsupported condition: {lines.get('when')!r}")
    raw = match["value"]
    value: float | str = float(raw) if re.fullmatch(r"-?\d+(\.\d+)?", raw) else raw
    return YamlRule(lines.get("name", "unnamed"), match["field"], match["op"], value)


def evaluate(rule: YamlRule, record: dict) -> bool:
    actual = record.get(rule.field)
    if actual is None:
        return False
    return {
        "<": lambda a, b: a < b,
        "<=": lambda a, b: a <= b,
        ">": lambda a, b: a > b,
        ">=": lambda a, b: a >= b,
        "==": lambda a, b: a == b,
    }[rule.op](actual, rule.value)
