"""The Rule interface. Rules are pure functions of (event, enrichment, history)."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, ClassVar

from sentinel.config import Settings
from sentinel.db import EventRepository
from sentinel.models import RuleHit, SecurityEvent


@dataclass
class RuleContext:
    events: EventRepository


class Rule(ABC):
    id: ClassVar[str]
    title: ClassVar[str]

    def __init__(self, settings: Settings):
        self.settings = settings
        self.params: dict[str, Any] = settings.rules.get(self.id, {})

    def param(self, key: str, default: Any) -> Any:
        return self.params.get(key, default)

    @staticmethod
    def enrichment(event: SecurityEvent, name: str) -> dict[str, Any]:
        """Enrichment result for ``name``; empty when that enricher did not run or found nothing."""
        return event.enrichment.get(name) or {}

    @abstractmethod
    def evaluate(self, event: SecurityEvent, ctx: RuleContext) -> RuleHit | None:
        """Return a hit, or ``None`` when the rule does not fire."""


RULES: dict[str, type[Rule]] = {}


def register_rule(cls: type[Rule]) -> type[Rule]:
    """Class decorator: make a Rule available to the engine under ``cls.id``."""
    if cls.id in RULES:
        raise ValueError(f"duplicate rule id: {cls.id}")
    RULES[cls.id] = cls
    return cls


def rule_ids() -> list[str]:
    return sorted(RULES)


def rule_ids() -> list[str]:
    return sorted(RULES)
