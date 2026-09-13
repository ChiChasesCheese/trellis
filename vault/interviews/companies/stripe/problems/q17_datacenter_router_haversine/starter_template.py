"""q17 Datacenter Request Router — YOUR implementation. Run: python drill.py test q17"""
from __future__ import annotations

import sys

EARTH_RADIUS_KM = 6371.0


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance in km (unrounded), R = 6371."""
    # TODO
    return 0.0


def process_commands(lines: list[str], tie: str = "name", allow_float: bool = False) -> list[str]:
    """lines: raw commands (REGISTER / SET_HEALTHZ / DISTANCE / ROUTE / RELEASE).
    Return one output line per command. tie: 'name' | 'registration' for equal distances."""
    # TODO
    return []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    out = process_commands(lines)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
