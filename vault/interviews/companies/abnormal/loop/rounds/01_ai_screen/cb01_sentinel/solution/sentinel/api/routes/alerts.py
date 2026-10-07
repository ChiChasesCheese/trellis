from __future__ import annotations

from sentinel.alerts import AlertStatus
from sentinel.api.framework import ApiContext, BadRequest, Conflict, NotFound, Request, Response, route


@route("GET", "/alerts")
def list_alerts(req: Request, ctx: ApiContext) -> Response:
    """Alerts for the caller's tenant, highest score first."""
    status = None
    if (raw := req.arg("status")) is not None:
        try:
            status = AlertStatus(raw.upper())
        except ValueError:
            raise BadRequest(f"unknown status {raw!r}") from None
    limit = req.int_arg("limit", 50, minimum=1, maximum=200)
    offset = req.int_arg("offset", 0)
    items = ctx.alerts.list(req.tenant, status=status, limit=limit, offset=offset)
    return Response.ok(
        {
            "items": [a.to_dict() for a in items],
            "total": ctx.alerts.count(req.tenant, status),
            "limit": limit,
            "offset": offset,
        }
    )


@route("GET", "/alerts/<alert_id>")
def get_alert(req: Request, ctx: ApiContext) -> Response:
    alert = ctx.alerts.get(req.tenant, req.params["alert_id"])
    if alert is None:
        raise NotFound("alert not found")
    return Response.ok(alert.to_dict())


@route("POST", "/alerts/<alert_id>/ack")
def ack_alert(req: Request, ctx: ApiContext) -> Response:
    alert = ctx.alerts.get(req.tenant, req.params["alert_id"])
    if alert is None:
        raise NotFound("alert not found")
    if alert.status is AlertStatus.CLOSED:
        raise Conflict("alert is closed")
    ctx.alerts.set_status(req.tenant, alert.id, AlertStatus.ACKED)
    return Response.ok(ctx.alerts.get(req.tenant, alert.id).to_dict())


@route("GET", "/events/<event_id>")
def get_event(req: Request, ctx: ApiContext) -> Response:
    event = ctx.events.get(req.tenant, req.params["event_id"])
    if event is None:
        raise NotFound("event not found")
    return Response.ok(event.to_dict())
