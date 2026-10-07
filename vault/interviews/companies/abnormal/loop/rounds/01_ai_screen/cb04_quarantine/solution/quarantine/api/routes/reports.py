from __future__ import annotations

from quarantine.api.framework import ApiContext, BadRequest, Conflict, NotFound, Request, Response, route
from quarantine.errors import ValidationError
from quarantine.models import ReportStatus


@route("POST", "/reports")
def submit_report(req: Request, ctx: ApiContext) -> Response:
    """File a phishing report. 201 for a new message, 200 when the message was already reported."""
    try:
        result = ctx.intake.submit(req.tenant, req.json())
    except ValidationError as exc:
        raise BadRequest(str(exc)) from None
    return Response.ok(result.report.to_dict(), status=201 if result.created else 200)


@route("GET", "/reports")
def list_reports(req: Request, ctx: ApiContext) -> Response:
    limit = req.int_arg("limit", 50, minimum=1, maximum=200)
    offset = req.int_arg("offset", 0)
    items = ctx.reports.list(req.tenant, limit=limit, offset=offset)
    return Response.ok(
        {
            "items": [r.to_dict() for r in items],
            "total": ctx.reports.count(req.tenant),
            "limit": limit,
            "offset": offset,
        }
    )


@route("GET", "/reports/<report_id>")
def get_report(req: Request, ctx: ApiContext) -> Response:
    report = ctx.reports.get(req.tenant, req.params["report_id"])
    if report is None:
        raise NotFound("report not found")
    return Response.ok(report.to_dict())


@route("POST", "/reports/<report_id>/release")
def release_report(req: Request, ctx: ApiContext) -> Response:
    """An admin puts a quarantined message back. Releasing twice is fine and does nothing the second time."""
    report = ctx.reports.get(req.tenant, req.params["report_id"])
    if report is None:
        raise NotFound("report not found")
    if report.status is ReportStatus.CLEARED:
        raise Conflict("report was never quarantined")
    ctx.actions.release(report)
    return Response.ok(ctx.reports.get(req.tenant, report.id).to_dict())
