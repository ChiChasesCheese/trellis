"""Customer rules run as ordinary detectors: same ``Signal`` shape, same runner, same storage."""
from __future__ import annotations

from rulelang.config import Settings
from rulelang.detectors.base import Detector, DetectorContext
from rulelang.models import Event, Severity, Signal
from rulelang.rules.compiler import CompiledRule
from rulelang.rules.fields import Scope


class CustomRuleDetector(Detector):
    kinds = ("email",)

    def __init__(self, settings: Settings, rule: CompiledRule):
        self.name = rule.name  # instance-level: one detector per customer rule
        self.rule = rule
        super().__init__(settings)

    def evaluate(self, event: Event, ctx: DetectorContext) -> Signal | None:
        scope = Scope(event, ctx.intel, ctx.settings.org.internal_domains)
        if not self.rule.matches(scope):
            return None
        return self.signal(event, Severity.MEDIUM, f"custom rule {self.name} matched", expression=self.rule.source)
