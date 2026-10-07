"""Evidence timeline: what the reviewer sees under a flagged identity, every line cited."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from vetting.models import Finding, Identity, Kind, Observation
from vetting.timeutil import to_iso

SOURCE_LABELS = {"greenhouse": "Greenhouse", "idp": "the identity provider"}


@dataclass(frozen=True)
class TimelineEntry:
    ts: datetime
    source: str
    ref: str
    text: str

    def to_dict(self) -> dict[str, str]:
        return {"ts": to_iso(self.ts), "source": self.source, "ref": self.ref, "text": self.text}


def build_timeline(
    identity: Identity, observations: list[Observation], findings: list[Finding]
) -> list[TimelineEntry]:
    label = SOURCE_LABELS.get(identity.source, identity.source)
    entries = [
        TimelineEntry(identity.applied_at, identity.source, identity.id, f"Application received via {label}")
    ]
    if any(o.kind is Kind.RESUME_SHA256 or o.kind is Kind.RESUME_NAME for o in observations):
        entries.append(
            TimelineEntry(
                identity.applied_at, identity.source, identity.id, "Resume extracted; automated analysis initiated"
            )
        )
    for finding in findings:
        for citation in finding.evidence:
            entries.append(TimelineEntry(citation.ts, citation.source, citation.ref, f"{finding.signal}: {finding.summary}"))
    last = max((e.ts for e in entries), default=identity.applied_at)
    entries.sort(key=lambda e: e.ts)
    entries.append(TimelineEntry(last, "vetting", identity.id, "Detection complete"))
    return entries
