"""Greenhouse Harvest-style applications: ``greenhouse/applications/*.json``, each a list."""
from __future__ import annotations

import json
import logging
from collections.abc import Iterator
from pathlib import Path
from typing import Any

from vetting.models import Identity, Kind
from vetting.sources.base import Ingested, Source, register_source
from vetting.timeutil import parse_ts

log = logging.getLogger(__name__)


def _first(items: list[dict[str, Any]] | None) -> str | None:
    return items[0].get("value") if items else None


@register_source
class GreenhouseSource(Source):
    name = "greenhouse"

    def load(self, root: Path, tenant_id: str) -> Iterator[Ingested]:
        for path in sorted((root / "greenhouse" / "applications").glob("*.json")):
            try:
                records = json.loads(path.read_text())
            except json.JSONDecodeError as exc:
                log.warning("greenhouse: unreadable file %s: %s", path.name, exc)
                self.bad_record(f"{path.name} is not valid JSON")
                continue
            for record in records:
                parsed = self._parse(record, tenant_id)
                if parsed is not None:
                    yield parsed

    def _parse(self, record: Any, tenant_id: str) -> Ingested | None:
        try:
            external_id = str(record["id"])
            applied_at = parse_ts(record["applied_at"])
            candidate = record.get("candidate") or {}
            full_name = f"{candidate.get('first_name', '')} {candidate.get('last_name', '')}".strip()
        except (KeyError, TypeError, ValueError, AttributeError) as exc:
            self.bad_record(repr(exc))
            return None

        identity = Identity(
            id=Identity.make_id(self.name, external_id),
            tenant_id=tenant_id,
            source=self.name,
            external_id=external_id,
            display_name=full_name or f"application {external_id}",
            applied_at=applied_at,
        )
        out: list = []
        emit = lambda kind, value, path: self.observe(  # noqa: E731
            out, identity_id=identity.id, tenant_id=tenant_id, kind=kind, value=value, ts=applied_at, path=path
        )
        emit(Kind.NAME, full_name, "candidate.name")
        emit(Kind.EMAIL, _first(candidate.get("email_addresses")), "candidate.email_addresses[0]")
        emit(Kind.PHONE, _first(candidate.get("phone_numbers")), "candidate.phone_numbers[0]")
        emit(Kind.COUNTRY, (candidate.get("location") or {}).get("country"), "candidate.location.country")
        submission = record.get("submission") or {}
        emit(Kind.IP, submission.get("ip_address"), "submission.ip_address")
        emit(Kind.USER_AGENT, submission.get("user_agent"), "submission.user_agent")

        for index, attachment in enumerate(record.get("attachments") or []):
            if attachment.get("type") != "resume":
                continue
            meta = attachment.get("metadata") or {}
            extracted = meta.get("extracted") or {}
            base = f"attachments[{index}].metadata"
            emit(Kind.RESUME_SHA256, meta.get("sha256"), f"{base}.sha256")
            emit(Kind.RESUME_AUTHOR, meta.get("author"), f"{base}.author")
            emit(Kind.RESUME_TOOL, meta.get("creator_tool"), f"{base}.creator_tool")
            emit(Kind.RESUME_NAME, extracted.get("name"), f"{base}.extracted.name")
            emit(Kind.RESUME_EMAIL, extracted.get("email"), f"{base}.extracted.email")
            emit(Kind.RESUME_PHONE, extracted.get("phone"), f"{base}.extracted.phone")
            break  # only the first resume attachment is analysed
        return Ingested(identity, out)
