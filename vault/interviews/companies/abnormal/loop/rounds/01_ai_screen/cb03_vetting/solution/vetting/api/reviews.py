"""Review endpoints: list (with tier filter), detail with evidence timeline, reviewer disposition."""
from __future__ import annotations

from vetting.api.errors import ApiError
from vetting.api.router import Request, Response, route
from vetting.models import DECISIONS, Disposition, Recommendation, Review
from vetting.timeline import build_timeline
from vetting.timeutil import to_iso, utcnow


def _summary(request: Request, review: Review) -> dict:
    identity = request.store.identities.get(request.tenant_id, review.identity_id)
    return {
        "identity_id": review.identity_id,
        "display_name": identity.display_name if identity else "",
        "source": identity.source if identity else "",
        "recommendation": review.recommendation.value,
        "score": review.score,
        "finding_count": len(review.findings),
    }


@route("GET", "/reviews")
def list_reviews(request: Request) -> Response:
    raw = request.query.get("recommendation")
    wanted = None
    if raw is not None:
        try:
            wanted = Recommendation(raw.upper())
        except ValueError:
            raise ApiError(400, "invalid_filter", f"recommendation must be one of {[r.value for r in Recommendation]}") from None
    reviews = request.store.reviews.list(request.tenant_id, wanted)
    return Response(200, {"count": len(reviews), "items": [_summary(request, r) for r in reviews]})


@route("GET", "/reviews/<identity_id>")
def get_review(request: Request) -> Response:
    tenant, identity_id = request.tenant_id, request.params["identity_id"]
    identity = request.store.identities.get(tenant, identity_id)
    review = request.store.reviews.get(tenant, identity_id)
    if identity is None or review is None:
        raise ApiError(404, "not_found", f"no review for {identity_id}")
    observations = request.store.observations.for_identity(tenant, identity_id)
    history = request.store.reviews.dispositions(tenant, identity_id)
    return Response(
        200,
        {
            **_summary(request, review),
            "applied_at": to_iso(identity.applied_at),
            "findings": [f.to_dict() for f in review.findings],
            "timeline": [e.to_dict() for e in build_timeline(identity, observations, review.findings)],
            "disposition": history[-1].decision if history else None,
            "dispositions": [
                {"decision": d.decision, "note": d.note, "decided_at": to_iso(d.decided_at)} for d in history
            ],
        },
    )


@route("POST", "/reviews/<identity_id>/disposition")
def post_disposition(request: Request) -> Response:
    tenant, identity_id = request.tenant_id, request.params["identity_id"]
    if request.store.identities.get(tenant, identity_id) is None:
        raise ApiError(404, "not_found", f"no review for {identity_id}")
    body = request.json()
    decision = body.get("decision")
    if decision not in DECISIONS:
        raise ApiError(400, "invalid_decision", f"decision must be one of {list(DECISIONS)}")
    note = body.get("note", "")
    if not isinstance(note, str):
        raise ApiError(400, "invalid_note", "note must be a string")
    when = utcnow()
    request.store.reviews.add_disposition(tenant, Disposition(identity_id, decision, note, when))
    return Response(201, {"identity_id": identity_id, "decision": decision, "note": note, "decided_at": to_iso(when)})
