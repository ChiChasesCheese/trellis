"""Links that point at hosts on the tenant-wide bad-host feed, or at punycode hosts."""
from __future__ import annotations

from rulelang.addresses import host_of
from rulelang.detectors.base import Detector, DetectorContext, register_detector
from rulelang.models import Event, Severity, Signal


@register_detector
class SuspiciousLink(Detector):
    name = "suspicious_link"
    kinds = ("email",)

    def evaluate(self, event: Event, ctx: DetectorContext) -> Signal | None:
        hosts = [host_of(u) for u in event.links]
        bad = sorted({h for h in hosts if h in ctx.intel.bad_hosts})
        if bad:
            return self.signal(event, Severity.HIGH, f"link to known bad host {bad[0]}", hosts=bad)
        puny = sorted({h for h in hosts if "xn--" in h})
        if puny:
            return self.signal(event, Severity.MEDIUM, f"punycode host {puny[0]}", hosts=puny)
        return None
