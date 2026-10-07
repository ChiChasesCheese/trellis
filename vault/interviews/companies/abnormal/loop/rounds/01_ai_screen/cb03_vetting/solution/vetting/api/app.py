"""WSGI application: Bearer token -> tenant, route, JSON in / JSON out, one error shape."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl
from wsgiref.simple_server import make_server

from vetting.api import reviews  # noqa: F401  (import registers the routes)
from vetting.api.errors import ApiError, from_exception
from vetting.api.router import Request, Response, resolve
from vetting.errors import VettingError
from vetting.settings import DEFAULT_DB, DEFAULT_TOKENS
from vetting.store import Store

_STATUS = {200: "200 OK", 201: "201 Created", 400: "400 Bad Request", 401: "401 Unauthorized",
           404: "404 Not Found", 405: "405 Method Not Allowed", 500: "500 Internal Server Error"}


def load_tokens(path: Path) -> dict[str, str]:
    return json.loads(path.read_text())


class App:
    def __init__(self, db_path: str | Path, tokens: dict[str, str]) -> None:
        self.db_path = db_path
        self.tokens = tokens

    def authenticate(self, authorization: str) -> str:
        scheme, _, token = authorization.partition(" ")
        tenant = self.tokens.get(token.strip()) if scheme.lower() == "bearer" else None
        if tenant is None:
            raise ApiError(401, "unauthorized", "missing or invalid bearer token")
        return tenant

    def handle(self, method: str, path: str, query: dict[str, str], authorization: str, body: bytes) -> Response:
        try:
            tenant = self.authenticate(authorization)
            matched, params = resolve(method, path)
            store = Store.open(self.db_path)
            try:
                request = Request(method, path, query, body, tenant, store, params)
                response = matched.handler(request)
                store.conn.commit()
                return response
            finally:
                store.close()
        except ApiError as exc:
            return Response(exc.status, exc.body())
        except VettingError as exc:
            error = from_exception(exc)
            return Response(error.status, error.body())

    def __call__(self, environ: dict[str, Any], start_response):
        length = int(environ.get("CONTENT_LENGTH") or 0)
        body = environ["wsgi.input"].read(length) if length else b""
        query = dict(parse_qsl(environ.get("QUERY_STRING", "")))
        response = self.handle(
            environ["REQUEST_METHOD"], environ["PATH_INFO"], query, environ.get("HTTP_AUTHORIZATION", ""), body
        )
        payload = json.dumps(response.body).encode()
        start_response(
            _STATUS.get(response.status, f"{response.status} Status"),
            [("Content-Type", "application/json"), ("Content-Length", str(len(payload)))],
        )
        return [payload]


def create_app(db_path: str | Path = DEFAULT_DB, tokens_path: Path = DEFAULT_TOKENS) -> App:
    return App(db_path, load_tokens(tokens_path))


def serve(app: App, host: str, port: int) -> None:
    with make_server(host, port, app) as server:
        print(f"serving on http://{host}:{port}")
        server.serve_forever()
