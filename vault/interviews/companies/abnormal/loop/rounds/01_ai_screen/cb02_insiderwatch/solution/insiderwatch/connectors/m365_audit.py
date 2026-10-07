"""Microsoft 365 unified audit log (Management Activity API shape)."""
from __future__ import annotations

from ..events import Action, Event, is_external
from ..timeutil import parse_ts
from .base import Connector, RawRecord, register_connector

_OPERATIONS = {
    "FileDownloaded": Action.FILE_DOWNLOAD,
    "FileSyncDownloadedFull": Action.FILE_DOWNLOAD,
    "FileUploaded": Action.FILE_UPLOAD,
    "FileDeleted": Action.FILE_DELETE,
}


def _param(record: dict, name: str) -> str | None:
    for item in record.get("Parameters", []):
        if item.get("Name") == name:
            return item.get("Value")
    return None


@register_connector
class M365AuditConnector(Connector):
    source = "m365_audit"

    def parse_page(self, payload: dict) -> tuple[list[dict], str | None]:
        return payload["Records"], payload.get("NextPage")

    def normalize(self, raw: RawRecord) -> Event | None:
        rec = raw.payload
        op = rec.get("Operation", "")
        user = rec.get("UserId")
        if not user:
            return self.drop("no_user")
        ts = parse_ts(rec["CreationTime"])  # naive in the API, UTC by contract
        if op in _OPERATIONS:
            return Event(user, ts, _OPERATIONS[op], bytes=int(rec.get("FileSize", 0)),
                         target=rec.get("ObjectId", ""), source=self.source,
                         attrs={"workload": rec.get("Workload", ""), "ip": rec.get("ClientIP", "")})
        if op == "SharingSet":
            if rec.get("TargetUserOrGroupType") == "Guest":
                return Event(user, ts, Action.FILE_SHARE_EXTERNAL, target=rec.get("ObjectId", ""),
                             source=self.source, attrs={"shared_with": rec.get("TargetUserOrGroupName", "")})
            return self.drop("internal_share")
        if op == "New-InboxRule":
            forward_to = _param(rec, "ForwardTo")
            if forward_to and is_external(forward_to, self.config.internal_domains):
                return Event(user, ts, Action.EMAIL_FORWARD_EXTERNAL, target=forward_to, source=self.source)
            return self.drop("internal_or_no_forward")
        return self.drop("unmapped_operation")
