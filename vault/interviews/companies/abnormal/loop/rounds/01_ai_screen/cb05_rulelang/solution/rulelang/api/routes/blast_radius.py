"""``GET /blast-radius?account=<addr>&since=<ISO timestamp>``."""
from __future__ import annotations

from rulelang.api.framework import ApiContext, BadRequest, Request, Response, route
from rulelang.graph import CommGraph, blast_radius
from rulelang.timeutil import iso, parse_ts


@route("GET", "/blast-radius")
def get_blast_radius(req: Request, ctx: ApiContext) -> Response:
    account, raw_since = req.arg("account"), req.arg("since")
    if not account or not raw_since:
        raise BadRequest("query parameters 'account' and 'since' are required")
    try:
        since = parse_ts(raw_since)
    except ValueError:
        raise BadRequest("query parameter 'since' must be an ISO-8601 timestamp") from None
    settings = ctx.settings.for_tenant(req.tenant)
    exposures = blast_radius(
        CommGraph(ctx.conn, req.tenant),
        account,
        since,
        settings.blast_radius.max_hops,
        settings.org.internal_domains,
    )
    return Response.ok(
        {
            "account": account.strip().lower(),
            "since": iso(since),
            "max_hops": settings.blast_radius.max_hops,
            "items": [e.to_dict() for e in exposures],
            "total": len(exposures),
        }
    )
