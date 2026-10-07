"""Usage and storage statistics."""
from __future__ import annotations

from filevault.api.framework import ApiContext, Forbidden, Request, Response, route


@route("GET", "/stats")
def my_stats(req: Request, ctx: ApiContext) -> Response:
    return Response.ok(ctx.service.usage(req.user))


@route("GET", "/admin/stats")
def admin_stats(req: Request, ctx: ApiContext) -> Response:
    if req.user not in ctx.settings.admin_users:
        raise Forbidden("admin only")
    return Response.ok(ctx.service.storage_stats())
