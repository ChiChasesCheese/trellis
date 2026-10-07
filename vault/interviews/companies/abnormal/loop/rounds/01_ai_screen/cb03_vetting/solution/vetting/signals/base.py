from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar

from vetting.lookups import Lookups
from vetting.models import Citation, Finding, Identity, Kind, Observation
from vetting.settings import Settings

if TYPE_CHECKING:
    from vetting.store import Store

SIGNALS: dict[str, type["Signal"]] = {}


def register_signal(cls: type["Signal"]) -> type["Signal"]:
    """Class decorator. The signal's weight must exist in config/default.toml."""
    if cls.name in SIGNALS:
        raise ValueError(f"duplicate signal name {cls.name!r}")
    SIGNALS[cls.name] = cls
    return cls


def all_signals() -> list["Signal"]:
    return [SIGNALS[name]() for name in sorted(SIGNALS)]


@dataclass(frozen=True)
class SignalContext:
    """Everything a signal may look at for one identity."""

    identity: Identity
    observations: list[Observation]
    lookups: Lookups
    settings: Settings
    store: "Store"

    def of(self, kind: Kind) -> list[Observation]:
        return [obs for obs in self.observations if obs.kind == kind]

    def first(self, kind: Kind) -> Observation | None:
        found = self.of(kind)
        return found[0] if found else None


class Signal(ABC):
    name: ClassVar[str]

    @abstractmethod
    def evaluate(self, ctx: SignalContext) -> Finding | None:
        """Return a finding when the signal fires, else None. Must not write anything."""

    def finding(
        self, ctx: SignalContext, summary: str, evidence: list[Observation], subject: str = ""
    ) -> Finding:
        return Finding(
            signal=self.name,
            weight=ctx.settings.weight(self.name),
            summary=summary,
            evidence=tuple(Citation.of(obs) for obs in evidence),
            subject=subject,
        )
