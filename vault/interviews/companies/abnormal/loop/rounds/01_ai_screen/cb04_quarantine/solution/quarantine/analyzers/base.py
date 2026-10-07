"""The Analyzer interface, its registry, and the context every analyzer receives."""
from __future__ import annotations

from dataclasses import dataclass

from quarantine.config import Settings, SettingsProvider
from quarantine.lookups import SenderIntel, UrlLookup
from quarantine.models import Report, Verdict
from quarantine.store import ReportRepository


@dataclass
class AnalysisContext:
    """Everything an analyzer may touch. Analyzers do not open files or sockets themselves."""

    settings: SettingsProvider
    reports: ReportRepository
    url_lookup: UrlLookup
    sender_intel: SenderIntel

    def tenant(self, report: Report) -> Settings:
        """The report's tenant settings."""
        return self.settings.for_tenant(report.tenant_id)


class Analyzer:
    """One signal. Subclasses set ``name`` and implement ``analyze``."""

    name: str = ""

    def analyze(self, report: Report, ctx: AnalysisContext) -> Verdict:  # pragma: no cover
        raise NotImplementedError


ANALYZERS: dict[str, type[Analyzer]] = {}


def register_analyzer(cls: type[Analyzer]) -> type[Analyzer]:
    if not cls.name:
        raise ValueError(f"{cls.__name__} has no name")
    if cls.name in ANALYZERS:
        raise ValueError(f"duplicate analyzer {cls.name!r}")
    ANALYZERS[cls.name] = cls
    return cls
