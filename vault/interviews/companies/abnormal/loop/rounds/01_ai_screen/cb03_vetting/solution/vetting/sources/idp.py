"""Identity-provider sign-ins for pre-boarding accounts: ``idp/*.jsonl``, one event per line.

These never create identities; they attach observations to the application they belong to
(``identity_id`` in the event). The pipeline counts events whose identity does not exist.
"""
from __future__ import annotations

import json
from collections.abc import Iterator
from pathlib import Path

from vetting.models import Kind
from vetting.sources.base import Ingested, Source, register_source
from vetting.timeutil import parse_ts


@register_source
class IdpSource(Source):
    name = "idp"

    def load(self, root: Path, tenant_id: str) -> Iterator[Ingested]:
        for path in sorted((root / "idp").glob("*.jsonl")):
            for line_no, line in enumerate(path.read_text().splitlines(), start=1):
                if not line.strip():
                    continue
                try:
                    event = json.loads(line)
                    identity_id = event["identity_id"]
                    ts = parse_ts(event["ts"])
                except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
                    self.bad_record(f"{path.name}:{line_no}: {exc!r}")
                    continue
                out: list = []
                where = f"idp/{path.name}:{line_no}"
                common = dict(out=out, identity_id=identity_id, tenant_id=tenant_id, ts=ts)
                self.observe(**common, kind=Kind.LOGIN_IP, value=event.get("ip"), path=f"{where}.ip")
                self.observe(
                    **common, kind=Kind.LOGIN_COUNTRY, value=(event.get("geo") or {}).get("country"), path=f"{where}.geo"
                )
                self.observe(**common, kind=Kind.DEVICE, value=event.get("device"), path=f"{where}.device")
                yield Ingested(None, out)
