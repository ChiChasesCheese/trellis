#!/usr/bin/env python3
"""Deterministically (re)build env/ for ic02_api_5xx.  Stdlib only; no clock, no network.

    python3 build_env.py [--out DIR]          # default: ./env

A per-minute model (traffic by tenant x route -> outcome categories per phase) drives every metric and the sampled
request logs, so ALB counts, route metrics, pool and RDS numbers agree with each other.  Everything is UTC.

Phases (reconstructed story):
  pre  < 09:40:07   normal
  A    09:40:07 - 09:52:14   migration 0142 holds ACCESS EXCLUSIVE on `alerts` (ALTER + non-concurrent CREATE INDEX in one
                             transaction); every pooled connection waits on the lock -> pool exhausted -> 503 / 504
  B    >= 09:52:14  pipeline killed the migration (720 s timeout), transaction rolled back, lock released -- but the
                    index the new /timeline endpoint needs was never built: seq-ish scans saturate RDS IO + the pool
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import random
import shutil
from datetime import datetime, timedelta, timezone
from pathlib import Path

UTC = timezone.utc
DAY = datetime(2026, 10, 2, tzinfo=UTC)


def hm(h, m, s=0):
    return DAY.replace(hour=h, minute=m, second=s)


START, NOW = hm(8, 30), hm(10, 5)
WEB_DEPLOY_DONE = hm(9, 35, 40)          # portal-web starts calling /timeline
DEPLOY = hm(9, 39, 30)
LOCK_ON, LOCK_OFF = hm(9, 40, 7), hm(9, 52, 14)
ACCOUNT, REGION = "111122223333", "us-east-1"
TASKS, POOL, MAXCONN, OTHER_CONN = 12, 20, 300, 52
NEW_AT = {40: 3, 41: 6, 42: 9, 43: 12}    # minute-of-09 -> new tasks serving
OLD_VER, NEW_VER = "2026.10.01-1610-c41d2a9", "2026.10.02-0939-e7b05f1"
LB = "app/portal-alb/7f3e2b1c9d4a6e05"
TG = "targetgroup/portal-api/3c9a1e7d2b6f4a80"
ALB_DIMS = f"LoadBalancer={LB}"
TG_DIMS = f"LoadBalancer={LB};TargetGroup={TG}"
DB = "DBInstanceIdentifier=portal-prod"

BASE_MIX = {"alerts_list": .35, "alert_detail": .20, "users_risk": .15, "config": .10, "me": .10, "search": .10}
TIMELINE_RATIO = .12
DB_ROUTES = {"alerts_list", "alert_detail", "users_risk", "timeline"}
PATH = {"alerts_list": "/api/v2/alerts", "alert_detail": "/api/v2/alerts/{id}", "users_risk": "/api/v2/users/{id}/risk",
        "timeline": "/api/v2/users/{id}/timeline", "config": "/api/v2/config", "me": "/api/v2/me", "search": "/api/v2/search"}
NORMAL = {"alerts_list": (70, .6), "alert_detail": (22, .5), "users_risk": (18, .5), "config": (4, .4), "me": (5, .4),
          "search": (110, .6), "timeline": (900, .5)}
OTHER_TENANTS = ["tn-kestrel", "tn-larch", "tn-heron", "tn-wren", "tn-ibis", "tn-alder", "tn-finch", "tn-moss"]

E503 = "sqlalchemy.exc.TimeoutError: QueuePool limit of size 20 overflow 0 reached, connection timed out, timeout 10.00"
E500 = "asyncpg.exceptions.QueryCanceledError: canceling statement due to statement timeout"
SLOT = "asyncpg.exceptions.TooManyConnectionsError: remaining connection slots are reserved for non-replication superuser connections"
TL_SQL = "SELECT id, kind, severity, created_at FROM alerts WHERE tenant_id = $1 AND user_id = $2 ORDER BY created_at DESC LIMIT 50"
LIST_SQL = "SELECT id, kind, severity, status, created_at FROM alerts WHERE tenant_id = $1 AND status = $2 AND (created_at, id) < ($3, $4) ORDER BY created_at DESC, id DESC LIMIT 100"


def iso(d: datetime) -> str:
    return d.strftime("%Y-%m-%dT%H:%M:%SZ")


def minutes():
    d = START
    while d <= NOW:
        yield d
        d += timedelta(minutes=1)


def overlap(d, lo, hi):
    a, b = max(d, lo), min(d + timedelta(minutes=1), hi)
    return max(0.0, (b - a).total_seconds()) / 60


def phases(d):
    a = overlap(d, LOCK_ON, LOCK_OFF)
    b = overlap(d, LOCK_OFF, hm(23, 59))
    return {"pre": 1 - a - b, "A": a, "B": b}


def new_frac(d):
    n = 0
    for m, k in sorted(NEW_AT.items()):
        if d >= hm(9, m):
            n = k
    return n / TASKS


def running_tasks(d):
    return 15 if hm(9, 40) <= d < hm(9, 44) else 12


def outcomes(route, group, phase, rng):
    """[(fraction, kind, median_ms, sigma)]; kind: ok | 401 | 503 | 504 | 500"""
    med, sg = NORMAL[route]
    if route == "timeline" and phase != "B":
        med = 6500 if group == "orbit" else 900
    if phase == "pre" or route not in DB_ROUTES:
        out = [(1.0, "ok", med, sg)]
        if route == "me":
            out = [(.97, "ok", med, sg), (.03, "401", 3, .3)]
        if route == "search":
            out = [(.9995, "ok", med, sg), (.0005, "500", 5000, .05)]
        return out
    if phase == "A":
        return [(.04, "504", 30000, .01), (.96, "503", 10000, .003)]
    j = 1 + rng.uniform(-.15, .15)
    if route == "timeline":
        if group == "orbit":
            return [(.35 * j, "504", 30000, .01), (.25 * j, "503", 10000, .003), (1 - .6 * j, "ok", 8500, .35)]
        return [(.15 * j, "503", 10000, .003), (1 - .15 * j, "ok", 2300, .5)]
    okm = {"alerts_list": 1700, "alert_detail": 1100, "users_risk": 1000}[route]
    return [(.08 * j, "503", 10000, .003), (1 - .08 * j, "ok", okm, .7)]


Z = [-2.326, -1.645, -1.282, -1.036, -.842, -.674, -.524, -.385, -.253, -.126, 0, .126, .253, .385, .524, .674, .842,
     1.036, 1.282, 1.645, 2.326, 2.576, 2.878, 3.09]


def quantile_points(count, med, sg):
    """24 representative points of a lognormal (heavier sampling of the tail) with weights summing to count."""
    w = [1 / 21] * 21 + [0, 0, 0]
    w[20] = 1 / 21 - .015
    w[21], w[22], w[23] = .008, .005, .002
    return [(med * math.exp(sg * z), count * wi) for z, wi in zip(Z, w)]


def wpct(pts, p):
    pts = sorted(pts)
    tot = sum(w for _, w in pts)
    acc = 0
    for v, w in pts:
        acc += w
        if acc >= p / 100 * tot:
            return v
    return pts[-1][0]


def simulate(rng):
    rows = []
    for d in minutes():
        hour = (d - START).total_seconds() / 3600
        others = 220 * (1 + .04 * math.sin(hour * 2.2)) + rng.uniform(-6, 6)
        ramp = min(1.0, max(0.0, (d - hm(9, 0)).total_seconds() / 1200))
        orbit = 30 + 30 * ramp + rng.uniform(-2, 2)
        ph = phases(d)
        f = new_frac(d)
        cats = []        # (route, group, phase, kind, count, med, sg)
        for group, rps in (("orbit", orbit), ("others", others)):
            n = rps * 60
            for route, mix in BASE_MIX.items():
                for phase, pf in ph.items():
                    if pf <= 0:
                        continue
                    for frac, kind, med, sg in outcomes(route, group, phase, rng):
                        cats.append((route, group, phase, kind, n * mix * pf * frac, med, sg))
            if d >= WEB_DEPLOY_DONE.replace(second=0):
                tl = n * TIMELINE_RATIO * (overlap(d, WEB_DEPLOY_DONE, hm(23, 59)))
                cats.append(("timeline", group, "pre", "404", tl * (1 - f), 3, .3))
                for phase, pf in ph.items():
                    if pf <= 0 or f == 0:
                        continue
                    for frac, kind, med, sg in outcomes("timeline", group, phase, rng):
                        cats.append(("timeline", group, phase, kind, tl * f * pf * frac, med, sg))
        total = sum(c[4] for c in cats)
        by = lambda pred: sum(c[4] for c in cats if pred(c))
        ok = by(lambda c: c[3] == "ok")
        t4 = by(lambda c: c[3] in ("401", "404"))
        t5 = by(lambda c: c[3] in ("503", "500"))
        e504 = by(lambda c: c[3] == "504")
        # ALB view: a 504 is the ALB giving up at its 15 s idle timeout; it has no target response time
        alb_pts = []
        for c in cats:
            if c[3] != "504":
                alb_pts += quantile_points(c[4], c[5], c[6])
        trt_avg = sum(v * w for v, w in alb_pts) / sum(w for _, w in alb_pts) / 1000
        trt_p99 = wpct(alb_pts, 99) / 1000
        route_stats = {}
        for r in PATH:
            rc = [c for c in cats if c[0] == r and c[3] != "404"]
            cnt = sum(c[4] for c in rc)
            if cnt < 0.5:
                continue
            pts = []
            for c in rc:
                pts += quantile_points(c[4], c[5], c[6])
            route_stats[r] = (cnt, sum(v * w for v, w in pts) / sum(w for _, w in pts), wpct(pts, 99))
        rows.append(dict(d=d, ph=ph, f=f, orbit=orbit, others=others, cats=cats, total=total, ok=ok, t4=t4, t5=t5,
                         e504=e504, trt_avg=trt_avg, trt_p99=trt_p99, route_stats=route_stats,
                         rate5xx=100 * (t5 + e504) / total))
    return rows


def fmt(v):
    return f"{v:.2f}".rstrip("0").rstrip(".") if isinstance(v, float) else str(v)


def write_csv(out: Path, ns: str, name: str, rows, extra=None):
    d = out / "cloudwatch" / "metrics" / ns.replace("/", "_")
    d.mkdir(parents=True, exist_ok=True)
    with (d / f"{name}.csv").open("w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["timestamp", "value", "dimensions"] + ([extra] if extra else []))
        for r in rows:
            w.writerow([iso(r[0]), fmt(float(r[1])), r[2]] + ([fmt(float(r[3]))] if extra else []))


def wj(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2) + "\n")


def write_jsonl(path: Path, recs):
    path.parent.mkdir(parents=True, exist_ok=True)
    recs = sorted((r for r in recs if START <= datetime.fromisoformat(r["timestamp"].replace("Z", "+00:00")) <= NOW),
                  key=lambda r: r["timestamp"])
    path.write_text("".join(json.dumps(r, separators=(",", ":")) + "\n" for r in recs))


def first_run(series, pred, n):
    run = 0
    for d, v in series:
        run = run + 1 if pred(v) else 0
        if run == n:
            return d
    return None


def blend(ph, pre, a, b):
    return ph["pre"] * pre + ph["A"] * a + ph["B"] * b


def build(out: Path):
    rng = random.Random(20261002)
    sim = simulate(rng)

    # ---------------- ALB
    write_csv(out, "AWS/ApplicationELB", "RequestCount", [(r["d"], r["total"], ALB_DIMS) for r in sim])
    write_csv(out, "AWS/ApplicationELB", "HTTPCode_Target_2XX_Count", [(r["d"], r["ok"], TG_DIMS) for r in sim])
    write_csv(out, "AWS/ApplicationELB", "HTTPCode_Target_4XX_Count", [(r["d"], r["t4"], TG_DIMS) for r in sim])
    write_csv(out, "AWS/ApplicationELB", "HTTPCode_Target_5XX_Count", [(r["d"], r["t5"], TG_DIMS) for r in sim])
    write_csv(out, "AWS/ApplicationELB", "HTTPCode_ELB_5XX_Count", [(r["d"], r["e504"], ALB_DIMS) for r in sim])
    write_csv(out, "AWS/ApplicationELB", "HTTPCode_ELB_504_Count", [(r["d"], r["e504"], ALB_DIMS) for r in sim])
    write_csv(out, "AWS/ApplicationELB", "HTTPCode_ELB_503_Count", [(r["d"], 0, ALB_DIMS) for r in sim])
    write_csv(out, "AWS/ApplicationELB", "TargetResponseTime", [(r["d"], r["trt_avg"], TG_DIMS, r["trt_p99"]) for r in sim], "p99")
    write_csv(out, "AWS/ApplicationELB", "HealthyHostCount", [(r["d"], running_tasks(r["d"]), TG_DIMS) for r in sim])
    write_csv(out, "AWS/ApplicationELB", "ClientTLSNegotiationErrorCount", [(r["d"], rng.choice([0, 0, 0, 0, 1, 1, 2]), ALB_DIMS) for r in sim])

    # ---------------- app metrics
    rs = []
    rl = []
    for r in sim:
        for route, (cnt, avg, p99) in r["route_stats"].items():
            rs.append((r["d"], cnt, f"Service=portal-api;Route={route}"))
            rl.append((r["d"], avg, f"Service=portal-api;Route={route}", p99))
    write_csv(out, "Portal/API", "RouteRequestCount", rs)
    write_csv(out, "Portal/API", "RouteLatencyMs", rl, "p99")
    write_csv(out, "Portal/API", "TenantRequestCount", [(r["d"], r["orbit"] * 60 * (1 + TIMELINE_RATIO * (r["d"] >= WEB_DEPLOY_DONE)), "Service=portal-api;Tenant=tn-orbit") for r in sim] +
              [(r["d"], r["others"] * 60 * (1 + TIMELINE_RATIO * (r["d"] >= WEB_DEPLOY_DONE)), "Service=portal-api;Tenant=all-others") for r in sim])
    slots = MAXCONN - 3 - OTHER_CONN                                  # 245 usable by portal-api
    pool_max = []
    pool_wait = []
    for r in sim:
        cap = min(POOL * running_tasks(r["d"]), slots)
        busy_pre = 14 + rng.uniform(-3, 9)
        busy = blend(r["ph"], busy_pre, cap, POOL * TASKS)
        if r["ph"]["A"] > 0 or r["ph"]["B"] > 0:
            busy = cap if r["ph"]["A"] > 0 else POOL * TASKS
        pool_max.append((r["d"], round(busy), "Service=portal-api"))
        pool_wait.append((r["d"], blend(r["ph"], .3 + rng.uniform(0, .2), 9600 + rng.uniform(-150, 150), 1400 + rng.uniform(-200, 200)),
                          "Service=portal-api", blend(r["ph"], 2 + rng.uniform(0, 1.5), 10000, 10000)))
    write_csv(out, "Portal/API", "DbPoolInUse", pool_max)
    write_csv(out, "Portal/API", "DbPoolWaitMs", pool_wait, "p99")

    # ---------------- ECS
    write_csv(out, "AWS/ECS", "CPUUtilization", [(r["d"], blend(r["ph"], 33, 7, 15) + rng.uniform(-1.5, 1.5), "ClusterName=prod;ServiceName=portal-api") for r in sim])
    write_csv(out, "AWS/ECS", "MemoryUtilization", [(r["d"], 41 + rng.uniform(-1, 1), "ClusterName=prod;ServiceName=portal-api") for r in sim])
    write_csv(out, "ECS/ContainerInsights", "RunningTaskCount", [(r["d"], running_tasks(r["d"]), "ClusterName=prod;ServiceName=portal-api") for r in sim])

    # ---------------- RDS
    conns = []
    for r in sim:
        if r["ph"]["A"] > 0 and hm(9, 40) <= r["d"] < hm(9, 44):
            v = MAXCONN - 3
        elif r["ph"]["A"] > 0:
            v = POOL * TASKS + OTHER_CONN + 1
        elif r["ph"]["B"] > 0:
            v = POOL * TASKS + OTHER_CONN
        else:
            v = 108 + OTHER_CONN + rng.choice([-2, -1, 0, 0, 1, 2])
        conns.append((r["d"], v, DB))
    write_csv(out, "AWS/RDS", "DatabaseConnections", conns)
    write_csv(out, "AWS/RDS", "CPUUtilization", [(r["d"], blend(r["ph"], 18 + rng.uniform(-2, 2), 24 + rng.uniform(-2, 2), 91 + rng.uniform(-2.5, 2.5)), DB) for r in sim])
    write_csv(out, "AWS/RDS", "ReadIOPS", [(r["d"], blend(r["ph"], 1400 + rng.uniform(-90, 90), 6400 + rng.uniform(-200, 200), 11800 + rng.uniform(-150, 150)), DB) for r in sim])
    write_csv(out, "AWS/RDS", "WriteIOPS", [(r["d"], blend(r["ph"], 900 + rng.uniform(-60, 60), 2400 + rng.uniform(-100, 100), 950 + rng.uniform(-60, 60)), DB) for r in sim])
    write_csv(out, "AWS/RDS", "ReadLatency", [(r["d"], round(blend(r["ph"], .0008, .0015, .0093) + rng.uniform(-.0001, .0001), 4), DB) for r in sim])
    load = [(r["d"], blend(r["ph"], 1.2 + rng.uniform(-.2, .3), 270 + rng.uniform(-6, 6), 38 + rng.uniform(-3, 3))) for r in sim]
    loadcpu = [(r["d"], blend(r["ph"], 1.0 + rng.uniform(-.15, .15), 1.6 + rng.uniform(-.2, .2), 7.4 + rng.uniform(-.3, .3))) for r in sim]
    write_csv(out, "AWS/RDS", "DBLoad", [(d, v, DB) for d, v in load])
    write_csv(out, "AWS/RDS", "DBLoadCPU", [(d, v, DB) for d, v in loadcpu])
    write_csv(out, "AWS/RDS", "DBLoadNonCPU", [(d, v - c, DB) for (d, v), (_, c) in zip(load, loadcpu)])

    # ---------------- alarms
    rate = [(r["d"], r["rate5xx"] if r["trt_p99"] > 3 else 0.0) for r in sim]
    page_t = first_run(rate, lambda v: v > 5, 3)
    conn_t = first_run([(d, v) for d, v, _ in conns], lambda v: v > 270, 3)
    cpu_series = []
    for row in (out / "cloudwatch" / "metrics" / "AWS_RDS" / "CPUUtilization.csv").read_text().splitlines()[1:]:
        ts, v, _ = row.split(",")
        cpu_series.append((datetime.fromisoformat(ts.replace("Z", "+00:00")), float(v)))
    cpu_t = first_run(cpu_series, lambda v: v > 80, 5)
    assert all(v > 5 for d, v in rate if d >= page_t), "page alarm must stay in ALARM through NOW"

    def alarm(name, ns, metric, dims, stat, op, thr, n, state, since, reason, history, **kw):
        return {"AlarmName": name, "Namespace": ns, "MetricName": metric, "Dimensions": dims, "Statistic": stat, "Period": 60,
                "EvaluationPeriods": n, "ComparisonOperator": op, "Threshold": thr, "StateValue": state,
                "StateUpdatedTimestamp": iso(since), "StateReason": reason, "History": history, **kw}
    alarms = [
        alarm("portal-api-5xx-rate-and-p99", "AWS/ApplicationELB", "5xxRatePct AND TargetResponseTime.p99", {"LoadBalancer": LB},
              "metric math", "GreaterThanThreshold", 5, 3, "ALARM", page_t,
              "3 datapoints: 100*(HTTPCode_Target_5XX_Count+HTTPCode_ELB_5XX_Count)/RequestCount > 5 AND TargetResponseTime p99 > 3 s",
              [{"Timestamp": iso(page_t), "From": "OK", "To": "ALARM"}],
              Expression="100*(HTTPCode_Target_5XX_Count+HTTPCode_ELB_5XX_Count)/RequestCount > 5 AND TargetResponseTime(p99) > 3"),
        alarm("rds-portal-prod-connections-high", "AWS/RDS", "DatabaseConnections", {"DBInstanceIdentifier": "portal-prod"},
              "Maximum", "GreaterThanThreshold", 270, 3, "ALARM", conn_t, "3 datapoints were greater than the threshold (270.0)",
              [{"Timestamp": iso(conn_t), "From": "OK", "To": "ALARM"}]),
        alarm("rds-portal-prod-cpu-high", "AWS/RDS", "CPUUtilization", {"DBInstanceIdentifier": "portal-prod"},
              "Average", "GreaterThanThreshold", 80, 5, "ALARM", cpu_t, "5 datapoints were greater than the threshold (80.0)",
              [{"Timestamp": iso(cpu_t), "From": "OK", "To": "ALARM"}]),
        alarm("acm-portal-cert-days-to-expiry", "AWS/CertificateManager", "DaysToExpiry", {"CertificateArn": f"arn:aws:acm:{REGION}:{ACCOUNT}:certificate/2f71c0a4-old"},
              "Minimum", "LessThanThreshold", 14, 1, "OK", hm(9, 39), "certificate replaced on the listener; the new certificate has 397 days left",
              [{"Timestamp": "2026-09-25T09:00:00Z", "From": "OK", "To": "ALARM"}, {"Timestamp": iso(hm(9, 39)), "From": "ALARM", "To": "OK"}]),
        alarm("portal-alb-tls-negotiation-errors", "AWS/ApplicationELB", "ClientTLSNegotiationErrorCount", {"LoadBalancer": LB},
              "Sum", "GreaterThanThreshold", 20, 3, "OK", START, "no datapoint above 20.0 in the snapshot window", []),
    ]
    wj(out / "alarms.json", alarms)
    wj(out / "meta.json", {"account": ACCOUNT, "region": REGION, "now": iso(NOW), "windowStart": iso(START),
                           "note": "All timestamps are UTC (ISO 8601). Metrics are one datapoint per minute. "
                                   "Request logs are sampled: every line carries sample_rate (1 line = sample_rate requests)."})

    # ---------------- app logs (sampled request lines)
    lrng = random.Random(11)
    hexid = lambda n=32: "".join(lrng.choice("0123456789abcdef") for _ in range(n))
    old_ids = [hexid() for _ in range(TASKS)]
    new_ids = [hexid() for _ in range(TASKS)]
    repl = {}
    for m, k in NEW_AT.items():
        for j in range(k - 3, k):
            repl[j] = hm(9, m)
    streams: dict[str, list] = {}

    def add(sid, ts, level, msg, **f):
        streams.setdefault(sid, []).append({"timestamp": iso(ts), "level": level, "message": msg, **f})

    for i, oid in enumerate(old_ids):
        add(f"app__{oid}", START, "INFO", f"db pool ready size={POOL} max_overflow=0 timeout=10s statement_timeout=30000ms",
            logger="portal.db", task=oid[:8], version=OLD_VER)
        add(f"app__{oid}", repl[i] + timedelta(seconds=50), "INFO", "SIGTERM received, draining connections", logger="portal.main", task=oid[:8], version=OLD_VER)
    for j, nid in enumerate(new_ids):
        t0 = repl[j] - timedelta(seconds=20)
        for k, (msg, lg) in enumerate([(f"starting portal-api {NEW_VER}", "portal.main"),
                                       ("feature flags loaded timeline_v2=true bulk_export=false", "portal.flags"),
                                       (f"db pool ready size={POOL} max_overflow=0 timeout=10s statement_timeout=30000ms", "portal.db")]):
            add(f"app__{nid}", t0 + timedelta(seconds=k), "INFO", msg, logger=lg, task=nid[:8], version=NEW_VER)
        if repl[j] < hm(9, 44):
            for s in (5, 25):
                add(f"app__{nid}", repl[j] + timedelta(seconds=s), "ERROR", "could not open pool connection", logger="portal.db",
                    error=SLOT, task=nid[:8], version=NEW_VER)

    def seg(d, phase):
        if phase == "pre":
            return d, min(d + timedelta(minutes=1), LOCK_ON)
        if phase == "A":
            return max(d, LOCK_ON), min(d + timedelta(minutes=1), LOCK_OFF)
        return max(d, LOCK_OFF), d + timedelta(minutes=1)

    for r in sim:
        d = r["d"]
        for route, group, phase, kind, cnt, med, sg in r["cats"]:
            slow = kind in ("503", "504", "500") or med >= 1000
            sr = 100 if slow else 1000
            n = int(cnt / sr + lrng.random())
            lo, hi = seg(d, phase)
            if kind == "404":
                lo, hi = max(d, WEB_DEPLOY_DONE), d + timedelta(minutes=1)
            span = max(1, int((hi - lo).total_seconds()))
            for _ in range(n):
                ts = lo + timedelta(seconds=lrng.randrange(span))
                alive_old = [x for k2, x in enumerate(old_ids) if ts < repl[k2] + timedelta(seconds=50)]
                alive_new = [x for k2, x in enumerate(new_ids) if ts >= repl[k2]]
                if kind == "404":                                   # only old tasks lack the route
                    use_new = False
                elif route == "timeline":
                    use_new = True
                else:
                    use_new = bool(alive_new) and (not alive_old or lrng.random() < r["f"])
                task = lrng.choice((alive_new if use_new else alive_old) or (new_ids if use_new else old_ids))
                ver = NEW_VER if use_new else OLD_VER
                tenant = "tn-orbit" if group == "orbit" else lrng.choice(OTHER_TENANTS)
                dur = med * math.exp(sg * lrng.gauss(0, 1))
                status = {"ok": 200, "401": 401, "404": 404, "503": 503, "504": 500, "500": 500}[kind]
                rec = dict(logger="portal.access", method="GET", route=PATH[route], status=status, duration_ms=round(dur, 1),
                           tenant=tenant, task=task[:8], version=ver, sample_rate=sr, request_id=hexid(16))
                lvl = "INFO"
                if kind == "503":
                    rec["error"], lvl = E503, "ERROR"
                elif kind == "504":
                    rec["error"], rec["client_disconnected"], lvl = E500, True, "ERROR"
                elif kind == "500":
                    rec["error"], lvl = "opensearchpy.exceptions.ConnectionTimeout: read timeout=5", "ERROR"
                elif dur >= 1000:
                    lvl = "WARN"
                # the app logs when the request finishes: a 504 is logged by the app at statement_timeout (30 s)
                add(f"app__{task}", min(ts + timedelta(milliseconds=dur), NOW), lvl, "request", **rec)
    lg = out / "cloudwatch" / "logs"
    for sid, recs in streams.items():
        write_jsonl(lg / "ecs__portal-api" / f"{sid}.jsonl", recs)

    # ---------------- migration task logs
    streams = {}
    mid = hexid()
    ms = f"migrate__{mid}"
    add(ms, hm(9, 40, 5), "INFO", f"starting migration runner {NEW_VER} mode=post-deploy-async timeout=720s", logger="migrate")
    add(ms, hm(9, 40, 6), "INFO", "applying 0142_alerts_timeline (transactional=true)", logger="migrate")
    add(ms, hm(9, 40, 7), "INFO", "BEGIN", logger="migrate.sql")
    add(ms, hm(9, 40, 7), "INFO", "ALTER TABLE alerts ADD COLUMN triage_note_id bigint -- ok (4 ms)", logger="migrate.sql")
    add(ms, hm(9, 40, 7), "INFO", "CREATE INDEX alerts_tenant_user_created_idx ON alerts (tenant_id, user_id, created_at DESC)", logger="migrate.sql")
    for k in range(1, 6):
        add(ms, hm(9, 40, 7) + timedelta(minutes=2 * k), "INFO", f"still running: CREATE INDEX alerts_tenant_user_created_idx (elapsed {120 * k}s)", logger="migrate")
    add(ms, hm(9, 52, 10), "WARN", "SIGTERM received: stopped by deploy pipeline (migration timeout 720s exceeded); closing connection", logger="migrate")
    write_jsonl(lg / "ecs__portal-api-migrate" / f"{ms}.jsonl", streams[ms])

    # ---------------- RDS postgres log
    streams = {}
    pg = "portal-prod"
    prng = random.Random(5)
    ips = [f"198.51.100.{x}" for x in range(20, 44)]

    def pgl(ts, level, msg, pid, user="portal", app="portal-api", **f):
        add(pg, ts, level, msg, logger="postgres", pid=pid, user=user, database="portal",
            client=f"{prng.choice(ips)}({prng.randint(40000, 60000)})", application_name=app, **f)
    for k in range(0, 70, 5):
        pgl(hm(8, 31) + timedelta(minutes=k), "LOG", "checkpoint complete: wrote 18213 buffers (0.9%); 0 WAL file(s) added, 0 removed, 12 recycled",
            pid=2177, user="rdsadmin", app="")
    pgl(hm(9, 12, 40), "LOG", "automatic vacuum of table \"portal.public.user_risk\": index scans: 1", pid=38821, user="rdsadmin", app="")
    pgl(hm(9, 40, 7), "LOG", "statement: BEGIN", pid=40117, user="migrator", app="portal-api-migrate")
    pgl(hm(9, 40, 7), "LOG", "statement: ALTER TABLE alerts ADD COLUMN triage_note_id bigint", pid=40117, user="migrator", app="portal-api-migrate")
    pgl(hm(9, 40, 7), "LOG", "statement: CREATE INDEX alerts_tenant_user_created_idx ON alerts (tenant_id, user_id, created_at DESC)",
        pid=40117, user="migrator", app="portal-api-migrate")
    t = hm(9, 40, 9)
    pid = 41200
    while t < LOCK_OFF:
        pid += prng.randint(1, 9)
        pgl(t, "LOG", f"process {pid} still waiting for AccessShareLock on relation 16421 of database 16401 after 1000.{prng.randint(100, 999)} ms",
            pid=pid, detail=f"Process holding the lock: 40117. Wait queue: {pid - 4}, {pid - 2}, {pid}.",
            statement=prng.choice([LIST_SQL, "SELECT id, kind, severity, status, payload FROM alerts WHERE tenant_id = $1 AND id = $2"]))
        if t >= hm(9, 40, 40) and prng.random() < .5:
            pgl(t + timedelta(seconds=2), "ERROR", "canceling statement due to statement timeout", pid=pid - 30,
                statement=prng.choice([LIST_SQL, TL_SQL]))
        t += timedelta(seconds=prng.randint(4, 7))
    for k in range(9):
        pgl(hm(9, 40, 31) + timedelta(seconds=23 * k), "FATAL", "remaining connection slots are reserved for non-replication superuser connections",
            pid=41000 + 13 * k)
    pgl(LOCK_OFF, "FATAL", "connection to client lost", pid=40117, user="migrator", app="portal-api-migrate",
        statement="CREATE INDEX alerts_tenant_user_created_idx ON alerts (tenant_id, user_id, created_at DESC)")
    pgl(LOCK_OFF, "LOG", f"process {pid + 3} acquired AccessShareLock on relation 16421 of database 16401 after 21877.402 ms", pid=pid + 3)
    t = LOCK_OFF + timedelta(seconds=3)
    n = 0
    while t <= NOW:
        n += 1
        user = f"u-{prng.randint(10000, 99999)}"
        dur = prng.uniform(6200, 14800)
        pgl(t, "LOG", f"duration: {dur:.3f} ms  execute <unnamed>: {TL_SQL}", pid=prng.randint(42000, 46000),
            detail=f"parameters: $1 = 'tn-orbit', $2 = '{user}'")
        if n % 4 == 0:
            pgl(t + timedelta(seconds=1), "ERROR", "canceling statement due to statement timeout", pid=prng.randint(42000, 46000),
                statement=TL_SQL, detail=f"parameters: $1 = 'tn-orbit', $2 = 'u-{prng.randint(10000, 99999)}'")
        if n % 12 == 1:
            removed = prng.randint(3_900_000, 4_400_000)
            pgl(t + timedelta(seconds=2), "LOG", f"duration: {dur + 310:.3f} ms  plan:\n"
                f"Query Text: {TL_SQL}\n"
                f"Limit  (cost=0.57..918734.21 rows=50 width=52) (actual time={dur - 5:.3f}..{dur + 300:.3f} rows=50 loops=1)\n"
                f"  Buffers: shared hit=21877 read={prng.randint(1_500_000, 1_700_000)}\n"
                f"  ->  Index Scan Backward using alerts_tenant_created_idx on alerts  (cost=0.57..71662117.80 rows=3901 width=52) (actual rows=50 loops=1)\n"
                f"        Index Cond: (tenant_id = 'tn-orbit'::text)\n"
                f"        Filter: (user_id = '{user}'::text)\n"
                f"        Rows Removed by Filter: {removed}",
                pid=prng.randint(42000, 46000), auto_explain=True)
        if n % 6 == 3:
            other = prng.choice(OTHER_TENANTS)
            pgl(t + timedelta(seconds=3), "LOG", f"duration: {prng.uniform(2100, 3900):.3f} ms  execute <unnamed>: {TL_SQL}",
                pid=prng.randint(42000, 46000), detail=f"parameters: $1 = '{other}', $2 = 'u-{prng.randint(10000, 99999)}'")
        t += timedelta(seconds=prng.randint(3, 6))
    write_jsonl(lg / "aws__rds__instance__portal-prod__postgresql" / f"{pg}.jsonl", streams[pg])

    # ---------------- cloudtrail
    ct = []

    def ev(ts, source, name, user, params=None, resp=None, ip="198.51.100.17", n=[0]):
        n[0] += 1
        ct.append({"eventVersion": "1.09", "eventTime": iso(ts), "eventSource": source, "eventName": name, "awsRegion": REGION,
                   "eventID": f"9b2c4d10-0000-4000-8000-{n[0]:012d}", "sourceIPAddress": ip,
                   "userIdentity": {"type": "AssumedRole" if user.startswith("role:") else "IAMUser", "userName": user.split(":", 1)[-1], "accountId": ACCOUNT},
                   "requestParameters": params or {}, "responseElements": resp or {}})
    new_cert = f"arn:aws:acm:{REGION}:{ACCOUNT}:certificate/9d03b6e8-new"
    old_cert = f"arn:aws:acm:{REGION}:{ACCOUNT}:certificate/2f71c0a4-old"
    lb_arn = f"arn:aws:elasticloadbalancing:{REGION}:{ACCOUNT}:loadbalancer/{LB}"
    listener = f"arn:aws:elasticloadbalancing:{REGION}:{ACCOUNT}:listener/{LB}/a1b2c3d4e5f60718"
    ev(hm(8, 50), "rds.amazonaws.com", "DescribeDBInstances", "role:monitoring-reader", {"dBInstanceIdentifier": "portal-prod"}, ip="203.0.113.40")
    ev(hm(9, 33, 10), "ecs.amazonaws.com", "UpdateService", "role:github-actions-deploy", {"cluster": "prod", "service": "portal-web", "taskDefinition": "portal-web:214"})
    ev(hm(9, 37, 50), "acm.amazonaws.com", "ImportCertificate", "ops-kim", {"domainName": "portal.example.com"}, {"certificateArn": new_cert}, ip="192.0.2.61")
    ev(hm(9, 38, 20), "elasticloadbalancing.amazonaws.com", "ModifyListener", "ops-kim",
       {"listenerArn": listener, "certificates": [{"certificateArn": new_cert}]}, {"listeners": [{"port": 443, "protocol": "HTTPS"}]}, ip="192.0.2.61")
    ev(hm(9, 39, 20), "ecs.amazonaws.com", "RegisterTaskDefinition", "role:github-actions-deploy",
       {"family": "portal-api", "containerDefinitions": [{"image": f"{ACCOUNT}.dkr.ecr.{REGION}.amazonaws.com/portal-api:{NEW_VER}"}]}, {"taskDefinition": {"revision": 88}})
    ev(hm(9, 39, 22), "ecs.amazonaws.com", "RegisterTaskDefinition", "role:github-actions-deploy",
       {"family": "portal-api-migrate", "containerDefinitions": [{"image": f"{ACCOUNT}.dkr.ecr.{REGION}.amazonaws.com/portal-api:{NEW_VER}", "command": ["migrate", "--timeout", "720"]}]},
       {"taskDefinition": {"revision": 88}})
    ev(DEPLOY, "ecs.amazonaws.com", "UpdateService", "role:github-actions-deploy", {"cluster": "prod", "service": "portal-api", "taskDefinition": "portal-api:88"})
    ev(hm(9, 40, 5), "ecs.amazonaws.com", "RunTask", "role:github-actions-deploy",
       {"cluster": "prod", "taskDefinition": "portal-api-migrate:88", "startedBy": "deploy-pipeline/portal-api#2291"},
       {"tasks": [{"taskArn": f"arn:aws:ecs:{REGION}:{ACCOUNT}:task/prod/{mid}"}]})
    ev(hm(9, 45, 30), "rds.amazonaws.com", "DescribeDBInstances", "oncall-ana", {"dBInstanceIdentifier": "portal-prod"}, ip="192.0.2.77")
    ev(hm(9, 47, 5), "rds.amazonaws.com", "DownloadDBLogFilePortion", "oncall-ana", {"dBInstanceIdentifier": "portal-prod", "logFileName": "error/postgresql.log"}, ip="192.0.2.77")
    ev(hm(9, 52, 10), "ecs.amazonaws.com", "StopTask", "role:github-actions-deploy",
       {"cluster": "prod", "task": mid, "reason": "Migration step exceeded 720s timeout (deploy-pipeline/portal-api#2291)"})
    ev(hm(9, 58, 40), "ecs.amazonaws.com", "DescribeServices", "oncall-ana", {"cluster": "prod", "services": ["portal-api"]}, ip="192.0.2.77")
    ct.sort(key=lambda e: e["eventTime"])
    (out / "cloudtrail").mkdir(parents=True, exist_ok=True)
    (out / "cloudtrail" / "events.jsonl").write_text("".join(json.dumps(e, separators=(",", ":")) + "\n" for e in ct))

    # ---------------- deploys
    img = lambda s, t: f"{ACCOUNT}.dkr.ecr.{REGION}.amazonaws.com/{s}:{t}"
    wj(out / "deploys.json", [
        {"service": "portal-api", "cluster": "prod", "id": "ecs-svc/7288", "startedAt": "2026-10-01T16:10:00Z", "completedAt": "2026-10-01T16:14:30Z", "status": "COMPLETED",
         "taskDefinition": "portal-api:87", "imageTag": OLD_VER, "image": img("portal-api", OLD_VER),
         "commit": {"sha": "c41d2a9", "author": "Priya Raman", "pr": 5107, "message": "paginate /api/v2/alerts with a keyset cursor"}},
        {"service": "portal-web", "cluster": "prod", "id": "ecs-svc/7301", "startedAt": "2026-10-02T09:33:10Z", "completedAt": iso(WEB_DEPLOY_DONE), "status": "COMPLETED",
         "taskDefinition": "portal-web:214", "imageTag": "2026.10.02-0933-9a0c3e1", "image": img("portal-web", "2026.10.02-0933-9a0c3e1"),
         "commit": {"sha": "9a0c3e1", "author": "Jonas Weber", "pr": 2876, "message": "user page: show alert timeline (calls GET /api/v2/users/{id}/timeline)"}},
        {"service": "portal-api", "cluster": "prod", "id": "ecs-svc/7304", "startedAt": iso(DEPLOY), "completedAt": "2026-10-02T09:44:10Z", "status": "COMPLETED",
         "taskDefinition": "portal-api:88", "previousTaskDefinition": "portal-api:87", "imageTag": NEW_VER, "image": img("portal-api", NEW_VER),
         "rollout": "ROLLING (min 100% / max 125%), health check GET /healthz (static, no DB)",
         "migrations": {"names": ["0142_alerts_timeline"], "mode": "post-deploy-async", "timeoutSeconds": 720, "task": "portal-api-migrate:88"},
         "commit": {"sha": "e7b05f1", "author": "Marta Silva", "pr": 5120,
                    "message": "add user alert timeline endpoint\n\nGET /api/v2/users/{id}/timeline behind flag timeline_v2 (default on).\n"
                               "Migration 0142 adds an alerts(tenant_id, user_id, created_at) index for it."}},
        {"service": "portal-api-migrate", "cluster": "prod", "id": "ecs-task/" + mid[:12], "type": "migration", "startedAt": "2026-10-02T09:40:05Z",
         "completedAt": "2026-10-02T09:52:10Z", "status": "FAILED", "taskDefinition": "portal-api-migrate:88", "imageTag": NEW_VER,
         "migration": "0142_alerts_timeline", "reason": "stopped by deploy pipeline: migration step exceeded 720s timeout",
         "commit": {"sha": "e7b05f1", "author": "Marta Silva", "pr": 5120, "message": "add user alert timeline endpoint"}},
    ])

    # ---------------- config before/after
    api_before = {"flags": {"bulk_export": False},
                  "db": {"pool_size": POOL, "max_overflow": 0, "pool_timeout_s": 10, "statement_timeout_ms": 30000},
                  "migrations": {"mode": "post-deploy-async", "timeout_s": 720, "transactional": True}}
    api_after = json.loads(json.dumps(api_before))
    api_after["flags"]["timeline_v2"] = True
    wj(out / "config" / "portal-api.before.json", api_before)
    wj(out / "config" / "portal-api.after.json", api_after)
    alb = {"listener": {"port": 443, "protocol": "HTTPS", "sslPolicy": "ELBSecurityPolicy-TLS13-1-2-2021-06", "certificateArn": old_cert},
           "attributes": {"idle_timeout.timeout_seconds": 15}, "targetGroup": {"healthCheckPath": "/healthz", "healthyThreshold": 2, "unhealthyThreshold": 3}}
    wj(out / "config" / "portal-alb.before.json", alb)
    alb2 = json.loads(json.dumps(alb))
    alb2["listener"]["certificateArn"] = new_cert
    wj(out / "config" / "portal-alb.after.json", alb2)
    params = {"max_connections": MAXCONN, "superuser_reserved_connections": 3, "statement_timeout": 0, "lock_timeout": 0,
              "deadlock_timeout": "1s", "log_lock_waits": 1, "log_min_duration_statement": 2000, "log_statement": "ddl",
              "client_connection_check_interval": 10000, "shared_preload_libraries": "pg_stat_statements,auto_explain",
              "auto_explain.log_min_duration": 5000}
    wj(out / "config" / "portal-pg15-params.before.json", params)
    wj(out / "config" / "portal-pg15-params.after.json", params)

    # ---------------- resources
    res = out / "resources"
    wj(res / "elbv2" / "portal-alb.json", {"LoadBalancers": [{"LoadBalancerArn": lb_arn, "DNSName": "portal-alb-1234567890.us-east-1.elb.example.com",
                                                             "Scheme": "internet-facing", "State": {"Code": "active"}, "Type": "application"}],
                                          "Listeners": [{"ListenerArn": listener, "Port": 443, "Protocol": "HTTPS", "Certificates": [{"CertificateArn": new_cert}],
                                                         "SslPolicy": "ELBSecurityPolicy-TLS13-1-2-2021-06"}],
                                          "Attributes": {"idle_timeout.timeout_seconds": "15"},
                                          "TargetGroups": [{"TargetGroupName": "portal-api", "HealthCheckPath": "/healthz", "Targets": 12, "HealthyTargets": 12}]})
    wj(res / "ecs" / "portal-api.json", {"services": [{"serviceName": "portal-api", "clusterArn": f"arn:aws:ecs:{REGION}:{ACCOUNT}:cluster/prod",
                                                      "status": "ACTIVE", "desiredCount": TASKS, "runningCount": TASKS, "launchType": "FARGATE",
                                                      "taskDefinition": "portal-api:88", "cpu": 1024, "memory": 2048,
                                                      "deployments": [{"status": "PRIMARY", "taskDefinition": "portal-api:88", "rolloutState": "COMPLETED",
                                                                       "createdAt": iso(DEPLOY), "updatedAt": "2026-10-02T09:44:10Z"}],
                                                      "deploymentConfiguration": {"minimumHealthyPercent": 100, "maximumPercent": 125},
                                                      "healthCheck": "GET /healthz (static 200; does not touch the database)",
                                                      "autoScaling": "target tracking on CPUUtilization 60%, min 12 max 24",
                                                      "dbPool": {"perTask": POOL, "maxOverflow": 0, "timeoutSeconds": 10}}]})
    wj(res / "ecs" / "portal-api-migrate.json", {"tasks": [{"taskArn": f"arn:aws:ecs:{REGION}:{ACCOUNT}:task/prod/{mid}", "taskDefinitionArn": "portal-api-migrate:88",
                                                           "lastStatus": "STOPPED", "startedAt": "2026-10-02T09:40:05Z", "stoppedAt": "2026-10-02T09:52:10Z",
                                                           "stopCode": "UserInitiated", "stoppedReason": "Migration step exceeded 720s timeout (deploy-pipeline/portal-api#2291)",
                                                           "containers": [{"name": "migrate", "exitCode": 143}]}]})
    wj(res / "rds" / "portal-prod.json", {"DBInstances": [{"DBInstanceIdentifier": "portal-prod", "Engine": "postgres", "EngineVersion": "15.7",
                                                           "DBInstanceClass": "db.r6g.2xlarge", "vCPU": 8, "DBInstanceStatus": "available", "MultiAZ": True,
                                                           "StorageType": "gp3", "AllocatedStorage": 2000, "Iops": 12000,
                                                           "DBParameterGroups": [{"DBParameterGroupName": "portal-pg15", "ParameterApplyStatus": "in-sync"}],
                                                           "PerformanceInsightsEnabled": True,
                                                           "note": "max_connections=300 comes from parameter group portal-pg15 (see: config show portal-pg15-params)"}]})
    wj(res / "pg" / "portal-prod.alerts.json", {
        "relation": "public.alerts", "oid": 16421, "database_oid": 16401, "n_live_tup": 182_400_000, "total_size": "214 GB",
        "columns": ["id bigint", "tenant_id text", "user_id text", "kind text", "severity smallint", "status text", "payload jsonb", "created_at timestamptz"],
        "indexes": [{"name": "alerts_pkey", "def": "UNIQUE btree (id)"},
                    {"name": "alerts_tenant_created_idx", "def": "btree (tenant_id, created_at DESC)"},
                    {"name": "alerts_tenant_status_created_idx", "def": "btree (tenant_id, status, created_at DESC, id DESC)"}],
        "rows_by_tenant_top": [{"tenant_id": "tn-orbit", "rows": 38_100_000}, {"tenant_id": "tn-kestrel", "rows": 9_400_000},
                               {"tenant_id": "tn-larch", "rows": 6_200_000}],
        "note": "snapshot of pg_class / pg_indexes / pg_stat_user_tables at 2026-10-02T10:05:00Z; column triage_note_id is absent"})
    wj(res / "pi" / "portal-prod.json", {"Identifier": "portal-prod", "MetricType": "db.load.avg", "vCPU": 8, "Windows": [
        {"Start": "2026-10-02T09:00:00Z", "End": "2026-10-02T09:40:00Z", "AvgLoad": 1.2,
         "TopWaits": [{"wait": "CPU", "load": 1.0}, {"wait": "IO:DataFileRead", "load": 0.15}],
         "TopSQL": [{"sql": LIST_SQL, "load": 0.5}, {"sql": "SELECT ... FROM user_risk WHERE tenant_id = $1 AND user_id = $2", "load": 0.2}]},
        {"Start": "2026-10-02T09:41:00Z", "End": "2026-10-02T09:52:00Z", "AvgLoad": 270,
         "TopWaits": [{"wait": "Lock:relation", "load": 266.8}, {"wait": "CPU", "load": 1.6}, {"wait": "IO:DataFileRead", "load": 1.2}],
         "TopSQL": [{"sql": LIST_SQL, "load": 118.0}, {"sql": "SELECT id, kind, severity, status, payload FROM alerts WHERE tenant_id = $1 AND id = $2", "load": 66.4},
                    {"sql": TL_SQL, "load": 30.9}, {"sql": "CREATE INDEX alerts_tenant_user_created_idx ON alerts (tenant_id, user_id, created_at DESC)", "load": 1.0}],
         "Blockers": [{"pid": 40117, "user": "migrator", "application_name": "portal-api-migrate", "state": "active",
                       "xact_start": "2026-10-02T09:40:07Z", "lock": "AccessExclusiveLock on relation 16421",
                       "query": "CREATE INDEX alerts_tenant_user_created_idx ON alerts (tenant_id, user_id, created_at DESC)", "blocked_sessions": 268}]},
        {"Start": "2026-10-02T09:53:00Z", "End": "2026-10-02T10:05:00Z", "AvgLoad": 38,
         "TopWaits": [{"wait": "IO:DataFileRead", "load": 27.9}, {"wait": "CPU", "load": 7.4}, {"wait": "Client:ClientRead", "load": 1.3}],
         "TopSQL": [{"sql": TL_SQL, "load": 31.2}, {"sql": LIST_SQL, "load": 4.1}], "Blockers": []},
    ]})
    wj(res / "migrations" / "0142_alerts_timeline.json", {
        "name": "0142_alerts_timeline", "transactional": True, "ranBy": "portal-api-migrate:88", "status": "ROLLED_BACK",
        "statements": ["ALTER TABLE alerts ADD COLUMN triage_note_id bigint;",
                       "CREATE INDEX alerts_tenant_user_created_idx ON alerts (tenant_id, user_id, created_at DESC);"],
        "applied": False, "note": "runner wraps each migration file in one transaction; connection lost at 2026-10-02T09:52:14Z, transaction rolled back"})

    page_rate = next(r["rate5xx"] for r in sim if r["d"] == page_t)
    return dict(page=iso(page_t), conn_alarm=iso(conn_t), cpu_alarm=iso(cpu_t), page_rate=round(page_rate, 1),
                rate_B_last=round(sim[-1]["rate5xx"], 1), p99_last=round(sim[-1]["trt_p99"], 2),
                log_lines=sum(len(p.read_text().splitlines()) for p in (out / "cloudwatch" / "logs").rglob("*.jsonl")))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=str(Path(__file__).resolve().parent / "env"))
    a = ap.parse_args()
    out = Path(a.out)
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    print(json.dumps(build(out), indent=1))


if __name__ == "__main__":
    main()
