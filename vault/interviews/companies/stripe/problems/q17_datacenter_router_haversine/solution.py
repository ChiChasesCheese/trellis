"""q17 Datacenter Request Router — reference solution.

State per region: lat, lon, capacity, healthy, load, registration index. Invalid commands
return ERROR and never mutate state. Distances are ranked unrounded; only printing rounds.
"""
from __future__ import annotations

import math
import sys

EARTH_RADIUS_KM = 6371.0


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Great-circle distance in km (unrounded), R = 6371."""
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp, dl = math.radians(lat2 - lat1), math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * EARTH_RADIUS_KM * math.asin(math.sqrt(min(1.0, a)))


def round_half_up(d: float) -> int:
    return math.floor(d + 0.5)  # rule: nearest integer, x.5 rounds UP (not banker's)


class Router:
    def __init__(self, tie: str = "name", allow_float: bool = False) -> None:
        self.regions: dict[str, dict] = {}
        self.tie = tie
        self.allow_float = allow_float

    # -- parsing helpers -------------------------------------------------------------------
    def _num(self, tok: str) -> float | None:
        try:
            return float(tok) if self.allow_float else int(tok)
        except ValueError:
            return None

    def _nums(self, toks: list[str]) -> list[float] | None:
        vals = [self._num(t) for t in toks]
        return None if any(v is None for v in vals) else vals  # type: ignore[return-value]

    # -- commands ----------------------------------------------------------------------------
    def register(self, args: list[str]) -> str:
        if len(args) != 4:
            return "ERROR"
        name, nums = args[0], self._nums(args[1:])
        if nums is None or name in self.regions:
            return "ERROR"
        lat, lon, cap = nums
        if not (-90 <= lat <= 90 and -180 <= lon <= 180 and cap > 0):  # inclusive bounds, cap strictly > 0
            return "ERROR"
        self.regions[name] = {"lat": lat, "lon": lon, "cap": cap, "healthy": True, "load": 0,
                              "idx": len(self.regions),
                              # pre-computed radians / cos(lat) so ROUTE is one sin/sqrt per region
                              "phi": math.radians(lat), "lam": math.radians(lon), "cosphi": math.cos(math.radians(lat))}
        return "OK"

    def set_healthz(self, args: list[str]) -> str:
        if len(args) != 2 or args[0] not in self.regions or args[1].lower() not in ("true", "false"):
            return "ERROR"
        self.regions[args[0]]["healthy"] = args[1].lower() == "true"
        return "OK"

    def distance(self, args: list[str]) -> str:
        nums = self._nums(args) if len(args) == 4 else None
        if nums is None:
            return "ERROR"
        return str(round_half_up(haversine_km(*nums)))

    def route(self, args: list[str]) -> str:
        nums = self._nums(args) if len(args) == 2 else None
        if nums is None:
            return "ERROR"
        phi, lam = math.radians(nums[0]), math.radians(nums[1])
        cosphi = math.cos(phi)
        ranked = []
        for name, r in self.regions.items():
            if r["healthy"]:  # candidates = all healthy regions, even at full capacity
                a = math.sin((r["phi"] - phi) / 2) ** 2 + cosphi * r["cosphi"] * math.sin((r["lam"] - lam) / 2) ** 2
                d = 2 * EARTH_RADIUS_KM * math.asin(math.sqrt(min(1.0, a)))  # == haversine_km(...)
                # rank by UNROUNDED distance, then name (or registration order)
                ranked.append((d, name if self.tie == "name" else r["idx"], name))
        ranked.sort()
        names = [n for _, _, n in ranked]
        for d, _, name in ranked:
            r = self.regions[name]
            if r["load"] < r["cap"]:
                r["load"] += 1  # ROUTE consumes one unit of capacity
                return " ".join([name, str(round_half_up(d))] + names)
        return " ".join(["NONE", "0"] + names)

    def release(self, args: list[str]) -> str:  # Part 4 (reconstructed)
        if len(args) != 1 or args[0] not in self.regions or self.regions[args[0]]["load"] <= 0:
            return "ERROR"
        self.regions[args[0]]["load"] -= 1
        return "OK"

    def handle(self, line: str) -> str:
        cmd, *args = line.split()
        fn = {"REGISTER": self.register, "SET_HEALTHZ": self.set_healthz, "DISTANCE": self.distance,
              "ROUTE": self.route, "RELEASE": self.release}.get(cmd)
        return fn(args) if fn else "ERROR"


def process_commands(lines: list[str], tie: str = "name", allow_float: bool = False) -> list[str]:
    router = Router(tie=tie, allow_float=allow_float)
    return [router.handle(ln) for ln in (l.strip() for l in lines) if ln]


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    out = process_commands(lines)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
