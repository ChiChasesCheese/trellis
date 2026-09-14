"""q22 Shipping Cost — reference solution.

Parts 1-3 (route version): directed legs (src, dst, carrier, cost); direct / one transfer /
Dijkstra.  Parts 4-5 (matrix version): country -> product -> unit cost or quantity bands, priced
in integer cents with Stripe's two tier modes (volume vs graduated).
"""
from __future__ import annotations

import heapq
import sys
from collections import defaultdict
from typing import NamedTuple


class Route(NamedTuple):
    src: str
    dst: str
    carrier: str
    cost: int


# ----------------------------------------------------------------------------- routes
def parse_routes(s: str) -> list[Route]:
    """'US:UK:FedEx:5,UK:US:UPS:4' (or 'US,UK,UPS,5:US,CA,FedEx,3') -> [Route, ...]."""
    s = s.strip()
    if not s:
        return []
    # the field separator is whichever of ':' / ',' appears 3x per leg; legs use the other one
    head = s.split(",")[0] if s.count(":") >= s.count(",") else s.split(":")[0]
    leg_sep, field_sep = (",", ":") if head.count(":") == 3 else (":", ",")
    routes = []
    for leg in s.split(leg_sep):
        if not leg.strip():
            continue
        src, dst, carrier, cost = (p.strip() for p in leg.split(field_sep))
        routes.append(Route(src, dst, carrier, int(cost)))
    return routes


def _adj(routes) -> dict[str, list[Route]]:
    """src -> legs out of src; duplicate (src,dst,carrier) keeps the cheaper leg.
    A dict is assumed to be an adjacency built earlier (main() builds it once for all queries)."""
    if isinstance(routes, dict):
        return routes
    best: dict[tuple[str, str, str], Route] = {}
    for r in routes:
        k = (r.src, r.dst, r.carrier)
        if k not in best or r.cost < best[k].cost:
            best[k] = r
    adj: dict[str, list[Route]] = defaultdict(list)
    for r in best.values():
        adj[r.src].append(r)
    return adj


def shipping_cost(routes: list[Route], src: str, dst: str, method: str) -> int:
    """Part 1: exact directed leg with that carrier; -1 if absent (no reverse, no transfer)."""
    costs = [r.cost for r in _adj(routes).get(src, []) if r.dst == dst and r.carrier == method]
    return min(costs) if costs else -1


def shipping_cost_one_transfer(routes: list[Route], src: str, dst: str) -> tuple[int, list[str]]:
    """Part 2: direct leg (any carrier) always wins; else cheapest src->X->dst.
    Ties -> lexicographically smallest [src, carrier, X, carrier, dst]. src == dst -> (0, [src])."""
    if src == dst:
        return 0, [src]
    adj = _adj(routes)
    direct = [(r.cost, [src, r.carrier, dst]) for r in adj.get(src, []) if r.dst == dst]
    if direct:
        return min(direct)
    two_leg = [
        (a.cost + b.cost, [src, a.carrier, a.dst, b.carrier, dst])
        for a in adj.get(src, [])
        if a.dst != dst
        for b in adj.get(a.dst, [])
        if b.dst == dst
    ]
    return min(two_leg) if two_leg else (-1, [])


def cheapest_shipping(routes: list[Route], src: str, dst: str) -> tuple[int, list[str]]:
    """Part 3: Dijkstra; ties -> fewer legs, then lexicographically smallest path."""
    adj = _adj(routes)
    heap = [(0, 0, [src])]  # (cost, legs, alternating path) — tuple order is the tie-break
    done: set[str] = set()
    while heap:
        cost, legs, path = heapq.heappop(heap)
        node = path[-1]
        if node == dst:
            return cost, path
        if node in done:
            continue
        done.add(node)
        for r in adj.get(node, []):
            if r.dst not in done:
                heapq.heappush(heap, (cost + r.cost, legs + 1, path + [r.carrier, r.dst]))
    return -1, []


def format_path(cost: int, path: list[str]) -> str:
    if cost < 0:
        return "-1"
    s = path[0]
    for i in range(1, len(path), 2):  # path = [country, carrier, country, carrier, ...]
        s += f"-{path[i]}->{path[i + 1]}"
    return f"{cost} {s}"


# ----------------------------------------------------------------------------- matrix
def _bands(spec) -> list[dict]:
    """Normalise a product entry to a sorted list of bands {min, max|None, cost|flat}."""
    if isinstance(spec, int):
        return [{"min": 1, "max": None, "cost": spec}]
    if "tiers" in spec:
        return sorted(spec["tiers"], key=lambda b: b["min"])
    return [{"min": 1, "max": None, **spec}]  # {"cost": 550} or {"flat": 2500}


def _product_table(country_entry) -> dict[str, list[dict]]:
    """List form [{"product":..,"cost":..}] or dict form -> product -> bands (last entry wins)."""
    if isinstance(country_entry, dict):
        return {p: _bands(spec) for p, spec in country_entry.items()}
    return {e["product"]: _bands(e) for e in country_entry}


def price_quantity(bands: list[dict], qty: int, mode: str) -> int:
    """Cents for `qty` units.  volume: the whole quantity at the band containing qty.
    graduated: each band charges its own units (or its flat amount once)."""
    if qty == 0:
        return 0
    if mode == "volume":
        for b in bands:
            if b["min"] <= qty and (b["max"] is None or qty <= b["max"]):  # max inclusive
                return b["flat"] if "flat" in b else qty * b["cost"]
        raise ValueError(f"no tier for quantity {qty}")
    if mode != "graduated":
        raise ValueError(f"unknown mode '{mode}'")
    total, covered = 0, 0
    for b in bands:
        hi = qty if b["max"] is None else min(qty, b["max"])
        units = hi - b["min"] + 1  # units of this order that fall inside [min, max]
        if units <= 0:
            continue
        total += b["flat"] if "flat" in b else units * b["cost"]
        covered = hi
        if covered == qty:
            return total
    raise ValueError(f"no tier for quantity {qty}")


def calculate_shipping_cost(order: dict, matrix: dict, mode: str = "volume") -> int:
    country = order["country"]
    if country not in matrix:
        raise ValueError(f"unknown country '{country}'")
    table = _product_table(matrix[country])
    qty_by_product: dict[str, int] = defaultdict(int)  # same product twice in one order -> summed
    for item in order["items"]:
        qty_by_product[item["product"]] += int(item["quantity"])
    total = 0
    for product, qty in qty_by_product.items():
        if product not in table:
            raise ValueError(f"unknown product '{product}' for country '{country}'")
        if qty < 0:
            raise ValueError(f"negative quantity for '{product}'")
        total += price_quantity(table[product], qty, mode)
    return total


# ----------------------------------------------------------------------------- stdin
def _parse_band(tok: str) -> dict:
    rng, price = tok.split(":")
    lo, hi = rng.split("-")
    band = {"min": int(lo), "max": int(hi) if hi else None}
    if price.startswith("="):
        band["flat"] = int(price[1:])
    else:
        band["cost"] = int(price)
    return band


def _run_matrix(lines: list[str], mode: str) -> list[str]:
    matrix: dict[str, dict] = defaultdict(dict)
    orders: list[dict] = []
    section = "MATRIX"
    for ln in lines:
        tok = ln.split()
        if tok[0] == "MATRIX":
            section = "MATRIX"
        elif tok[0] == "ORDER":
            section = "ORDER"
            orders.append({"country": tok[1], "items": []})
        elif section == "MATRIX":
            country, product, spec = tok[0], tok[1], tok[2:]
            if len(spec) == 1 and ":" not in spec[0]:
                matrix[country][product] = {"cost": int(spec[0])}
            else:
                matrix[country][product] = {"tiers": [_parse_band(t) for t in spec]}
        else:
            orders[-1]["items"].append({"product": tok[0], "quantity": int(tok[1])})
    out = []
    for order in orders:
        try:
            out.append(str(calculate_shipping_cost(order, matrix, mode)))
        except ValueError as e:
            out.append(f"ERROR: {e}")
    return out


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    if not lines:
        return
    part = int(lines[0].split()[1])
    out: list[str] = []
    if part <= 3:
        routes = _adj(parse_routes(lines[1]) if len(lines) > 1 else [])  # adjacency built once
        for q in lines[2:]:
            f = q.split()
            if part == 1:
                out.append(str(shipping_cost(routes, f[0], f[1], f[2])))
            elif part == 2:
                out.append(format_path(*shipping_cost_one_transfer(routes, f[0], f[1])))
            else:
                out.append(format_path(*cheapest_shipping(routes, f[0], f[1])))
    else:
        mode, body = "volume", lines[1:]
        if body and body[0].startswith("MODE"):
            mode, body = body[0].split()[1], body[1:]
        out = _run_matrix(body, mode)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
