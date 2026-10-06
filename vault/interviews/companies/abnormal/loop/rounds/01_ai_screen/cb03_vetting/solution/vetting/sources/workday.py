"""Workday recruiting export: ``workday/applications.json`` and the pages its ``Paging.next`` names.

A page is ``{"Report_Entry": [...], "Paging": {"next": "<cursor>" | null}}``; the cursor ``p2`` lives
in ``applications.p2.json``. Applications are re-delivered across pages, which is harmless because
identity ids come from ``Job_Application_ID`` and observations are de-duplicated on insert.
"""
from __future__ import annotations

import json
from collections.abc import Iterator
from pathlib import Path
from typing import Any

from vetting.models import Identity, Kind
from vetting.sources.base import Ingested, Source, register_source
from vetting.timeutil import parse_ts


@register_source
class WorkdaySource(Source):
    name = "workday"

    def load(self, root: Path, tenant_id: str) -> Iterator[Ingested]:
        base = root / "workday"
        cursor: str | None = ""
        seen: set[str] = set()
        while cursor is not None and cursor not in seen:
            seen.add(cursor)
            path = base / (f"applications.{cursor}.json" if cursor else "applications.json")
            if not path.exists():
                return
            try:
                page = json.loads(path.read_text())
            except json.JSONDecodeError:
                self.bad_record(f"{path.name} is not valid JSON")
                return
            for record in page.get("Report_Entry", []):
                parsed = self._parse(record, tenant_id)
                if parsed is not None:
                    yield parsed
            cursor = (page.get("Paging") or {}).get("next")

    def _parse(self, record: Any, tenant_id: str) -> Ingested | None:
        try:
            external_id = str(record["Job_Application_ID"])
            applied_at = parse_ts(record["Application_Date"])
            candidate = record.get("Candidate") or {}
            legal = candidate.get("Legal_Name") or {}
            full_name = f"{legal.get('First_Name', '')} {legal.get('Last_Name', '')}".strip()
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
        emit(Kind.NAME, full_name, "Candidate.Legal_Name")
        emit(Kind.EMAIL, candidate.get("Email_Address"), "Candidate.Email_Address")
        phone = candidate.get("Phone") or {}
        number = phone.get("Phone_Number")
        emit(Kind.PHONE, f"+{phone.get('Country_Code', '1')} {number}" if number else None, "Candidate.Phone")
        emit(
            Kind.COUNTRY,
            (candidate.get("Country_Reference") or {}).get("ISO_3166_1_Alpha_2_Code"),
            "Candidate.Country_Reference",
        )
        details = record.get("Source_Details") or {}
        emit(Kind.IP, details.get("IP_Address"), "Source_Details.IP_Address")
        emit(Kind.USER_AGENT, details.get("User_Agent"), "Source_Details.User_Agent")

        for index, attachment in enumerate(record.get("Attachments") or []):
            if attachment.get("Document_Category") != "Resume":
                continue
            meta = attachment.get("Metadata") or {}
            base = f"Attachments[{index}].Metadata"
            emit(Kind.RESUME_SHA256, meta.get("SHA256"), f"{base}.SHA256")
            emit(Kind.RESUME_AUTHOR, meta.get("Author"), f"{base}.Author")
            emit(Kind.RESUME_TOOL, meta.get("Creator_Tool"), f"{base}.Creator_Tool")
            emit(Kind.RESUME_NAME, meta.get("Extracted_Name"), f"{base}.Extracted_Name")
            emit(Kind.RESUME_EMAIL, meta.get("Extracted_Email"), f"{base}.Extracted_Email")
            emit(Kind.RESUME_PHONE, meta.get("Extracted_Phone"), f"{base}.Extracted_Phone")
            break
        return Ingested(identity, out)
