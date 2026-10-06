"""SQL for the endpoints."""
from __future__ import annotations

from typing import Optional

from .db import Database


def get_user(db: Database, tenant_id: str, user_id: str) -> Optional[tuple]:
    rows = db.query(
        "SELECT user_id, name, email, department FROM users WHERE tenant_id = ? AND user_id = ?",
        (tenant_id, user_id),
    )
    return rows[0] if rows else None


def load_signals(db: Database, tenant_id: str, user_id: str) -> list[tuple[str, int, str]]:
    return db.query(
        "SELECT kind, weight, observed_at FROM signals WHERE tenant_id = ? AND user_id = ? ORDER BY observed_at",
        (tenant_id, user_id),
    )


def list_users(db: Database, tenant_id: str, sort: str, cursor, limit: int) -> list[tuple]:
    """Keyset pagination ordered by (`sort`, user_id). Returns (user_id, name, risk_score, sort_value)."""
    sql = f"SELECT user_id, name, risk_score, {sort} FROM users WHERE tenant_id = ?"
    params: list = [tenant_id]
    if cursor:
        sort_value, last_id = cursor
        sql += f" AND ({sort}, user_id) >= (?, ?)"
        params += [sort_value, last_id]
    sql += f" ORDER BY {sort}, user_id LIMIT ?"
    params.append(limit)
    return db.query(sql, params)
