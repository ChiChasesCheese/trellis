"""Unauthenticated liveness endpoint for load balancers."""
from __future__ import annotations

from filevault import __version__
from filevault.api.framework import ApiContext, Request, Response, route


@route("GET", "/health", public=True)
def health(req: Request, ctx: ApiContext) -> Response:
    return Response.ok({"status": "ok", "version": __version__})
