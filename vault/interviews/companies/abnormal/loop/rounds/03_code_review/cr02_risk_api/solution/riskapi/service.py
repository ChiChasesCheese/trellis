"""Risk lookup with a read-through cache (JSON values, single-flight per key)."""
from __future__ import annotations

import json
import logging
import threading
from datetime import datetime, timezone
from typing import Optional

from . import repo
from .cache import Cache
from .db import Database
from .scoring import compute_risk
from .settings import Settings

log = logging.getLogger(__name__)
_STRIPES = 64


class RiskService:
    def __init__(self, db: Database, cache: Cache, settings: Settings):
        self.db = db
        self.cache = cache
        self.settings = settings
        self._locks = [threading.Lock() for _ in range(_STRIPES)]  # striped: bounded memory

    @staticmethod
    def _key(tenant_id: str, user_id: str) -> str:
        return f"risk:{tenant_id}:{user_id}"

    def _cached(self, key: str) -> Optional[dict]:
        raw = self.cache.get(key)
        if raw is None:
            return None
        try:
            value = json.loads(raw)
        except ValueError:  # includes UnicodeDecodeError: a corrupt or foreign entry is just a miss
            log.warning("discarding unreadable cache entry %s", key)
            self.cache.delete(key)
            return None
        return value if isinstance(value, dict) else None

    def get_risk(self, tenant_id: str, user_id: str) -> Optional[dict]:
        key = self._key(tenant_id, user_id)
        hit = self._cached(key)
        if hit is not None:
            return hit
        with self._locks[hash(key) % _STRIPES]:  # single-flight: one loader per key, the rest wait
            hit = self._cached(key)
            if hit is not None:
                return hit
            user = repo.get_user(self.db, tenant_id, user_id)
            if user is None:
                return None
            result = compute_risk(repo.load_signals(self.db, tenant_id, user_id))
            payload = {
                "tenant_id": tenant_id,
                "user_id": user_id,
                "name": user[1],
                "score": result.score,
                "level": result.level,
                "factors": result.factors,
                "computed_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            }
            self.cache.set(key, json.dumps(payload).encode(), self.settings.cache_ttl_s)
            log.info("risk lookup tenant=%s user=%s score=%s", tenant_id, user_id, result.score)
            return payload
