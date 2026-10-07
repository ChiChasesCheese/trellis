"""The WSGI application: ``X-User-Id`` -> route -> JSON, with one error shape."""
from __future__ import annotations

import logging
import re
from collections.abc import Callable, Iterable
from typing import Any

from filevault.api import routes  # noqa: F401  (importing registers the handlers)
from filevault.api.framework import (
    ApiContext,
    ApiError,
    BadRequest,
    NotFound,
    PayloadTooLarge,
    Request,
    Response,
    Unauthorized,
    resolve,
)
from filevault.errors import BlobNotFound, FileNotFound, FileTooLarge, FileVaultError, InvalidInput

log = logging.getLogger(__name__)

USER_ID = re.compile(r"^[A-Za-z0-9_.@-]{1,64}$")


def translate(exc: FileVaultError) -> ApiError | None:
    """Map a domain error onto the API error it should surface as (``None`` = unexpected)."""
    if isinstance(exc, InvalidInput):
        return BadRequest(str(exc), {"field": exc.field})
    if isinstance(exc, (FileNotFound, BlobNotFound)):
        return NotFound("file not found")
    if isinstance(exc, FileTooLarge):
        return PayloadTooLarge(str(exc), {"limit": exc.limit})
    return None


class ApiApp:
    def __init__(self, ctx: ApiContext):
        self.ctx = ctx

    def authenticate(self, request: Request) -> str:
        user = request.headers.get("x-user-id", "")
        if not user:
            raise Unauthorized("missing X-User-Id header")
        if not USER_ID.match(user):
            raise Unauthorized("invalid X-User-Id header")
        return user

    def handle(self, request: Request) -> Response:
        try:
            matched, params = resolve(request.method, request.path)
            if not matched.public:
                request.user = self.authenticate(request)
            request.params = params
            return matched.handler(request, self.ctx)
        except ApiError as exc:
            return Response(status=exc.status, body=exc.to_body(), headers=exc.headers)
        except FileVaultError as exc:
            mapped = translate(exc)
            if mapped is None:
                log.exception("unhandled domain error on %s %s", request.method, request.path)
                return self._internal_error()
            return Response(status=mapped.status, body=mapped.to_body(), headers=mapped.headers)
        except Exception:
            log.exception("unhandled error on %s %s", request.method, request.path)
            return self._internal_error()

    @staticmethod
    def _internal_error() -> Response:
        return Response(
            status=500, body={"error": {"code": "internal_error", "message": "internal error"}}
        )

    def __call__(
        self, environ: dict[str, Any], start_response: Callable[..., Any]
    ) -> Iterable[bytes]:
        response = self.handle(Request.from_environ(environ))
        status, headers, payload = response.render()
        start_response(status, headers)
        return [payload]
