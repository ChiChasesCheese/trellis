"""The WSGI application: bearer-token auth -> route -> JSON, with one error shape."""
from __future__ import annotations

import hmac
import json
import logging
from collections.abc import Callable, Iterable
from pathlib import Path
from typing import Any

from sentinel.api import routes  # noqa: F401  (importing registers the handlers)
from sentinel.api.framework import ApiContext, ApiError, Request, Response, Unauthorized, resolve

log = logging.getLogger(__name__)


class TokenStore:
    def __init__(self, path: Path):
        self._tokens: dict[str, str] = json.loads(Path(path).read_text())

    def tenant_for(self, authorization: str | None) -> str:
        if not authorization or not authorization.startswith("Bearer "):
            raise Unauthorized("missing bearer token")
        presented = authorization[len("Bearer ") :].strip()
        for token, tenant in self._tokens.items():
            if hmac.compare_digest(token, presented):
                return tenant
        raise Unauthorized("invalid token")


class ApiApp:
    def __init__(self, ctx: ApiContext, tokens: TokenStore):
        self.ctx = ctx
        self.tokens = tokens

    def handle(self, request: Request) -> Response:
        try:
            request.tenant = self.tokens.tenant_for(request.headers.get("authorization"))
            handler, params = resolve(request.method, request.path)
            request.params = params
            return handler(request, self.ctx)
        except ApiError as exc:
            return Response(status=exc.status, body=exc.to_body())
        except Exception:
            log.exception("unhandled error on %s %s", request.method, request.path)
            return Response(
                status=500,
                body={"error": {"code": "internal_error", "message": "internal error"}},
            )

    def __call__(
        self, environ: dict[str, Any], start_response: Callable[..., Any]
    ) -> Iterable[bytes]:
        response = self.handle(Request.from_environ(environ))
        status, headers, payload = response.render()
        start_response(status, headers)
        return [payload]
