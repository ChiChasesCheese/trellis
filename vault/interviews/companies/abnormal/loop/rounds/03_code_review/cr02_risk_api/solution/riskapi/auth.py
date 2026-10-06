"""API-key authentication. Keys look like `<key_id>.<secret>` and belong to one tenant."""
from __future__ import annotations

import hmac
from dataclasses import dataclass
from typing import Mapping, Optional

from .db import Database, hash_secret

_DUMMY = hash_secret("no-such-key")


@dataclass(frozen=True)
class Principal:
    tenant_id: str
    key_id: str


def authenticate(db: Database, headers: Mapping[str, str]) -> Optional[Principal]:
    raw = headers.get("X-API-Key", "")
    key_id, _, secret = raw.partition(".")
    if not key_id or not secret:
        return None
    rows = db.query("SELECT tenant_id, key_hash FROM api_keys WHERE key_id = ?", (key_id,))
    tenant_id, stored = rows[0] if rows else ("", _DUMMY)  # always do exactly one comparison
    ok = hmac.compare_digest(hash_secret(secret), stored)
    return Principal(tenant_id=tenant_id, key_id=key_id) if ok and rows else None
