"""``GET /signals`` and ``GET /signals?event_id=``."""
from __future__ import annotations

from rulelang.api.framework import ApiContext, NotFound, Request, Response, route


@route("GET", "/signals")
def list_signals(req: Request, ctx: ApiContext) -> Response:
    event_id = req.arg("event_id")
    if event_id:
        if ctx.events.get(req.tenant, event_id) is None:
            raise NotFound(f"no event {event_id!r}")
        found = ctx.signals.for_event(req.tenant, event_id)
    else:
        found = ctx.signals.list(req.tenant, limit=req.int_arg("limit", 50, minimum=1))
    items = [s.to_dict() for s in found]
    return Response.ok({"items": items, "total": len(items)})
