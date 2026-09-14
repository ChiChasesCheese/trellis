"""q09 Jupyter Load Balancer — YOUR implementation. Run: python drill.py test q09"""
from __future__ import annotations

import sys


def route_requests(num_targets: int, max_connections_per_target: int, requests: list[str],
                   *, shutdown_permanent: bool = False, variant_b: bool = False) -> list[str]:
    """requests: 'CONNECT id user [object]' | 'DISCONNECT id' | 'SHUTDOWN t' (t 1-based).
    Return one 'id,user,target' line (target 1-based) per successful placement."""
    # TODO
    return []


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    if not lines:
        return
    n, cap = (int(x) for x in lines[0].split())
    out = route_requests(n, cap, lines[1:])
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
