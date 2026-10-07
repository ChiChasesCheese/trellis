from __future__ import annotations

from typing import Any

from sentinel.api.framework import ApiContext, BadRequest, NotFound, Request, Response, route
from sentinel.rules import rule_ids
from sentinel.suppressions import SuppressionRepository, new_suppression
from sentinel.timeutil import utcnow

_SCALARS = (str, int, float, bool)


def _validate_match(raw: Any) -> dict[str, Any]:
    if raw is None:
        return {}
    if not isinstance(raw, dict):
        raise BadRequest("'match' must be an object of {field path: value}")
    for path, value in raw.items():
        values = value if isinstance(value, list) else [value]
        if not path or not values or not all(isinstance(v, _SCALARS) for v in values):
            raise BadRequest(f"invalid match condition for {path!r}")
    return raw


@route("POST", "/suppressions")
def create_suppression(req: Request, ctx: ApiContext) -> Response:
    body = req.json()
    rule_id = body.get("rule_id")
    if rule_id not in rule_ids():
        raise BadRequest("unknown or missing rule_id", details={"valid_rule_ids": rule_ids()})
    s = new_suppression(req.tenant, rule_id, _validate_match(body.get("match")), utcnow())
    SuppressionRepository(ctx.conn).add(s)
    return Response.ok(s.to_dict(), status=201)


@route("GET", "/suppressions")
def list_suppressions(req: Request, ctx: ApiContext) -> Response:
    items = SuppressionRepository(ctx.conn).list(req.tenant)
    return Response.ok({"items": [s.to_dict() for s in items], "total": len(items)})


@route("DELETE", "/suppressions/<suppression_id>")
def delete_suppression(req: Request, ctx: ApiContext) -> Response:
    if not SuppressionRepository(ctx.conn).delete(req.tenant, req.params["suppression_id"]):
        raise NotFound("suppression not found")
    return Response.no_content()
