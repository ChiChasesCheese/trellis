"""A first-time sender whose domain imitates one of the tenant's real vendors."""
from __future__ import annotations

from rulelang.detectors.base import Detector, DetectorContext, register_detector
from rulelang.models import Event, Severity, Signal

_CONFUSABLE = str.maketrans({"0": "o", "1": "l", "5": "s"})


def _edit_distance(a: str, b: str) -> int:
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def looks_like(domain: str, vendor: str) -> bool:
    return domain != vendor and (
        domain.translate(_CONFUSABLE) == vendor or _edit_distance(domain, vendor) == 1
    )


@register_detector
class VendorLookalike(Detector):
    name = "vendor_lookalike"
    kinds = ("email",)
    requires = ("new_sender",)

    def evaluate(self, event: Event, ctx: DetectorContext) -> Signal | None:
        # A known contact is not an impersonation attempt: only first contacts are checked.
        if "new_sender" not in ctx.signals:
            return None
        for vendor in ctx.intel.vendors:
            if looks_like(event.actor_domain, vendor):
                return self.signal(
                    event,
                    Severity.HIGH,
                    f"{event.actor_domain} imitates vendor {vendor}",
                    vendor=vendor,
                    sender_domain=event.actor_domain,
                )
        return None
