from vetting import normalize
from vetting.models import Finding, Kind
from vetting.signals.base import Signal, SignalContext, register_signal


@register_signal
class IpGeoMismatch(Signal):
    """The country the applicant claims differs from where their IP or sign-ins are."""

    name = "ip_geo_mismatch"

    def evaluate(self, ctx: SignalContext) -> Finding | None:
        claim = ctx.first(Kind.COUNTRY)
        claimed = normalize.country_code(claim.value) if claim else None
        if claim is None or claimed is None:
            return None
        mismatches, seen = [], []
        for obs in ctx.of(Kind.IP):
            country = normalize.country_code(ctx.lookups.ip.lookup(obs.value).country)
            if country and country != claimed:
                mismatches.append(obs)
                seen.append(country)
        for obs in ctx.of(Kind.LOGIN_COUNTRY):
            country = normalize.country_code(obs.value)
            if country and country != claimed:
                mismatches.append(obs)
                seen.append(country)
        if not mismatches:
            return None
        where = ", ".join(sorted(set(seen)))
        return self.finding(
            ctx, f"Applicant says {claimed}; IP geolocation / sign-ins say {where}", [claim, *mismatches]
        )
