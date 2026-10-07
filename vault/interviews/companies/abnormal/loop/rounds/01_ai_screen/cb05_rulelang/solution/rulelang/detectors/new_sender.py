"""An outside address emailing people it has never been in touch with."""
from __future__ import annotations

from rulelang.addresses import is_internal
from rulelang.detectors.base import Detector, DetectorContext, register_detector
from rulelang.models import Event, Severity, Signal


@register_detector
class NewSender(Detector):
    name = "new_sender"
    kinds = ("email",)

    def evaluate(self, event: Event, ctx: DetectorContext) -> Signal | None:
        if is_internal(event.actor, ctx.settings.org.internal_domains):
            return None
        for recipient in event.recipients:
            known = ctx.graph.first_contact(event.actor, recipient) or ctx.graph.first_contact(
                recipient, event.actor
            )
            if known:
                return None
        return self.signal(
            event,
            Severity.LOW,
            f"first contact from {event.actor}",
            sender=event.actor,
            recipients=list(event.recipients),
        )
