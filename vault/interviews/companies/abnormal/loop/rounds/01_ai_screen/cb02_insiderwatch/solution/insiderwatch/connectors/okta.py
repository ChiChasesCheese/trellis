"""Okta System Log: sign-in events."""
from __future__ import annotations

from ..events import Action, Event
from ..timeutil import parse_ts
from .base import Connector, RawRecord, register_connector


@register_connector
class OktaConnector(Connector):
    source = "okta"

    def parse_page(self, payload: dict) -> tuple[list[dict], str | None]:
        return payload["data"], payload.get("next")

    def normalize(self, raw: RawRecord) -> Event | None:
        rec = raw.payload
        if rec.get("eventType") != "user.session.start":
            return self.drop("unmapped_event_type")
        failed = rec.get("outcome", {}).get("result") != "SUCCESS"
        geo = rec.get("client", {}).get("geographicalContext", {})
        return Event(
            user=rec["actor"]["alternateId"],
            ts=parse_ts(rec["published"]),
            action=Action.LOGIN_FAILED if failed else Action.LOGIN,
            target=rec.get("client", {}).get("ipAddress", ""),
            source=self.source,
            attrs={"country": geo.get("country", "")},
        )
