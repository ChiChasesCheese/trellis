"""Perf sweep -> SLA verdict per (model, traffic profile) + anomaly flags.

    uv run --project <repo root> python solution.py data/*.csv --concurrency 16 --ttft-ms 1400 --tps-user 300

The only contract with the input is the header table below and the file-name pattern Model_<X>_profile_<N>.csv.
A new model is a new file or new rows: no code changes.
"""
from __future__ import annotations

import argparse
import csv
import re
from dataclasses import dataclass, field
from pathlib import Path

# ---------------------------------------------------------------- Part 1: the header contract

# canonical field -> {normalised header: multiplier into the canonical unit}
SYNONYMS: dict[str, dict[str, float]] = {
    "model": {"model": 1, "modelname": 1, "modelid": 1},
    "profile": {"profile": 1, "trafficprofile": 1, "workload": 1, "scenario": 1},
    "input_len": {"inputlen": 1, "inputtokens": 1, "isl": 1, "promptlen": 1, "prompttokens": 1, "inputlength": 1},
    "output_len": {"outputlen": 1, "outputtokens": 1, "osl": 1, "genlen": 1, "outputlength": 1,
                   "completiontokens": 1},
    "concurrency": {"concurrency": 1, "batchsize": 1, "bs": 1, "users": 1, "concurrentusers": 1, "numusers": 1},
    "ttft_ms": {"ttft": 1, "ttftms": 1, "timetofirsttoken": 1, "timetofirsttokenms": 1,
                "ttfts": 1000, "timetofirsttokens": 1000},
    "tpot_ms": {"tpot": 1, "tpotms": 1, "itl": 1, "itlms": 1, "intertokenlatency": 1, "intertokenlatencyms": 1,
                "timeperoutputtoken": 1, "timeperoutputtokenms": 1, "tpots": 1000, "itls": 1000},
    "tps_user": {"tpsuser": 1, "tokpersperuser": 1, "tokenspersperuser": 1, "tokenspersecondperuser": 1,
                 "pertpsuser": 1, "pertokpers": 1, "usertokpers": 1, "outputtokpersperuser": 1},
    "tps_total": {"tpstotal": 1, "totaltps": 1, "totaltokpers": 1, "totaltokenspers": 1, "throughput": 1,
                  "systemthroughput": 1, "totalthroughput": 1, "outputthroughput": 1},
}
NUMERIC = ("input_len", "output_len", "concurrency", "ttft_ms", "tpot_ms", "tps_user", "tps_total")
FILE_NAME = re.compile(r"Model_(?P<model>[^_]+)_profile_(?P<profile>[^_.]+)", re.I)


def normalize_header(h: str) -> str:
    """'TTFT (ms)' -> 'ttftms', 'tok/s/user' -> 'tokpersperuser': lower case, '/' read as 'per', keep [a-z0-9]."""
    return re.sub(r"[^a-z0-9]", "", h.lower().replace("/", "per"))


def map_headers(headers: list[str]) -> dict[str, tuple[str, float]]:
    """canonical field -> (the column that carries it, multiplier). Unknown columns are ignored.
    Raises ValueError if a numeric field has no column or two columns claim the same field."""
    lookup = {syn: (f, mult) for f, syns in SYNONYMS.items() for syn, mult in syns.items()}
    found: dict[str, tuple[str, float]] = {}
    for h in headers:
        hit = lookup.get(normalize_header(h))
        if hit is None:
            continue
        f, mult = hit
        if f in found:
            raise ValueError(f"columns {found[f][0]!r} and {h!r} both mean {f}")
        found[f] = (h, mult)
    missing = [f for f in NUMERIC if f not in found]
    if missing:
        raise ValueError(f"no column for {missing}; headers seen: {headers}")
    return found


@dataclass(frozen=True)
class Point:
    model: str
    profile: str
    input_len: int
    output_len: int
    concurrency: int
    ttft_ms: float
    tpot_ms: float
    tps_user: float
    tps_total: float


@dataclass(frozen=True)
class Anomaly:
    model: str
    profile: str
    concurrency: int | None
    kind: str  # missing_value | duplicate_point | throughput_drop | ttft_drop | total_mismatch | tpot_mismatch
    detail: str


def parse_sweep(path: str | Path) -> tuple[list[Point], list[Anomaly]]:
    """Rows -> Points. Model and profile come from columns, else from the file name. A row with an empty or
    non-numeric cell becomes a missing_value anomaly instead of a Point."""
    path = Path(path)
    with path.open(newline="") as f:
        reader = csv.DictReader(f)
        cols = map_headers(reader.fieldnames or [])
        from_name = FILE_NAME.search(path.stem)
        for key in ("model", "profile"):
            if key not in cols and not from_name:
                raise ValueError(f"{path.name}: no {key} column and the name is not Model_<X>_profile_<N>")
        points: list[Point] = []
        anomalies: list[Anomaly] = []
        for row in reader:
            model = row[cols["model"][0]].strip() if "model" in cols else from_name["model"]
            profile = row[cols["profile"][0]].strip() if "profile" in cols else from_name["profile"]
            values: dict[str, float] = {}
            bad = []
            for f in NUMERIC:
                col, mult = cols[f]
                try:
                    values[f] = float(row[col]) * mult
                except (TypeError, ValueError):
                    bad.append(col)
            if bad:
                conc = row.get(cols["concurrency"][0], "")
                anomalies.append(Anomaly(model, profile, int(float(conc)) if conc.strip() else None,
                                         "missing_value", f"{path.name}: empty or not a number in {bad}"))
                continue
            points.append(Point(model, profile, int(values["input_len"]), int(values["output_len"]),
                                int(values["concurrency"]), values["ttft_ms"], values["tpot_ms"],
                                values["tps_user"], values["tps_total"]))
    return points, anomalies


def load_all(paths: list[str | Path]) -> tuple[list[Point], list[Anomaly]]:
    points, anomalies = [], []
    for p in paths:
        pts, an = parse_sweep(p)
        points += pts
        anomalies += an
    return points, anomalies


def curves(points: list[Point]) -> dict[tuple[str, str], list[Point]]:
    """(model, profile) -> its points sorted by concurrency."""
    out: dict[tuple[str, str], list[Point]] = {}
    for p in points:
        out.setdefault((p.model, p.profile), []).append(p)
    return {k: sorted(v, key=lambda p: p.concurrency) for k, v in sorted(out.items())}


# ---------------------------------------------------------------- Part 2: the verdict


@dataclass(frozen=True)
class SLA:
    concurrency: int  # how many users the customer will run at once
    ttft_ms_max: float  # longest acceptable wait for the first token
    tps_user_min: float  # slowest acceptable reading speed per user
    amber_margin: float = 0.10  # passing by less than this fraction is amber


@dataclass
class Verdict:
    model: str
    profile: str
    color: str  # green | amber | red
    concurrency_used: int | None
    ttft_ms: float | None
    tps_user: float | None
    reasons: list[str] = field(default_factory=list)


def verdict_for(curve: list[Point], sla: SLA, flagged: set[int] = frozenset()) -> Verdict:
    """Judge one (model, profile) curve at the customer's load. Uses the smallest measured concurrency at or above
    the requested one (never a lighter load than asked: that would flatter the model) and says so when it differs.
    `flagged` = concurrencies on this curve that carry an anomaly: a green on suspect data becomes amber."""
    model, profile = curve[0].model, curve[0].profile
    at_or_above = [p for p in curve if p.concurrency >= sla.concurrency]
    if not at_or_above:
        top = curve[-1].concurrency
        return Verdict(model, profile, "red", None, None, None,
                       [f"no measurement at {sla.concurrency} users (largest is {top})"])
    p = at_or_above[0]
    reasons = []
    if p.concurrency != sla.concurrency:
        reasons.append(f"nearest measured load above {sla.concurrency} users: {p.concurrency}")
    ttft_margin = (sla.ttft_ms_max - p.ttft_ms) / sla.ttft_ms_max
    tps_margin = (p.tps_user - sla.tps_user_min) / sla.tps_user_min
    misses = []
    if ttft_margin < 0:
        misses.append(f"TTFT {p.ttft_ms:.0f} ms > {sla.ttft_ms_max:.0f} ms")
    if tps_margin < 0:
        misses.append(f"{p.tps_user:.0f} tok/s per user < {sla.tps_user_min:.0f}")
    if misses:
        return Verdict(model, profile, "red", p.concurrency, p.ttft_ms, p.tps_user, misses + reasons)
    color = "green"
    if min(ttft_margin, tps_margin) < sla.amber_margin:
        color = "amber"
        reasons.append(f"passes by only {min(ttft_margin, tps_margin):.0%}")
    if p.concurrency in flagged:
        color = "amber"
        reasons.append("the point used has an anomaly: check the data")
    return Verdict(model, profile, color, p.concurrency, p.ttft_ms, p.tps_user, reasons)


def verdicts(points: list[Point], sla: SLA, anomalies: list[Anomaly] = ()) -> list[Verdict]:
    flagged: dict[tuple[str, str], set[int]] = {}
    for a in anomalies:
        if a.concurrency is not None:
            flagged.setdefault((a.model, a.profile), set()).add(a.concurrency)
    return [verdict_for(c, sla, flagged.get(k, set())) for k, c in curves(points).items()]


# ---------------------------------------------------------------- Part 3: anomaly flags


def find_anomalies(points: list[Point], step_tol: float = 0.02, ratio_tol: float = 0.10) -> list[Anomaly]:
    """Checks a deployment engineer runs before trusting a sweep, per curve in concurrency order:
    - duplicate_point: the same concurrency twice (the later row is ignored by the other checks);
    - throughput_drop: total tok/s falls as load rises (more users should never lower the total);
    - ttft_drop: first-token wait shrinks as load rises (more users should never make it faster);
    - total_mismatch: per-user tok/s x users differs from total tok/s by more than ratio_tol;
    - tpot_mismatch: 1000 / TPOT(ms) differs from per-user tok/s by more than ratio_tol."""
    out: list[Anomaly] = []
    for (model, profile), curve in curves(points).items():
        seen: dict[int, Point] = {}
        for p in curve:
            if p.concurrency in seen:
                out.append(Anomaly(model, profile, p.concurrency, "duplicate_point", "two rows at this load"))
            else:
                seen[p.concurrency] = p
        uniq = list(seen.values())
        for prev, p in zip(uniq, uniq[1:]):
            if p.tps_total < prev.tps_total * (1 - step_tol):
                out.append(Anomaly(model, profile, p.concurrency, "throughput_drop",
                                   f"total {prev.tps_total:.0f} -> {p.tps_total:.0f} tok/s"))
            if p.ttft_ms < prev.ttft_ms * (1 - step_tol):
                out.append(Anomaly(model, profile, p.concurrency, "ttft_drop",
                                   f"TTFT {prev.ttft_ms:.0f} -> {p.ttft_ms:.0f} ms"))
        for p in uniq:
            expect = p.tps_user * p.concurrency
            if p.tps_total > 0 and abs(expect - p.tps_total) > ratio_tol * p.tps_total:
                out.append(Anomaly(model, profile, p.concurrency, "total_mismatch",
                                   f"{p.tps_user:.0f} x {p.concurrency} = {expect:.0f} vs total {p.tps_total:.0f}"))
            if p.tpot_ms > 0 and abs(1000 / p.tpot_ms - p.tps_user) > ratio_tol * p.tps_user:
                out.append(Anomaly(model, profile, p.concurrency, "tpot_mismatch",
                                   f"1000/{p.tpot_ms:.2f} ms = {1000 / p.tpot_ms:.0f} vs {p.tps_user:.0f} tok/s"))
    return out


# ---------------------------------------------------------------- Part 4: the report


def report(paths: list[str | Path], sla: SLA) -> str:
    points, parse_anomalies = load_all(paths)
    anomalies = parse_anomalies + find_anomalies(points)
    lines = [f"SLA: {sla.concurrency} users, TTFT <= {sla.ttft_ms_max:.0f} ms, >= {sla.tps_user_min:.0f} tok/s per user",
             f"{'model':8s} {'profile':8s} {'verdict':7s} {'load':>5s} {'TTFT ms':>8s} {'tok/s/user':>10s}  why"]
    for v in verdicts(points, sla, anomalies):
        load = "-" if v.concurrency_used is None else str(v.concurrency_used)
        ttft = "-" if v.ttft_ms is None else f"{v.ttft_ms:.0f}"
        tps = "-" if v.tps_user is None else f"{v.tps_user:.0f}"
        lines.append(f"{v.model:8s} {v.profile:8s} {v.color:7s} {load:>5s} {ttft:>8s} {tps:>10s}  "
                     + "; ".join(v.reasons))
    lines.append(f"anomalies: {len(anomalies)}")
    for a in sorted(anomalies, key=lambda a: (a.model, a.profile, a.concurrency or 0, a.kind)):
        lines.append(f"  {a.model} profile {a.profile} @ {a.concurrency}: {a.kind} ({a.detail})")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--concurrency", type=int, default=16)
    ap.add_argument("--ttft-ms", type=float, default=1400)
    ap.add_argument("--tps-user", type=float, default=300)
    a = ap.parse_args(argv)
    print(report(a.files, SLA(a.concurrency, a.ttft_ms, a.tps_user)))


if __name__ == "__main__":
    main()
