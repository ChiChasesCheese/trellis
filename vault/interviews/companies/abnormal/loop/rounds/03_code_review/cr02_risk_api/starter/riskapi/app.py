"""WSGI application: routing and handlers."""
from __future__ import annotations

import base64
import json
import logging
import re
from typing import Optional
from urllib.parse import parse_qs

from . import repo
from .auth import authenticate
from .cache import Cache
from .db import Database
from .service import RiskService
from .settings import Settings

log = logging.getLogger(__name__)

RISK_RE = re.compile(r"^/tenants/([^/]+)/users/([^/]+)/risk$")
LIST_RE = re.compile(r"^/tenants/([^/]+)/users$")


def encode_cursor(sort_value, user_id) -> str:
    return base64.urlsafe_b64encode(json.dumps([sort_value, user_id]).encode()).decode()


def decode_cursor(raw: str):
    return json.loads(base64.urlsafe_b64decode(raw.encode()))


def create_app(db: Database, cache: Optional[Cache] = None, settings: Optional[Settings] = None):
    settings = settings or Settings()
    cache = cache if cache is not None else Cache()
    service = RiskService(db, cache, settings)

    def route(environ):
        path = environ.get("PATH_INFO", "")
        qs = parse_qs(environ.get("QUERY_STRING", ""))
        headers = {"X-API-Key": environ.get("HTTP_X_API_KEY", "")}
        if environ.get("REQUEST_METHOD") != "GET":
            return "405 Method Not Allowed", {"error": "method not allowed"}

        m = RISK_RE.match(path)
        if m:
            tenant, user = m.groups()
            principal = authenticate(db, headers)
            if principal is None:
                return "401 Unauthorized", {"error": "unauthorized"}
            result = service.get_risk(tenant, user)
            if result is None:
                return "404 Not Found", {"message": "user not found"}
            return "200 OK", result

        m = LIST_RE.match(path)
        if m:
            tenant = m.group(1)
            principal = authenticate(db, headers)
            if principal is None:
                return "401 Unauthorized", {"error": "unauthorized"}
            sort = qs.get("sort", ["user_id"])[0]
            cursor = decode_cursor(qs["cursor"][0]) if "cursor" in qs else None
            limit = int(qs.get("limit", [settings.default_limit])[0])
            rows = repo.list_users(db, tenant, sort, cursor, limit)
            items = [{"user_id": r[0], "name": r[1], "risk_score": r[2]} for r in rows]
            next_cursor = encode_cursor(rows[-1][3], rows[-1][0]) if len(rows) == limit else None
            return "200 OK", {"items": items, "next_cursor": next_cursor}

        return "404 Not Found", {"error": "no such route"}

    def app(environ, start_response):
        try:
            status, body = route(environ)
        except Exception as exc:
            log.exception("unhandled error")
            status, body = "500 Internal Server Error", {"error": str(exc)}
        data = json.dumps(body).encode()
        start_response(status, [("Content-Type", "application/json"), ("Content-Length", str(len(data)))])
        return [data]

    return app
