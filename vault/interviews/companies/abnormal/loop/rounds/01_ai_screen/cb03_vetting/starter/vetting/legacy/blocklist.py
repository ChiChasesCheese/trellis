"""DEPRECATED. Static blocklist from before we had lookups and signals.

Nothing in the pipeline imports this any more: `vpn_hosting_ip` and `voip_phone` replaced it, and
their data comes from fixtures/intel. It stays until the 2026-Q4 cleanup because
tests/test_pipeline.py still pins its behaviour for the old export script. Do not extend it.
"""
from __future__ import annotations

BLOCKED_IPS = {"203.0.113.66", "203.0.113.67"}
BLOCKED_PHONE_PREFIXES = ("+1900", "+1976")


def is_blocked(ip: str | None = None, phone: str | None = None) -> bool:
    if ip and ip in BLOCKED_IPS:
        return True
    return bool(phone) and phone.startswith(BLOCKED_PHONE_PREFIXES)
