"""Risk lookup with a read-through cache."""
from __future__ import annotations

import logging
import pickle
from datetime import datetime, timezone
from typing import Optional

from . import repo
from .cache import Cache
from .db import Database
from .scoring import compute_risk
from .settings import Settings

log = logging.getLogger(__name__)


class RiskService:
    def __init__(self, db: Database, cache: Cache, settings: Settings):
        self.db = db
        self.cache = cache
        self.settings = settings

    def get_risk(self, tenant_id: str, user_id: str) -> Optional[dict]:
        key = f"risk:{user_id}"
        cached = self.cache.get(key)
        if cached is not None:
            return pickle.loads(cached)

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
        self.cache.set(key, pickle.dumps(payload), self.settings.cache_ttl_s)
        log.info("risk lookup tenant=%s user=%s email=%s score=%s", tenant_id, user_id, user[2], result.score)
        return payload
