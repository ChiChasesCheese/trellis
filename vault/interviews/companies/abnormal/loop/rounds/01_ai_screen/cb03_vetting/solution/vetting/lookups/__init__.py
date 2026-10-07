"""External lookups (carrier, IP intelligence, domain reputation).

The implementations here read ``fixtures/intel/*.json``; production swaps in API-backed ones with
the same ``lookup`` method. Signals only ever see the ``Lookups`` bundle, never a file path.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from vetting.cache import TTLCache
from vetting.lookups.email import EmailInfo, EmailLookup
from vetting.lookups.ip import IpInfo, IpLookup
from vetting.lookups.phone import LineType, PhoneInfo, PhoneLookup

__all__ = ["Lookups", "build_lookups", "EmailInfo", "IpInfo", "LineType", "PhoneInfo"]


@dataclass(frozen=True)
class Lookups:
    phone: PhoneLookup
    ip: IpLookup
    email: EmailLookup


def build_lookups(intel_dir: Path, ttl_seconds: float = 3600) -> Lookups:
    return Lookups(
        phone=PhoneLookup.from_file(intel_dir / "phone.json", TTLCache(ttl_seconds)),
        ip=IpLookup.from_file(intel_dir / "ip.json", TTLCache(ttl_seconds)),
        email=EmailLookup.from_file(intel_dir / "email.json", TTLCache(ttl_seconds)),
    )
