"""HR roster: who works here, who they report to, and when they are leaving."""
from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterator

from ..errors import RosterError
from ..events import normalize_user


@dataclass(frozen=True)
class Employee:
    email: str
    name: str
    department: str
    manager: str | None = None
    timezone: str = "UTC"
    termination_date: date | None = None  # last day of employment, if known
    resignation_submitted: date | None = None  # day the employee gave notice, if they did


def _opt_date(value: str | None) -> date | None:
    return date.fromisoformat(value) if value else None


class Roster:
    def __init__(self, employees: list[Employee]) -> None:
        self._by_email = {e.email: e for e in employees}

    @classmethod
    def load(cls, path: str | Path) -> "Roster":
        try:
            data = json.loads(Path(path).read_text())
            employees = [
                Employee(
                    email=normalize_user(item["email"]),
                    name=item["name"],
                    department=item.get("department", ""),
                    manager=normalize_user(item["manager"]) if item.get("manager") else None,
                    timezone=item.get("timezone", "UTC"),
                    termination_date=_opt_date(item.get("termination_date")),
                    resignation_submitted=_opt_date(item.get("resignation_submitted")),
                )
                for item in data["employees"]
            ]
        except (OSError, KeyError, ValueError) as exc:
            raise RosterError(f"cannot load roster {path}: {exc}") from exc
        return cls(employees)

    @classmethod
    def empty(cls) -> "Roster":
        return cls([])

    def get(self, user: str) -> Employee | None:
        return self._by_email.get(normalize_user(user))

    def __contains__(self, user: str) -> bool:
        return self.get(user) is not None

    def __iter__(self) -> Iterator[Employee]:
        return iter(self._by_email.values())

    def timezone_for(self, user: str, default: str = "UTC") -> str:
        emp = self.get(user)
        return emp.timezone if emp else default
