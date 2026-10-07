from vetting import normalize
from vetting.lookups import LineType
from vetting.models import Finding, Kind
from vetting.signals.base import Signal, SignalContext, register_signal


@register_signal
class VoipPhone(Signal):
    name = "voip_phone"

    def evaluate(self, ctx: SignalContext) -> Finding | None:
        for obs in ctx.of(Kind.PHONE):
            e164 = normalize.phone_e164(obs.value)
            if e164 is None:
                continue
            info = ctx.lookups.phone.lookup(e164)
            if info.line_type is LineType.VOIP:
                carrier = f" ({info.carrier})" if info.carrier else ""
                return self.finding(
                    ctx, f"Phone number resolves to a VoIP line{carrier}", [obs], subject=f"phone:{e164}"
                )
        return None
