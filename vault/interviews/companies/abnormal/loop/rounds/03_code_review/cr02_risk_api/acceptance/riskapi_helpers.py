"""Builders for the risk-API acceptance tests. Only public entry points are used: create_app (WSGI),
Database / create_api_key / add_user / add_signal, Cache, RiskService through the HTTP routes."""
from __future__ import annotations

import io
import json
import threading
from urllib.parse import quote

from riskapi import db as dbmod
from riskapi.app import create_app
from riskapi.cache import Cache
from riskapi.db import Database

ACME_KEY = "k_acme.acme-secret-0001"
GLOBEX_KEY = "k_globex.globex-secret-0002"
FLAG: list[str] = []


def pwn():
    FLAG.append("code executed")


class Evil:
    """Unpickling this calls pwn(): what a poisoned cache entry could do."""

    def __reduce__(self):
        return (pwn, ())


class Client:
    def __init__(self, app):
        self.app = app

    def get(self, path, key=None, **query):
        qs = "&".join(f"{k}={quote(str(v), safe='')}" for k, v in query.items())
        environ = {"REQUEST_METHOD": "GET", "PATH_INFO": path, "QUERY_STRING": qs, "wsgi.input": io.BytesIO(b"")}
        if key:
            environ["HTTP_X_API_KEY"] = key
        out = {}

        def start_response(status, headers):
            out["status"] = int(status.split()[0])

        raw = b"".join(self.app(environ, start_response))
        return out["status"], json.loads(raw)


class World:
    def __init__(self, db_cls=Database, extra_acme_users=0, **app_kwargs):
        self.db = db_cls()
        db = self.db
        dbmod.create_api_key(db, "acme", "k_acme", "acme-secret-0001")
        dbmod.create_api_key(db, "globex", "k_globex", "globex-secret-0002")
        for i, name in enumerate(["Ann", "Bob", "Cy", "Di", "Eve"], start=1):
            dbmod.add_user(db, "acme", f"u{i}", f"{name.lower()}@acme.example.com", name, "eng", risk_score=(i * 7) % 5 * 10)
        for i in range(6, 6 + extra_acme_users):
            dbmod.add_user(db, "acme", f"u{i:04d}", f"user{i}@acme.example.com", f"User {i}", "eng", risk_score=i % 7)
        dbmod.add_user(db, "globex", "u1", "zed@globex.example.com", "Zed", "ops", risk_score=5)
        dbmod.add_signal(db, "acme", "u1", "mass_download", 40, "2026-10-01T10:00:00Z")
        dbmod.add_signal(db, "acme", "u1", "impossible_travel", 30, "2026-10-01T11:00:00Z")
        dbmod.add_signal(db, "globex", "u1", "off_hours_login", 10, "2026-10-01T03:00:00Z")
        self.cache = app_kwargs.pop("cache", None) or Cache()
        self.client = Client(create_app(db, self.cache, **app_kwargs))


def run_concurrently(n, fn):
    barrier = threading.Barrier(n)
    results = [None] * n

    def work(i):
        barrier.wait()
        results[i] = fn()

    threads = [threading.Thread(target=work, args=(i,)) for i in range(n)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(10)
    return results
