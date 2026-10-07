"""One sender fanning out to many recipients, in one message or across many in a short window."""
from __future__ import annotations

from rulelang.detectors.base import Detector, DetectorContext, register_detector
from rulelang.models import Event, Severity, Signal
from rulelang.timeutil import window_start


@register_detector
class MassMailing(Detector):
    name = "mass_mailing"
    kinds = ("email",)

    def evaluate(self, event: Event, ctx: DetectorContext) -> Signal | None:
        fan_out = len(set(event.recipients))
        if fan_out >= self.param("recipient_threshold", 15):
            return self.signal(
                event, Severity.MEDIUM, f"{event.actor} sent one message to {fan_out} recipients", recipients=fan_out
            )
        window = self.param("window_minutes", 60)
        recent = ctx.events.count_emails_from(
            event.tenant_id, event.actor, window_start(event.ts, window), event.ts
        )
        if recent + 1 >= self.param("email_threshold", 30):
            return self.signal(
                event, Severity.MEDIUM, f"{event.actor} sent {recent + 1} messages in {window} min", messages=recent + 1
            )
        return None
