from vetting import normalize
from vetting.models import Finding, Kind
from vetting.signals.base import Signal, SignalContext, register_signal


@register_signal
class DisposableEmail(Signal):
    name = "disposable_email"

    def evaluate(self, ctx: SignalContext) -> Finding | None:
        for obs in ctx.of(Kind.EMAIL):
            domain = normalize.email_domain(obs.value)
            if domain and ctx.lookups.email.lookup(domain).disposable:
                return self.finding(ctx, f"Email uses a disposable-mail domain ({domain})", [obs], subject=f"domain:{domain}")
        return None
