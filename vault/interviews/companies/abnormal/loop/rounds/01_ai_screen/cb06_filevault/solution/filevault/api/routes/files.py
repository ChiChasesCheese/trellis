"""``/files`` endpoints. Uploads are JSON with the content base64-encoded (see README)."""
from __future__ import annotations

import base64
import binascii

from filevault.api.framework import (
    ApiContext,
    BadRequest,
    Request,
    Response,
    TooManyRequests,
    route,
)
from filevault.validation import parse_filters

FILTER_PARAMS = ("q", "type", "min_size", "max_size", "from", "to")


@route("POST", "/files")
def upload_file(req: Request, ctx: ApiContext) -> Response:
    retry_after = ctx.limiter.check(req.user)
    if retry_after is not None:
        raise TooManyRequests(
            "too many uploads, slow down", headers={"Retry-After": str(retry_after)}
        )
    body = req.json()
    filename, encoded = body.get("filename"), body.get("content_base64")
    if not isinstance(filename, str) or not isinstance(encoded, str):
        raise BadRequest("filename and content_base64 are required strings")
    content_type = body.get("content_type") or "application/octet-stream"
    if not isinstance(content_type, str):
        raise BadRequest("content_type must be a string")
    try:
        data = base64.b64decode(encoded, validate=True)
    except (binascii.Error, ValueError):
        raise BadRequest("content_base64 is not valid base64") from None
    record = ctx.service.upload(req.user, filename, content_type, data)
    return Response.ok(record.to_dict(), status=201)


@route("GET", "/files")
def list_files(req: Request, ctx: ApiContext) -> Response:
    limit = req.int_arg("limit", ctx.settings.default_page_size, 1, ctx.settings.max_page_size)
    filters = parse_filters({name: req.arg(name) for name in FILTER_PARAMS})
    records, next_cursor = ctx.service.list_files(req.user, req.arg("cursor"), limit, filters)
    return Response.ok({"items": [r.to_dict() for r in records], "next_cursor": next_cursor})


@route("GET", "/files/<file_id>")
def get_file(req: Request, ctx: ApiContext) -> Response:
    return Response.ok(ctx.service.get(req.user, req.params["file_id"]).to_dict())


@route("GET", "/files/<file_id>/content")
def get_content(req: Request, ctx: ApiContext) -> Response:
    record, data = ctx.service.read(req.user, req.params["file_id"])
    return Response(
        body=data,
        content_type=record.content_type,
        headers={"Content-Disposition": f'attachment; filename="{record.id}"'},
    )


@route("DELETE", "/files/<file_id>")
def delete_file(req: Request, ctx: ApiContext) -> Response:
    ctx.service.delete(req.user, req.params["file_id"])
    return Response.no_content()
