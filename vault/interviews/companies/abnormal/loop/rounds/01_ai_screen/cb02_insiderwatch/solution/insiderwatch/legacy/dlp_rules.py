"""DEPRECATED: the v1 DLP rule engine. Superseded by `insiderwatch.signals`.

Kept only so customers on the `legacy_dlp_rules` flag keep their old log lines until the
migration finishes (tracked in INSIDER-212). Do not add rules here and do not import it
from new code.
"""
from __future__ import annotations

import logging

from ..events import Action, Event

log = logging.getLogger(__name__)

BULK_DOWNLOAD_BYTES = 500 * 1024 * 1024
RULES = ("bulk_download", "external_share")


def check_bulk_download(event: Event) -> bool:
    return event.action is Action.FILE_DOWNLOAD and event.bytes >= BULK_DOWNLOAD_BYTES


def check_external_share(event: Event) -> bool:
    return event.action is Action.FILE_SHARE_EXTERNAL


def scan_event(event: Event) -> list[str]:
    """Return the names of the v1 rules this single event trips."""
    hits = []
    if check_bulk_download(event):
        hits.append("bulk_download")
    if check_external_share(event):
        hits.append("external_share")
    for hit in hits:
        log.warning("legacy dlp rule %s: user=%s target=%s", hit, event.user, event.target)
    return hits
