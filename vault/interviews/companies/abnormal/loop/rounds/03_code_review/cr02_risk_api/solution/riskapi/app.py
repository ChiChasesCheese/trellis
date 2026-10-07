"""WSGI application: routing and handlers."""
from __future__ import annotations

import base64
import binascii
import json
import logging
import re
from typing import Optional
from urllib.parse import parse_qs

from . import repo
from .auth import Principal, authenticate
from .cache import Cache
from .db import Database
from .service import RiskService
from .settings import Settings

log = logging.getLogger(__name__)

RISK_RE = re.compile(r"^/tenants/([^/]+)/users/([^/]+)/risk$")
LIST_RE = re.compile(r"^/tenants/([^/]+)/users$")


class ApiError(Exception):
    def __init__(self, status: str, code: str, message: str):
        super().__init__(message)
        self.status, self.code, self.message = status, code, message


UNAUTHORIZED = ApiError("401 Unauthorized", "unauthorized", "missing or invalid API key")
NOT_FOUND = ApiError("404 Not Found", "not_found", "not found")


def encode_cursor(sort_value, user_id) -> str:
    return base64.urlsafe_b64encode(json.dumps([sort_value, user_id]).encode()).decode()


def decode_cursor(raw: str):
    try:
        value = json.loads(base64.urlsafe_b64decode(raw.encode()))
    except (ValueError, binascii.Error) as exc:
        raise ApiError("400 Bad Request", "invalid_cursor", "malformed cursor") from exc
    if not (isinstance(value, list) and len(value) == 2):
        raise ApiError("400 Bad Request", "invalid_cursor", "malformed cursor")
    return value


def parse_limit(raw: str, settings: Settings) -> int:
    try:
        limit = int(raw)
    except ValueError:
        limit = 0
    if not 1 <= limit <= settings.max_limit:
        raise ApiError("400 Bad Request", "invalid_limit", f"limit must be between 1 and {settings.max_limit}")
    return limit


def create_app(db: Database, cache: Optional[Cache] = None, settings: Optional[Settings] = None):
    settings = settings or Settings()
    cache = cache if cache is not None else Cache(max_entries=settings.cache_max_entries)
    service = RiskService(db, cache, settings)

    def authorize(environ, tenant: str) -> Principal:
        principal = authenticate(db, {"X-API-Key": environ.get("HTTP_X_API_KEY", "")})
        if principal is None:
            raise UNAUTHORIZED
        if principal.tenant_id != tenant:
            raise NOT_FOUND  # do not reveal which tenants exist
        return principal

    def get_risk(environ, tenant: str, user: str):
        authorize(environ, tenant)
        result = service.get_risk(tenant, user)
        if result is None:
            raise NOT_FOUND
        return "200 OK", result

    def list_users(environ, tenant: str):
        authorize(environ, tenant)
        qs = parse_qs(environ.get("QUERY_STRING", ""))
        sort = qs.get("sort", ["user_id"])[0]
        if sort not in repo.SORT_COLUMNS:
            raise ApiError("400 Bad Request", "invalid_sort", f"sort must be one of {sorted(repo.SORT_COLUMNS)}")
        cursor = decode_cursor(qs["cursor"][0]) if "cursor" in qs else None
        limit = parse_limit(qs.get("limit", [str(settings.default_limit)])[0], settings)
        rows = repo.list_users(db, tenant, sort, cursor, limit + 1)  # one extra row says whether a next page exists
        page = rows[:limit]
        items = [{"user_id": r[0], "name": r[1], "risk_score": r[2]} for r in page]
        next_cursor = encode_cursor(page[-1][3], page[-1][0]) if len(rows) > limit else None
        return "200 OK", {"items": items, "next_cursor": next_cursor}

    def route(environ):
        if environ.get("REQUEST_METHOD") != "GET":
            raise ApiError("405 Method Not Allowed", "method_not_allowed", "only GET is supported")
        path = environ.get("PATH_INFO", "")
        m = RISK_RE.match(path)
        if m:
            return get_risk(environ, *m.groups())
        m = LIST_RE.match(path)
        if m:
            return list_users(environ, m.group(1))
        raise ApiError("404 Not Found", "no_such_route", "no such route")

    def app(environ, start_response):
        try:
            status, body = route(environ)
        except ApiError as err:
            status, body = err.status, {"error": {"code": err.code, "message": err.message}}
        except Exception:
            log.exception("unhandled error")
            status, body = "500 Internal Server Error", {"error": {"code": "internal", "message": "internal error"}}
        data = json.dumps(body).encode()
        start_response(status, [("Content-Type", "application/json"), ("Content-Length", str(len(data)))])
        return [data]

    return app
