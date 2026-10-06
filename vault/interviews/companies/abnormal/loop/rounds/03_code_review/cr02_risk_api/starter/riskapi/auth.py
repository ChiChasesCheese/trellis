"""API-key authentication. Keys look like `<key_id>.<secret>` and belong to one tenant."""
from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Mapping, Optional

from .db import Database


@dataclass(frozen=True)
class Principal:
    tenant_id: str
    key_id: str


def authenticate(db: Database, headers: Mapping[str, str]) -> Optional[Principal]:
    raw = headers.get("X-API-Key", "")
    key_id, _, secret = raw.partition(".")
    if not key_id or not secret:
        return None
    rows = db.query("SELECT tenant_id, key_md5 FROM api_keys WHERE key_id = ?", (key_id,))
    if not rows:
        return None
    tenant_id, stored = rows[0]
    if hashlib.md5(secret.encode()).hexdigest() == stored:
        return Principal(tenant_id=tenant_id, key_id=key_id)
    return None
