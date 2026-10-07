"""Detection rules. Importing this package registers every built-in rule."""
from __future__ import annotations

import logging

from sentinel import metrics
from sentinel.config import ConfigError, Settings
from sentinel.models import RuleHit, SecurityEvent
from sentinel.rules import (  # noqa: F401  (registration side effect)
    brute_force,
    impossible_travel,
    known_bad_ip,
    new_country_login,
    rare_admin_action,
)
from sentinel.rules.base import RULES, Rule, RuleContext, register_rule, rule_ids

log = logging.getLogger(__name__)


class RuleEngine:
    """Instantiates the enabled rules for one tenant and runs them over events."""

    def __init__(self, settings: Settings):
        unknown = set(settings.rules) - set(RULES)
        if unknown:
            raise ConfigError(f"config refers to unknown rules: {', '.join(sorted(unknown))}")
        self.rules: list[Rule] = [
            cls(settings)
            for rule_id, cls in sorted(RULES.items())
            if settings.rules.get(rule_id, {}).get("enabled", True)
        ]

    def evaluate(self, event: SecurityEvent, ctx: RuleContext) -> list[RuleHit]:
        hits: list[RuleHit] = []
        for rule in self.rules:
            try:
                hit = rule.evaluate(event, ctx)
            except Exception:  # one broken rule must not stop detection
                log.exception("rule %s failed on event %s", rule.id, event.id)
                metrics.incr("rules.error", rule=rule.id)
                continue
            if hit is not None:
                metrics.incr("rules.hit", rule=rule.id)
                hits.append(hit)
        return hits


__all__ = ["RULES", "Rule", "RuleContext", "RuleEngine", "register_rule", "rule_ids"]
