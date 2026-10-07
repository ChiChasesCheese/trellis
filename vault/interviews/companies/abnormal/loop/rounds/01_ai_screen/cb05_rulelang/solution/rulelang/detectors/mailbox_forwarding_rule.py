"""A mailbox rule that forwards mail outside the organisation."""
from __future__ import annotations

from rulelang.addresses import is_internal
from rulelang.detectors.base import Detector, DetectorContext, register_detector
from rulelang.models import Event, Severity, Signal


@register_detector
class MailboxForwardingRule(Detector):
    name = "mailbox_forwarding_rule"
    kinds = ("mailbox_rule_created",)

    def evaluate(self, event: Event, ctx: DetectorContext) -> Signal | None:
        target = event.attrs.get("forward_to", "")
        if not target or is_internal(target, ctx.settings.org.internal_domains):
            return None
        return self.signal(
            event,
            Severity.HIGH,
            f"{event.actor} forwards mail to external address {target}",
            rule_name=event.attrs.get("rule_name", ""),
            forward_to=target,
        )
