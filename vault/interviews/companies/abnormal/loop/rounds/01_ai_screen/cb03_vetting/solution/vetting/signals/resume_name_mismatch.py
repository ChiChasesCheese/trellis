from vetting import normalize
from vetting.models import Finding, Kind
from vetting.signals.base import Signal, SignalContext, register_signal


@register_signal
class ResumeNameMismatch(Signal):
    name = "resume_name_mismatch"

    def evaluate(self, ctx: SignalContext) -> Finding | None:
        applied, resume = ctx.first(Kind.NAME), ctx.first(Kind.RESUME_NAME)
        if applied is None or resume is None:
            return None
        if normalize.name_key(applied.value) == normalize.name_key(resume.value):
            return None
        return self.finding(
            ctx,
            f"Name in resume ({resume.value}) differs from application name ({applied.value})",
            [applied, resume],
        )
