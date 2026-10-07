from __future__ import annotations

import ipaddress
import json
from dataclasses import dataclass
from pathlib import Path

from vetting.cache import TTLCache


@dataclass(frozen=True)
class IpInfo:
    country: str | None = None
    asn: str | None = None
    org: str | None = None
    is_vpn: bool = False
    is_hosting: bool = False


UNKNOWN_IP = IpInfo()


class IpLookup:
    """Geo / ASN / VPN lookup. The most specific matching CIDR in the table wins."""

    def __init__(self, rows: list[dict], cache: TTLCache[IpInfo]) -> None:
        self._networks = sorted(
            ((ipaddress.ip_network(row["cidr"]), row) for row in rows),
            key=lambda pair: pair[0].prefixlen,
            reverse=True,
        )
        self._cache = cache

    @classmethod
    def from_file(cls, path: Path, cache: TTLCache[IpInfo]) -> "IpLookup":
        return cls(json.loads(path.read_text()), cache)

    def lookup(self, ip: str) -> IpInfo:
        return self._cache.get_or_load(ip, self._load)

    def _load(self, ip: str) -> IpInfo:
        try:
            addr = ipaddress.ip_address(ip)
        except ValueError:
            return UNKNOWN_IP
        for network, row in self._networks:
            if addr.version == network.version and addr in network:
                return IpInfo(
                    country=row.get("country"),
                    asn=row.get("asn"),
                    org=row.get("org"),
                    is_vpn=bool(row.get("vpn")),
                    is_hosting=bool(row.get("hosting")),
                )
        return UNKNOWN_IP
