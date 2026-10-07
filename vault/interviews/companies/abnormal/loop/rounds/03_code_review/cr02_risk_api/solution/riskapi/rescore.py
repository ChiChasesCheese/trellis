"""Nightly job: recompute the denormalised `users.risk_score` from raw signals.

Run as `python -m riskapi.rescore`. The API serves detailed scores live (see service.py); this job
only keeps the sortable summary column fresh.
"""
from __future__ import annotations

import logging
from typing import Optional

from .db import Database
from .scoring import compute_risk
from .settings import Settings

log = logging.getLogger(__name__)


def rescore_tenant(db: Database, tenant_id: str) -> int:
    """Recompute every user's score in one tenant; returns the number of rows that changed."""
    changed = 0
    users = db.query("SELECT user_id, risk_score FROM users WHERE tenant_id = ?", (tenant_id,))
    for user_id, old in users:
        signals = db.query(
            "SELECT kind, weight, observed_at FROM signals WHERE tenant_id = ? AND user_id = ?",
            (tenant_id, user_id),
        )
        new = compute_risk(signals).score
        if new != old:
            db.execute(
                "UPDATE users SET risk_score = ? WHERE tenant_id = ? AND user_id = ?",
                (new, tenant_id, user_id),
            )
            changed += 1
    return changed


def rescore_all(db: Database, only: Optional[str] = None) -> dict[str, int]:
    tenants = [r[0] for r in db.query("SELECT DISTINCT tenant_id FROM users ORDER BY tenant_id")]
    out = {}
    for t in tenants:
        if only and t != only:
            continue
        out[t] = rescore_tenant(db, t)
        log.info("rescored tenant=%s changed=%d", t, out[t])
    return out


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    print(rescore_all(Database(Settings.from_env().db_path)))


if __name__ == "__main__":
    main()
