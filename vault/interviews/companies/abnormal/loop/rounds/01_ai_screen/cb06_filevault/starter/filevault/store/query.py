"""A tiny parameterised WHERE builder. Values always travel as bound parameters."""
from __future__ import annotations

from collections.abc import Sequence
from typing import Any

COLUMNS = frozenset({"id", "owner", "filename", "content_type", "size", "created_at"})
OPERATORS = frozenset({"<", "<=", ">", ">=", "!="})


class Where:
    """Collects AND-ed conditions; ``build()`` returns ``(sql, params)``.

    Column names are checked against ``COLUMNS`` (they are identifiers, so they cannot be
    parameters); everything else is a ``?`` placeholder.
    """

    def __init__(self) -> None:
        self._clauses: list[str] = []
        self._params: list[Any] = []

    @staticmethod
    def _column(name: str) -> str:
        if name not in COLUMNS:
            raise ValueError(f"unknown column {name!r}")
        return name

    def eq(self, column: str, value: Any) -> "Where":
        self._clauses.append(f"{self._column(column)} = ?")
        self._params.append(value)
        return self

    def compare(self, column: str, op: str, value: Any) -> "Where":
        if op not in OPERATORS:
            raise ValueError(f"unsupported operator {op!r}")
        self._clauses.append(f"{self._column(column)} {op} ?")
        self._params.append(value)
        return self

    def row_compare(self, columns: Sequence[str], op: str, values: Sequence[Any]) -> "Where":
        """``(a, b) < (?, ?)``: lexicographic comparison, used for keyset pagination."""
        if op not in OPERATORS or len(columns) != len(values):
            raise ValueError("bad row comparison")
        names = ", ".join(self._column(c) for c in columns)
        marks = ", ".join("?" for _ in values)
        self._clauses.append(f"({names}) {op} ({marks})")
        self._params.extend(values)
        return self

    def build(self) -> tuple[str, tuple[Any, ...]]:
        if not self._clauses:
            return "", ()
        return "WHERE " + " AND ".join(self._clauses), tuple(self._params)
