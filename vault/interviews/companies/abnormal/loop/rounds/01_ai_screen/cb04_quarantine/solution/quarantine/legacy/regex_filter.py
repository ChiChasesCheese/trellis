"""DEPRECATED (v1). Subject-line regex filter, replaced by the analyzers in 0.3.

Frozen: nothing imports this module any more and it must not be extended. Kept for reference
until the last on-prem customer has migrated.
"""
from __future__ import annotations

import re

SUBJECT_PATTERNS = [
    re.compile(r"verify your account", re.I),
    re.compile(r"password (will )?expire", re.I),
    re.compile(r"urgent.*wire transfer", re.I),
    re.compile(r"\binvoice\b.*\battached\b", re.I),
]


def legacy_match(subject: str) -> bool:
    """True when the subject looks like phishing by the old rules."""
    return any(p.search(subject) for p in SUBJECT_PATTERNS)


def legacy_filter(reports: list[dict]) -> list[dict]:
    return [r for r in reports if legacy_match(r.get("subject", ""))]
