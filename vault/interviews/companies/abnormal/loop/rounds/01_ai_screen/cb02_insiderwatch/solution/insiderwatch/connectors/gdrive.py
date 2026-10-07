"""Google Workspace Drive audit log (Admin SDK Reports API, `drive` application)."""
from __future__ import annotations

from typing import Any

from ..events import Action, Event, is_external
from ..timeutil import parse_ts
from .base import Connector, RawRecord, register_connector

_EXPOSED_VISIBILITY = {"people_with_link", "public_on_the_web"}


def _params(event: dict) -> dict[str, Any]:
    """Flatten the API's [{name, value|intValue|boolValue|multiValue}] parameter list."""
    out: dict[str, Any] = {}
    for p in event.get("parameters", []):
        if "intValue" in p:
            out[p["name"]] = int(p["intValue"])  # the API sends int64 as a string
        elif "boolValue" in p:
            out[p["name"]] = p["boolValue"]
        elif "multiValue" in p:
            out[p["name"]] = p["multiValue"]
        else:
            out[p["name"]] = p.get("value")
    return out


@register_connector
class GDriveConnector(Connector):
    source = "gdrive"

    def parse_page(self, payload: dict) -> tuple[list[dict], str | None]:
        # One activity item can carry several events; each becomes its own record.
        records = [
            {"time": item["id"]["time"], "actor": item.get("actor", {}), "ip": item.get("ipAddress", ""), "event": ev}
            for item in payload.get("items", [])
            for ev in item.get("events", [])
        ]
        return records, payload.get("nextPageToken")

    def normalize(self, raw: RawRecord) -> Event | None:
        rec = raw.payload
        email = rec["actor"].get("email")
        if not email:
            return self.drop("no_user")
        ts = parse_ts(rec["time"])
        name = rec["event"].get("name", "")
        params = _params(rec["event"])
        target = params.get("doc_title", "")
        attrs = {"doc_id": params.get("doc_id", ""), "ip": rec["ip"]}
        if name == "download":
            return Event(email, ts, Action.FILE_DOWNLOAD, bytes=params.get("file_size", 0), target=target,
                         source=self.source, attrs=attrs)
        if name == "change_document_visibility":
            if params.get("visibility") in _EXPOSED_VISIBILITY:
                return Event(email, ts, Action.FILE_SHARE_EXTERNAL, target=target, source=self.source,
                             attrs={**attrs, "visibility": params["visibility"]})
            return self.drop("visibility_not_exposed")
        if name == "change_user_access":
            who = params.get("target_user", "")
            if who and is_external(who, self.config.internal_domains):
                return Event(email, ts, Action.FILE_SHARE_EXTERNAL, target=target, source=self.source,
                             attrs={**attrs, "shared_with": who})
            return self.drop("internal_access_change")
        return self.drop("unmapped_event")
