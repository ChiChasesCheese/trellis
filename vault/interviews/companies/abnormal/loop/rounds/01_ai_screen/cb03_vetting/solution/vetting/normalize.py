"""Canonical forms for the values we compare: phone numbers, emails, names, IP prefixes.

Observations keep the value exactly as the source gave it (the evidence timeline shows what was
submitted). Anything that compares two values must go through these functions first.
"""
from __future__ import annotations

import ipaddress
import re
import unicodedata

# Providers where dots in the local part do not matter (a.b@x == ab@x).
DOT_INSENSITIVE_DOMAINS = frozenset({"gmail.com", "googlemail.com", "mail.example.org"})

_EXTENSION = re.compile(r"(?:\s*(?:x|ext\.?|extension)\s*\d+)\s*$", re.IGNORECASE)
_COUNTRY_NAMES = {"UNITED STATES": "US", "USA": "US", "UNITED KINGDOM": "GB", "UK": "GB", "GERMANY": "DE"}


def phone_e164(raw: str | None, default_country_code: str = "1") -> str | None:
    """Return ``+<digits>`` or None when the input cannot be a phone number.

    Strips extensions ("x204", "ext. 9"), punctuation and a ``00`` international prefix. A bare
    10-digit number gets the default country code.
    """
    if not raw:
        return None
    text = _EXTENSION.sub("", raw.strip())
    plus = text.startswith("+")
    digits = re.sub(r"\D", "", text)
    if not plus and digits.startswith("00"):
        plus, digits = True, digits[2:]
    if not plus:
        if len(digits) == 10:
            digits = default_country_code + digits
        elif len(digits) == 11 and digits.startswith(default_country_code):
            pass
        else:
            return None
    if not 8 <= len(digits) <= 15:
        return None
    return "+" + digits


def phone_prefix(e164: str, digits: int) -> str:
    """The first ``digits`` digits after the ``+`` (shorter numbers are returned whole)."""
    return e164[: 1 + digits]


def email_key(raw: str | None) -> str | None:
    """Lower-case, drop ``+tag`` and, for dot-insensitive providers, dots in the local part."""
    if not raw or "@" not in raw:
        return None
    local, _, domain = raw.strip().lower().rpartition("@")
    local = local.split("+", 1)[0]
    if domain in DOT_INSENSITIVE_DOMAINS:
        local = local.replace(".", "")
    if not local or not domain:
        return None
    return f"{local}@{domain}"


def email_domain(raw: str | None) -> str | None:
    key = email_key(raw)
    return key.rpartition("@")[2] if key else None


def name_key(raw: str | None) -> str | None:
    """Case, accents, punctuation and word order do not matter: "Müller, Zoë" == "zoe muller"."""
    if not raw:
        return None
    decomposed = unicodedata.normalize("NFKD", raw)
    stripped = "".join(ch for ch in decomposed if not unicodedata.combining(ch))
    words = re.sub(r"[^\w\s]|_", " ", stripped.casefold()).split()
    return " ".join(sorted(words)) or None


def ip_prefix24(raw: str | None) -> str | None:
    """IPv4 -> its /24 (``198.51.100.0/24``); IPv6 -> its /48. None if unparseable."""
    if not raw:
        return None
    try:
        addr = ipaddress.ip_address(raw.strip())
    except ValueError:
        return None
    width = 24 if addr.version == 4 else 48
    return str(ipaddress.ip_network(f"{addr}/{width}", strict=False))


def country_code(raw: str | None) -> str | None:
    """ISO 3166-1 alpha-2 in upper case; accepts a few common long names."""
    if not raw:
        return None
    text = raw.strip().upper()
    if len(text) == 2 and text.isalpha():
        return text
    return _COUNTRY_NAMES.get(text)
