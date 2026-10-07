from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass
class Settings:
    db_path: str = "riskapi.db"
    host: str = "127.0.0.1"
    port: int = 8080
    # --- risk endpoint / caching ---
    cache_ttl_s: int = 300
    default_limit: int = 50
    max_limit: int = 200
    cache_max_entries: int = 10_000

    @classmethod
    def from_env(cls) -> "Settings":
        s = cls()
        s.db_path = os.environ.get("RISKAPI_DB", s.db_path)
        s.port = int(os.environ.get("RISKAPI_PORT", s.port))
        s.cache_ttl_s = int(os.environ.get("RISKAPI_CACHE_TTL", s.cache_ttl_s))
        return s
