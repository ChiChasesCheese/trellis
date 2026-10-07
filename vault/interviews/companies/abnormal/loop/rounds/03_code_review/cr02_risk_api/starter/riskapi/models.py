"""Typed row shapes used by tooling and tests."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class UserRow:
    tenant_id: str
    user_id: str
    email: str
    name: str
    department: str
    risk_score: int

    @classmethod
    def from_row(cls, row: tuple) -> "UserRow":
        return cls(*row)
