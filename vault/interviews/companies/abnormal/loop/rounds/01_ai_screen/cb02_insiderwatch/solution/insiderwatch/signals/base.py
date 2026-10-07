"""Signal base class and registry.

A signal looks at one user's events for one UTC day (plus baselines and HR data) and returns
zero or more findings. `strength` is 0..1; scoring turns it into a risk score using the
signal's configured weight.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Any, Callable, ClassVar, Iterable, Sequence

from ..baselines import BaselineStore
from ..config import Config
from ..errors import InsiderWatchError
from ..events import Event
from ..hr import Roster


@dataclass(frozen=True)
class Finding:
    signal: str
    user: str
    ts: datetime
    strength: float
    reasons: tuple[str, ...]
    evidence: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class SignalContext:
    day: date
    baselines: BaselineStore
    roster: Roster
    config: Config


class Signal(ABC):
    name: ClassVar[str]

    @abstractmethod
    def evaluate(self, ctx: SignalContext, user: str, events: Sequence[Event]) -> Iterable[Finding]:
        """`events` are this user's events on `ctx.day`, in time order."""


_REGISTRY: dict[str, type[Signal]] = {}


def signal(name: str) -> Callable[[type[Signal]], type[Signal]]:
    """Class decorator: register a Signal under `name`."""

    def decorate(cls: type[Signal]) -> type[Signal]:
        if name in _REGISTRY:
            raise InsiderWatchError(f"duplicate signal {name!r}")
        cls.name = name
        _REGISTRY[name] = cls
        return cls

    return decorate


def all_signals() -> list[Signal]:
    return [cls() for cls in _REGISTRY.values()]


def signal_names() -> list[str]:
    return list(_REGISTRY)
