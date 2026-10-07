"""In-process client for tests: no sockets, same code path as the WSGI app."""
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from vetting.api.app import App


@dataclass
class TestResponse:
    __test__ = False  # not a pytest class

    status: int
    body: Any

    def json(self) -> Any:
        return self.body


class TestClient:
    __test__ = False

    def __init__(self, app: App, token: str | None = None) -> None:
        self.app, self.token = app, token

    def request(self, method: str, path: str, params: dict[str, str] | None = None, body: Any = None) -> TestResponse:
        auth = f"Bearer {self.token}" if self.token else ""
        raw = json.dumps(body).encode() if body is not None else b""
        response = self.app.handle(method, path, dict(params or {}), auth, raw)
        return TestResponse(response.status, json.loads(json.dumps(response.body)))

    def get(self, path: str, **params: str) -> TestResponse:
        return self.request("GET", path, params)

    def post(self, path: str, json: Any = None) -> TestResponse:  # noqa: A002
        return self.request("POST", path, body=json if json is not None else {})

    def delete(self, path: str) -> TestResponse:
        return self.request("DELETE", path)
