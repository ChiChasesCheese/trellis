"""Address and host normalisation. Use these instead of ad-hoc ``split("@")``."""
from __future__ import annotations

from collections.abc import Iterable
from urllib.parse import urlsplit


def normalize_address(raw: str) -> str:
    """``"Dana <Dana@Acme.Example>"`` -> ``"dana@acme.example"``."""
    text = raw.strip()
    if "<" in text and text.endswith(">"):
        text = text[text.index("<") + 1 : -1]
    return text.strip().lower()


def domain_of(address: str) -> str:
    return address.rsplit("@", 1)[-1].lower() if "@" in address else ""


def is_internal(address: str, internal_domains: Iterable[str]) -> bool:
    return domain_of(address) in set(internal_domains)


def host_of(url: str) -> str:
    return (urlsplit(url).hostname or "").lower()
