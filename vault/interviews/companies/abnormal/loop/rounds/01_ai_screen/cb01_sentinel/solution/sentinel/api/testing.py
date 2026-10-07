"""In-process client for tests: drives the WSGI app without opening a socket."""
from __future__ import annotations

import io
import json
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlencode


@dataclass
class TestResponse:
    __test__ = False  # not a pytest test class

    status_code: int
    body: bytes

    @property
    def json(self) -> Any:
        return json.loads(self.body) if self.body else None


class TestClient:
    __test__ = False

    def __init__(self, app: Any, token: str | None = None):
        self.app = app
        self.token = token

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
        if self.token:
            environ["HTTP_AUTHORIZATION"] = f"Bearer {self.token}"
        captured: dict[str, Any] = {}

        def start_response(status: str, headers: list[tuple[str, str]]) -> None:
            captured["status"] = int(status.split()[0])

        body = b"".join(self.app(environ, start_response))
        return TestResponse(status_code=captured["status"], body=body)

    def get(self, path: str, params: dict[str, Any] | None = None) -> TestResponse:
        return self.request("GET", path, params=params)

    def post(self, path: str, json_body: Any = None) -> TestResponse:
        return self.request("POST", path, json_body=json_body)

    def delete(self, path: str) -> TestResponse:
        return self.request("DELETE", path)
