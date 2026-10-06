"""A very small router: ``@route("GET", "/reviews/<identity_id>")`` registers a handler."""
from __future__ import annotations

import json
import re
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from vetting.api.errors import ApiError

if TYPE_CHECKING:
    from vetting.store import Store

Handler = Callable[["Request"], "Response"]
ROUTES: list["Route"] = []


@dataclass(frozen=True)
class Route:
    method: str
    pattern: re.Pattern[str]
    handler: Handler


def route(method: str, path: str) -> Callable[[Handler], Handler]:
    regex = re.compile("^" + re.sub(r"<(\w+)>", r"(?P<\1>[^/]+)", path) + "$")

    def register(handler: Handler) -> Handler:
        ROUTES.append(Route(method.upper(), regex, handler))
        return handler

    return register


@dataclass
class Request:
    method: str
    path: str
    query: dict[str, str]
    body: bytes
    tenant_id: str
    store: "Store"
    params: dict[str, str] = field(default_factory=dict)

    def json(self) -> dict[str, Any]:
        try:
            data = json.loads(self.body or b"{}")
        except json.JSONDecodeError:
            raise ApiError(400, "invalid_json", "request body is not valid JSON") from None
        if not isinstance(data, dict):
            raise ApiError(400, "invalid_json", "request body must be a JSON object")
        return data


@dataclass
class Response:
    status: int
    body: Any


def resolve(method: str, path: str) -> tuple[Route, dict[str, str]]:
    path_matched = False
    for candidate in ROUTES:
        match = candidate.pattern.match(path)
        if match is None:
            continue
        path_matched = True
        if candidate.method == method.upper():
            return candidate, match.groupdict()
    if path_matched:
        raise ApiError(405, "method_not_allowed", f"{method} not allowed for {path}")
    raise ApiError(404, "not_found", f"no route for {path}")
