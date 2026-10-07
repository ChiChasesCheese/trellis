import io
import json

import pytest

from riskapi import db as dbmod
from riskapi.app import create_app
from riskapi.cache import Cache
from riskapi.db import Database

ACME_KEY = "k_acme.acme-secret-0001"
GLOBEX_KEY = "k_globex.globex-secret-0002"


class Client:
    def __init__(self, app):
        self.app = app

    def get(self, path, key=None, query=""):
        environ = {
            "REQUEST_METHOD": "GET",
            "PATH_INFO": path,
            "QUERY_STRING": query,
            "wsgi.input": io.BytesIO(b""),
        }
        if key:
            environ["HTTP_X_API_KEY"] = key
        out = {}

        def start_response(status, headers):
            out["status"] = int(status.split()[0])

        body = b"".join(self.app(environ, start_response))
        return out["status"], json.loads(body)


@pytest.fixture
def world():
    db = Database()
    dbmod.create_api_key(db, "acme", "k_acme", "acme-secret-0001")
    dbmod.create_api_key(db, "globex", "k_globex", "globex-secret-0002")
    for i, name in enumerate(["Ann", "Bob", "Cy", "Di", "Eve"], start=1):
        dbmod.add_user(db, "acme", f"u{i}", f"{name.lower()}@acme.example.com", name, "eng", risk_score=i * 10)
    dbmod.add_user(db, "globex", "u1", "zed@globex.example.com", "Zed", "ops", risk_score=5)
    dbmod.add_signal(db, "acme", "u1", "mass_download", 40, "2026-10-01T10:00:00Z")
    dbmod.add_signal(db, "acme", "u1", "impossible_travel", 30, "2026-10-01T11:00:00Z")
    dbmod.add_signal(db, "globex", "u1", "off_hours_login", 10, "2026-10-01T03:00:00Z")
    cache = Cache()
    return db, cache, Client(create_app(db, cache))
