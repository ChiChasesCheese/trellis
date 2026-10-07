"""The mini web framework: error types, Request/Response, and the ``@route`` registry.

One JSON error shape for the whole API: ``{"error": {"code", "message", "details"?}}``.
Handlers register themselves with ``@route`` (see ``quarantine/api/routes/``); importing a route
module is what registers it.
"""
from __future__ import annotations

import json
import re
import sqlite3
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any
from urllib.parse import parse_qs

from quarantine.actions import ActionService
from quarantine.config import SettingsProvider
from quarantine.intake import IntakeService
from quarantine.store import ReportRepository

# ---------------------------------------------------------------- errors


class ApiError(Exception):
    status = 500
    code = "internal_error"

    def __init__(self, message: str, details: dict[str, Any] | None = None):
        super().__init__(message)
        self.message = message
        self.details = details

    def to_body(self) -> dict[str, Any]:
        body: dict[str, Any] = {"code": self.code, "message": self.message}
        if self.details:
            body["details"] = self.details
        return {"error": body}


class BadRequest(ApiError):
    status = 400
    code = "bad_request"


class Unauthorized(ApiError):
    status = 401
    code = "unauthorized"


class NotFound(ApiError):
    status = 404
    code = "not_found"


class MethodNotAllowed(ApiError):
    status = 405
    code = "method_not_allowed"


class Conflict(ApiError):
    status = 409
    code = "conflict"


# ---------------------------------------------------------------- request / response


@dataclass
class Request:
    method: str
    path: str
    query: dict[str, list[str]] = field(default_factory=dict)
    headers: dict[str, str] = field(default_factory=dict)
    body: bytes = b""
    params: dict[str, str] = field(default_factory=dict)  # path parameters
    tenant: str = ""  # set by the auth middleware

    @classmethod
    def from_environ(cls, environ: dict[str, Any]) -> "Request":
        length = int(environ.get("CONTENT_LENGTH") or 0)
        headers = {
            k[5:].replace("_", "-").lower(): v for k, v in environ.items() if k.startswith("HTTP_")
        }
        return cls(
            method=environ["REQUEST_METHOD"].upper(),
            path=environ.get("PATH_INFO", "/"),
            query=parse_qs(environ.get("QUERY_STRING", "")),
            headers=headers,
            body=environ["wsgi.input"].read(length) if length else b"",
        )

    def arg(self, name: str, default: str | None = None) -> str | None:
        values = self.query.get(name)
        return values[0] if values else default

    def int_arg(self, name: str, default: int, minimum: int = 0, maximum: int = 1000) -> int:
        raw = self.arg(name)
        if raw is None:
            return default
        try:
            value = int(raw)
        except ValueError:
            raise BadRequest(f"query parameter {name!r} must be an integer") from None
        if not minimum <= value <= maximum:
            raise BadRequest(f"query parameter {name!r} must be between {minimum} and {maximum}")
        return value

    def json(self) -> dict[str, Any]:
        """The body as a JSON object; anything else is a 400."""
        try:
            data = json.loads(self.body or b"null")
        except json.JSONDecodeError:
            raise BadRequest("request body is not valid JSON") from None
        if not isinstance(data, dict):
            raise BadRequest("request body must be a JSON object")
        return data


@dataclass
class Response:
    status: int = 200
    body: Any = None
    headers: dict[str, str] = field(default_factory=dict)

    @classmethod
    def ok(cls, body: Any, status: int = 200) -> "Response":
        return cls(status=status, body=body)

    @classmethod
    def no_content(cls) -> "Response":
        return cls(status=204)

    def render(self) -> tuple[str, list[tuple[str, str]], bytes]:
        phrase = {200: "OK", 201: "Created", 204: "No Content"}.get(self.status, "Error")
        if self.body is None:
            return f"{self.status} {phrase}", list(self.headers.items()), b""
        payload = json.dumps(self.body, sort_keys=True).encode()
        headers = [("Content-Type", "application/json"), ("Content-Length", str(len(payload)))]
        return f"{self.status} {phrase}", headers + list(self.headers.items()), payload


# ---------------------------------------------------------------- routing


@dataclass
class ApiContext:
    """Dependencies handed to every route handler."""

    conn: sqlite3.Connection
    settings: SettingsProvider
    reports: ReportRepository
    intake: IntakeService
    actions: ActionService


Handler = Callable[[Request, ApiContext], Response]


@dataclass(frozen=True)
class Route:
    method: str
    pattern: re.Pattern[str]
    handler: Handler


ROUTES: list[Route] = []


def route(method: str, path: str) -> Callable[[Handler], Handler]:
    """Register ``handler`` for ``METHOD /path/<param>``."""
    regex = re.compile("^" + re.sub(r"<(\w+)>", r"(?P<\1>[^/]+)", path) + "$")

    def decorator(handler: Handler) -> Handler:
        ROUTES.append(Route(method.upper(), regex, handler))
        return handler

    return decorator


def resolve(method: str, path: str) -> tuple[Handler, dict[str, str]]:
    path_matched = False
    for r in ROUTES:
        m = r.pattern.match(path)
        if not m:
            continue
        path_matched = True
        if r.method == method:
            return r.handler, m.groupdict()
    if path_matched:
        raise MethodNotAllowed(f"{method} not allowed on {path}")
    raise NotFound(f"no route for {path}")
