"""In-process client for tests: drives the WSGI app without opening a socket."""
from __future__ import annotations

import io
import json
from dataclasses import dataclass, field
from typing import Any
from urllib.parse import urlencode


@dataclass
class TestResponse:
    __test__ = False  # not a pytest test class

    status_code: int
    body: bytes
    headers: dict[str, str] = field(default_factory=dict)

    @property
    def json(self) -> Any:
        return json.loads(self.body) if self.body else None


class TestClient:
    __test__ = False

    def __init__(self, app: Any, user: str | None = None):
        self.app = app
        self.user = user

    def request(
        self, method: str, path: str, json_body: Any = None, params: dict[str, Any] | None = None
    ) -> TestResponse:
        payload = json.dumps(json_body).encode() if json_body is not None else b""
        environ = {
            "REQUEST_METHOD": method,
            "PATH_INFO": path,
            "QUERY_STRING": urlencode(params or {}),
            "CONTENT_LENGTH": str(len(payload)),
            "wsgi.input": io.BytesIO(payload),
        }
        if self.user:
            environ["HTTP_X_USER_ID"] = self.user
        captured: dict[str, Any] = {}

        def start_response(status: str, headers: list[tuple[str, str]]) -> None:
            captured["status"] = int(status.split()[0])
            captured["headers"] = {k: v for k, v in headers}

        body = b"".join(self.app(environ, start_response))
        return TestResponse(captured["status"], body, captured["headers"])

    def get(self, path: str, params: dict[str, Any] | None = None) -> TestResponse:
        return self.request("GET", path, params=params)

    def post(self, path: str, json_body: Any = None) -> TestResponse:
        return self.request("POST", path, json_body=json_body)

    def delete(self, path: str) -> TestResponse:
        return self.request("DELETE", path)
