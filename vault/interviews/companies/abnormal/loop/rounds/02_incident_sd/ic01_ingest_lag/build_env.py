#!/usr/bin/env python3
"""Deterministically (re)build env/ for ic01_ingest_lag.  Stdlib only; no clock, no network.

    python3 build_env.py [--out DIR]          # default: ./env

The numbers come from a small per-minute simulation (see simulate()), not from a hand-typed table, so the
metrics, logs, alarms and resource descriptions agree with each other.  Everything is UTC.
"""
from __future__ import annotations

import argparse
import csv
import json
import random
import shutil
from datetime import datetime, timedelta, timezone
from pathlib import Path

UTC = timezone.utc
DAY = datetime(2026, 9, 30, tzinfo=UTC)
START = DAY.replace(hour=12, minute=30)
NOW = DAY.replace(hour=14, minute=30)
DEPLOY = DAY.replace(hour=14, minute=2)
ACCOUNT, REGION = "111122223333", "us-east-1"

# model constants
PRODUCE = 150.0          # messages/s into security-events
OLD_RATE = 333.0         # msgs/s per task with batch+cache (~3 ms/msg)
ATTEMPT_MS = 150.0       # one synchronous geoip call (new TLS connection per call)
LIMIT_RPM = 1200         # geoip-svc per-client rate limit
MAX_ATTEMPTS = 5
TASKS = 8
NEW_TASKS_AT = {3: 2, 4: 4, 5: 6, 6: 8}   # minute-of-14:00 -> new tasks serving


def iso(d: datetime) -> str:
    return d.strftime("%Y-%m-%dT%H:%M:%SZ")


def minutes():
    d = START
    while d <= NOW:
        yield d
        d += timedelta(minutes=1)


def new_tasks(d: datetime) -> int:
    if d < DEPLOY:
        return 0
    k = 0
    for m, n in sorted(NEW_TASKS_AT.items()):
        if d >= DAY.replace(hour=14, minute=m):
            k = n
    return k


def simulate(rng: random.Random):
    """Per-minute model.  Partitions are spread evenly over the 8 consumers, so during the rolling deploy the
    k new (slow) tasks own k/8 of the partitions and their backlog grows while the old tasks keep up with theirs.
    When the last old task leaves, its (small) backlog moves to the new owners."""
    rows = []
    lag_old, lag_new = 240.0, 0.0
    dlq = 0.0
    for d in minutes():
        k = new_tasks(d)
        hour = (d - START).total_seconds() / 3600
        prod = PRODUCE + 6 * (hour / 2) + rng.uniform(-7, 7)
        demand = k * 60000 / ATTEMPT_MS * (1 + rng.uniform(-0.03, 0.03))   # attempts/min: every new task loops hot
        p = 1.0 if demand <= LIMIT_RPM else LIMIT_RPM / demand            # per-attempt success probability
        q = 1 - p
        avg_attempts = 1.0 if p == 1 else (1 - q ** MAX_ATTEMPTS) / p
        succ_frac = 1 - q ** MAX_ATTEMPTS
        new_msgs_s = (demand / avg_attempts / 60) if k else 0.0
        old_share = (TASKS - k) / TASKS
        old_in, new_in = prod * old_share, prod * (1 - old_share)
        if k == TASKS and lag_old:
            lag_new, lag_old = lag_new + lag_old, 0.0
        c_old = min((TASKS - k) * OLD_RATE, old_in + lag_old / 60) if k < TASKS else 0.0
        c_new = min(new_msgs_s, new_in + lag_new / 60)
        if k < TASKS:
            lag_old = max((200 + rng.uniform(-60, 90)) * old_share, lag_old + (old_in - c_old) * 60)
        lag_new = max(0.0, lag_new + (new_in - c_new) * 60)
        consumed = c_old + c_new
        lag = lag_old + lag_new
        dead = c_new * 60 * (1 - succ_frac) if k else 0.0
        dlq += dead
        throttled = demand * q
        new_share = (c_new / consumed) if consumed else 0
        lat_avg = (1 - new_share) * (3.0 + rng.uniform(-0.3, 0.3)) + new_share * (avg_attempts * ATTEMPT_MS + 3)
        lat_p99 = (9.0 + rng.uniform(-1.5, 1.5) if k == 0 else
                   MAX_ATTEMPTS * ATTEMPT_MS + 40 + rng.uniform(-15, 15) if q > 0 else 190.0 + rng.uniform(-10, 10))
        rows.append(dict(d=d, k=k, prod=prod, consumed=consumed, lag=lag, dlq=dlq, dead=dead, throttled=throttled,
                         attempts=demand, p=p, avg_attempts=avg_attempts, lat_avg=lat_avg, lat_p99=lat_p99,
                         new_msgs_s=c_new))
    return rows


def write_csv(out: Path, ns: str, name: str, rows: list[tuple], extra: str | None = None):
    d = out / "cloudwatch" / "metrics" / ns.replace("/", "_")
    d.mkdir(parents=True, exist_ok=True)
    with (d / f"{name}.csv").open("w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["timestamp", "value", "dimensions"] + ([extra] if extra else []))
        for r in rows:
            w.writerow([iso(r[0]), f"{r[1]:.2f}".rstrip("0").rstrip("."), r[2]] + ([f"{r[3]:.2f}".rstrip("0").rstrip(".")] if extra else []))


def write_jsonl(path: Path, recs: list[dict]):
    path.parent.mkdir(parents=True, exist_ok=True)
    recs = sorted((r for r in recs if r["timestamp"] <= iso(NOW)), key=lambda r: r["timestamp"])
    path.write_text("".join(json.dumps(r, separators=(",", ":")) + "\n" for r in recs))


def wj(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2) + "\n")


def first_run(rows, key, pred, n):
    """Timestamp of the n-th consecutive datapoint satisfying pred (alarm evaluation)."""
    run = 0
    for r in rows:
        run = run + 1 if pred(r[key]) else 0
        if run == n:
            return r["d"]
    return None


def build(out: Path):
    rng = random.Random(20260930)
    sim = simulate(rng)
    CL = "ClusterName=security-events-cluster"
    ENRICH = "Service=alert-ingest"
    LAG = f"ConsumerGroup=alert-ingest;Topic=security-events;{CL}"

    # ---- Kafka
    write_csv(out, "AWS/Kafka", "SumOffsetLag", [(r["d"], r["lag"], LAG) for r in sim])
    # age of the oldest unconsumed record ~ backlog / arrival rate (MSK: EstimatedMaxTimeLag, seconds)
    write_csv(out, "AWS/Kafka", "EstimatedMaxTimeLag", [(r["d"], r["lag"] / r["prod"], LAG) for r in sim])
    write_csv(out, "AWS/Kafka", "MessagesInPerSec", [(r["d"], r["prod"], f"Topic=security-events;{CL}") for r in sim])
    disk = []
    for d in minutes():
        mm = (d - START).total_seconds() / 60       # 0 = 12:30
        for b, base in ((1, 58.0), (2, 59.0), (3, 57.0)):
            v = base + rng.uniform(-0.4, 0.4) + (d - START).total_seconds() / 3600 * 0.6
            if b == 2:
                if 18 <= mm < 25:                    # 12:48-12:54 climbing
                    v += (mm - 17) * 4.0
                elif 25 <= mm < 31:                  # 12:55-13:00 plateau
                    v = 87.0 + rng.uniform(-0.5, 0.5)
                elif 31 <= mm < 34:                  # 13:01 storage grown 1000 -> 1500 GB, then settles
                    v = 87.0 * (1000 / 1500) + 1.0 + rng.uniform(-0.3, 0.3)
            disk.append((d, v, f"BrokerID={b};{CL}"))
    write_csv(out, "AWS/Kafka", "KafkaDataLogsDiskUsed", disk)
    b2 = [(d, v) for d, v, dims in disk if "BrokerID=2" in dims]

    # ---- ECS
    def cpu(r):
        return ((TASKS - r["k"]) * 38.0 + r["k"] * 7.0) / TASKS + rng.uniform(-1.5, 1.5)
    # geoip-svc CPU: 22% baseline, +load from the retry storm
    gcpu = [(r["d"], 22 + r["attempts"] * 0.006 + rng.uniform(-1, 1), "ClusterName=prod;ServiceName=geoip-svc") for r in sim]
    renderer = [(r["d"], (24 if r["d"] < DAY.replace(hour=14, minute=5) else 91) + rng.uniform(-2, 2),
                 "ClusterName=prod-batch;ServiceName=report-renderer") for r in sim]
    ingest_cpu = [(r["d"], cpu(r), "ClusterName=prod;ServiceName=alert-ingest") for r in sim]
    write_csv(out, "AWS/ECS", "CPUUtilization", ingest_cpu + gcpu + renderer)
    write_csv(out, "AWS/ECS", "MemoryUtilization", [(r["d"], 54 + rng.uniform(-1, 1) + 0.01 * (r["d"] - START).seconds / 60,
                                                    "ClusterName=prod;ServiceName=alert-ingest") for r in sim])
    running = []
    for r in sim:
        n = 8
        if DEPLOY <= r["d"] < DAY.replace(hour=14, minute=7):
            n = 10
        running.append((r["d"], n, "ClusterName=prod;ServiceName=alert-ingest"))
    write_csv(out, "ECS/ContainerInsights", "RunningTaskCount", running)

    # ---- app metrics
    write_csv(out, "Abnormal/AlertIngest", "ProcessedPerSec", [(r["d"], r["consumed"], ENRICH) for r in sim])
    write_csv(out, "Abnormal/AlertIngest", "EnrichLatencyMs", [(r["d"], r["lat_avg"], ENRICH, r["lat_p99"]) for r in sim], "p99")
    write_csv(out, "Abnormal/AlertIngest", "GeoipRequestCount", [(r["d"], (18 * (TASKS - r["k"]) / TASKS if r["k"] < TASKS else 0) + r["attempts"] + rng.uniform(0, 3), ENRICH) for r in sim])
    write_csv(out, "Abnormal/AlertIngest", "Geoip429Count", [(r["d"], r["throttled"], ENRICH) for r in sim])
    write_csv(out, "AWS/SQS", "ApproximateNumberOfMessagesVisible", [(r["d"], r["dlq"], "QueueName=security-events-dlq") for r in sim])
    write_csv(out, "AWS/SQS", "NumberOfMessagesSent", [(r["d"], r["dead"], "QueueName=security-events-dlq") for r in sim])
    # geoip-svc (server side): healthy, just rate-limiting one client
    write_csv(out, "Abnormal/GeoipSvc", "RequestCount", [(r["d"], (18 * (TASKS - r["k"]) / TASKS) + r["attempts"] + rng.uniform(0, 3), "Client=alert-ingest") for r in sim] +
              [(r["d"], 310 + rng.uniform(-25, 25), "Client=risk-engine") for r in sim])
    write_csv(out, "Abnormal/GeoipSvc", "ThrottledCount", [(r["d"], r["throttled"], "Client=alert-ingest") for r in sim] +
              [(r["d"], 0, "Client=risk-engine") for r in sim])
    write_csv(out, "Abnormal/GeoipSvc", "Http5xxCount", [(r["d"], 0, "Service=geoip-svc") for r in sim])
    write_csv(out, "Abnormal/GeoipSvc", "ServerLatencyMs", [(r["d"], 11 + rng.uniform(-1, 1), "Service=geoip-svc", 38 + rng.uniform(-3, 3)) for r in sim], "p99")

    # ---- RDS (alerts-prod): idle, not the bottleneck
    db = "DBInstanceIdentifier=alerts-prod"
    write_csv(out, "AWS/RDS", "CPUUtilization", [(r["d"], 6 + 16 * r["consumed"] / r["prod"] if r["consumed"] < r["prod"] else 22 + rng.uniform(-2, 2), db) for r in sim])
    write_csv(out, "AWS/RDS", "DatabaseConnections", [(r["d"], 64 + rng.choice([-1, 0, 0, 1]), db) for r in sim])
    write_csv(out, "AWS/RDS", "WriteIOPS", [(r["d"], 1800 * min(1.0, r["consumed"] / r["prod"]) + rng.uniform(-60, 60), db) for r in sim])
    write_csv(out, "AWS/RDS", "WriteLatency", [(r["d"], 0.0012 + rng.uniform(-0.0001, 0.0001), db) for r in sim])

    # ---- alarms
    lag_t = first_run(sim, "lag", lambda v: v > 50000, 10)
    cross = first_run(sim, "lag", lambda v: v > 50000, 1)
    rend_t = first_run([dict(d=d, v=v) for d, v, dims in renderer], "v", lambda v: v > 85, 3)
    b2_hi = first_run([dict(d=d, v=v) for d, v in b2], "v", lambda v: v > 80, 3)
    b2_ok = None
    seen_hi = False
    for d, v in b2:
        seen_hi = seen_hi or v > 80
        if seen_hi and v <= 80:
            b2_ok = d
            break
    last = sim[-1]

    def alarm(name, ns, metric, dims, stat, op, thr, n, state, since, reason, history, **kw):
        return {"AlarmName": name, "Namespace": ns, "MetricName": metric, "Dimensions": dims, "Statistic": stat, "Period": 60,
                "EvaluationPeriods": n, "ComparisonOperator": op, "Threshold": thr, "StateValue": state,
                "StateUpdatedTimestamp": iso(since), "StateReason": reason, "History": history, **kw}
    alarms = [
        alarm("alert-ingest-consumer-lag-high", "AWS/Kafka", "SumOffsetLag",
              {"ConsumerGroup": "alert-ingest", "Topic": "security-events", "ClusterName": "security-events-cluster"},
              "Maximum", "GreaterThanThreshold", 50000, 10, "ALARM", lag_t,
              "10 datapoints were greater than the threshold (50000.0)",
              [{"Timestamp": iso(lag_t), "From": "OK", "To": "ALARM"}]),
        alarm("report-renderer-cpu-high", "AWS/ECS", "CPUUtilization", {"ClusterName": "prod-batch", "ServiceName": "report-renderer"},
              "Average", "GreaterThanThreshold", 85, 3, "ALARM", rend_t, "3 datapoints were greater than the threshold (85.0)",
              [{"Timestamp": iso(rend_t), "From": "OK", "To": "ALARM"}]),
        alarm("msk-broker-2-disk-high", "AWS/Kafka", "KafkaDataLogsDiskUsed", {"BrokerID": "2", "ClusterName": "security-events-cluster"},
              "Maximum", "GreaterThanThreshold", 80, 3, "OK", b2_ok, "Threshold Crossed: 1 datapoint was not greater than the threshold (80.0)",
              [{"Timestamp": iso(b2_hi), "From": "OK", "To": "ALARM"}, {"Timestamp": iso(b2_ok), "From": "ALARM", "To": "OK"}]),
        alarm("alerts-prod-rds-cpu-high", "AWS/RDS", "CPUUtilization", {"DBInstanceIdentifier": "alerts-prod"},
              "Average", "GreaterThanThreshold", 80, 5, "OK", START, "no datapoint above 80.0 in the snapshot window", []),
        alarm("geoip-svc-5xx-high", "Abnormal/GeoipSvc", "Http5xxCount", {"Service": "geoip-svc"},
              "Sum", "GreaterThanThreshold", 50, 3, "OK", START, "no datapoint above 50.0 (note: HTTP 429 is not a 5xx; there is no alarm on ThrottledCount)", []),
    ]
    wj(out / "alarms.json", alarms)
    wj(out / "meta.json", {"account": ACCOUNT, "region": REGION, "now": iso(NOW), "windowStart": iso(START),
                           "note": "All timestamps are UTC (ISO 8601). Metrics are one datapoint per minute."})

    # ---- logs
    rid = random.Random(7)
    hexid = lambda: "".join(rid.choice("0123456789abcdef") for _ in range(32))
    old_ids = [hexid() for _ in range(TASKS)]
    new_ids = [hexid() for _ in range(TASKS)]
    gids = [hexid() for _ in range(3)]
    lg = out / "cloudwatch" / "logs"
    repl_at = {}                      # old task i replaced when its pair of new tasks come up
    for m, n in NEW_TASKS_AT.items():
        for j in range(n - 2, n):
            repl_at[j] = DAY.replace(hour=14, minute=m)
    streams: dict[str, list[dict]] = {}

    def add(sid, ts, level, msg, **f):
        streams.setdefault(sid, []).append({"timestamp": iso(ts), "level": level, "logger": f.pop("logger", "ingest"), "message": msg, **f})

    for i, oid in enumerate(old_ids):
        sid = f"app__{oid}"
        end = repl_at[i]
        add(sid, START, "INFO", "geoip client mode=batch cache=lru ttl=3600s batch_size=500 backoff_ms=250 jitter=true",
            logger="ingest.geoip", version="2026.09.29-1640-5e1d9b2")
        for r in sim:
            if r["d"] < end:
                add(sid, r["d"] + timedelta(seconds=rng.randint(0, 40)), "INFO", "consumed batch",
                    logger="ingest.consumer", records=int(r["prod"] * 60 / TASKS * (1 + rng.uniform(-.05, .05))),
                    enrich_ms_avg=round(3 + rng.uniform(-.6, .6), 1), partitions=[i % 12, (i + 8) % 12] if i < 4 else [i % 12])
        add(sid, end + timedelta(seconds=10), "INFO", "SIGTERM received, draining and committing offsets", logger="ingest.main")
    for j, nid in enumerate(new_ids):
        sid = f"app__{nid}"
        start = repl_at[j] - timedelta(seconds=25)
        add(sid, start, "INFO", "starting alert-ingest 2026.09.30-1402-a91f3c7", logger="ingest.main", version="2026.09.30-1402-a91f3c7")
        add(sid, start + timedelta(seconds=2), "INFO", "geoip client mode=sync cache=none batch_size=1 backoff_ms=0 jitter=false",
            logger="ingest.geoip", version="2026.09.30-1402-a91f3c7")
        for r in sim:
            if r["d"] < repl_at[j]:
                continue
            k = r["k"]
            per_task_msgs = r["new_msgs_s"] * 60 / k
            add(sid, r["d"] + timedelta(seconds=rng.randint(0, 9)), "INFO", "consumed batch", logger="ingest.consumer",
                records=int(per_task_msgs), enrich_ms_avg=round(r["avg_attempts"] * ATTEMPT_MS + 3, 1))
            if r["throttled"] > 0:
                per_task_429 = r["throttled"] / k
                per_task_dead = r["dead"] / k
                for s in range(6):                              # rate-limited logger: one line / 10 s, with a suppressed count
                    ts = r["d"] + timedelta(seconds=10 * s + rng.randint(0, 6))
                    sup = int(per_task_429 / 6)
                    att, el = rng.randint(1, MAX_ATTEMPTS), rng.randint(131, 170)
                    add(sid, ts, "WARN", f"geoip lookup throttled status=429 attempt={att} elapsed_ms={el} retry_in_ms=0 (suppressed {sup} similar in last 10s)",
                        logger="ingest.geoip", status=429, attempt=att, elapsed_ms=el, retry_in_ms=0, suppressed=sup)
                    if per_task_dead >= 1:
                        sup = int(per_task_dead / 6)
                        add(sid, ts + timedelta(seconds=1), "ERROR", f"enrichment failed after {MAX_ATTEMPTS} attempts, message sent to DLQ topic=security-events partition={rng.randint(0, 11)} (suppressed {sup} similar in last 10s)",
                            logger="ingest.consumer", attempts=MAX_ATTEMPTS, dlq="security-events-dlq", suppressed=sup)
    for sid, recs in streams.items():          # structured logs carry the image version and the task id on every line
        ver = "2026.09.30-1402-a91f3c7" if sid[5:] in new_ids else "2026.09.29-1640-5e1d9b2"
        for rec in recs:
            rec.setdefault("version", ver)
            rec.setdefault("task", sid[5:13])
        write_jsonl(lg / "ecs__alert-ingest" / f"{sid}.jsonl", recs)

    streams = {}
    for gi, gid in enumerate(gids):
        sid = f"app__{gid}"
        add(sid, START, "INFO", "loaded rate limit config client=alert-ingest limit_rpm=1200 client=risk-engine limit_rpm=1200",
            logger="geoip.config")
        for r in sim:
            add(sid, r["d"] + timedelta(seconds=gi * 3 + 5), "INFO", "stats", logger="geoip.stats",
                rps_alert_ingest=round((18 * (TASKS - r["k"]) / TASKS + r["attempts"]) / 60 / 3, 1), p99_ms=38)
            if r["throttled"] > 0:
                for s in range(6):
                    sup = int(r["throttled"] / 3 / 6)
                    add(sid, r["d"] + timedelta(seconds=10 * s + gi + 2), "WARN",
                        f"rate limit exceeded client=alert-ingest limit_rpm=1200 status=429 (suppressed {sup} similar in last 10s)",
                        logger="geoip.ratelimit", client="alert-ingest", status=429, suppressed=sup)
    for sid, recs in streams.items():
        write_jsonl(lg / "ecs__geoip-svc" / f"{sid}.jsonl", recs)

    streams = {}
    rr = f"app__{hexid()}"
    add(rr, DAY.replace(hour=13, minute=58, second=50), "INFO", "starting report-renderer 2026.09.30-1358-b07c4de", logger="renderer.main")
    for r in sim:
        if r["d"] >= DAY.replace(hour=14, minute=5):
            add(rr, r["d"] + timedelta(seconds=15), "WARN", "job monthly-pdf-export running in-process, cpu-bound, 41 pages/min", logger="renderer.jobs", job="monthly-pdf-export")
    write_jsonl(lg / "ecs__report-renderer" / f"{rr}.jsonl", streams[rr])

    streams = {}
    bsid = "broker-2"
    add(bsid, DAY.replace(hour=12, minute=50), "WARN", "log dir /kafka/data usage 71%: retention.bytes backlog on __consumer_offsets-14 and security-events-7", logger="kafka.log")
    add(bsid, DAY.replace(hour=12, minute=55), "WARN", "log dir /kafka/data usage 87%: segment cleaner behind (compaction of __consumer_offsets)", logger="kafka.log")
    add(bsid, DAY.replace(hour=13, minute=1, second=10), "INFO", "storage volume resize 1000 GiB -> 1500 GiB requested via UpdateBrokerStorage", logger="kafka.ops")
    add(bsid, DAY.replace(hour=13, minute=5), "INFO", "log dir /kafka/data usage 59% after volume resize and segment cleanup", logger="kafka.log")
    write_jsonl(lg / "aws__msk__broker-2" / "broker-2.jsonl", streams[bsid])

    # ---- cloudtrail
    ct = []

    def ev(ts, source, name, user, params=None, resp=None, ip="198.51.100.17", n=[0]):
        n[0] += 1
        ct.append({"eventVersion": "1.09", "eventTime": iso(ts), "eventSource": source, "eventName": name, "awsRegion": REGION,
                   "eventID": f"6d1e0f2a-0000-4000-8000-{n[0]:012d}", "sourceIPAddress": ip,
                   "userIdentity": {"type": "AssumedRole" if user.startswith("role:") else "IAMUser", "userName": user.split(":", 1)[-1],
                                    "accountId": ACCOUNT},
                   "requestParameters": params or {}, "responseElements": resp or {}})
    ev(DAY.replace(hour=12, minute=41), "ecs.amazonaws.com", "DescribeServices", "role:monitoring-reader", {"cluster": "prod"}, ip="203.0.113.40")
    ev(DAY.replace(hour=13, minute=1, second=5), "kafka.amazonaws.com", "UpdateBrokerStorage", "ops-dana",
       {"clusterArn": f"arn:aws:kafka:{REGION}:{ACCOUNT}:cluster/security-events-cluster/6a1f", "targetBrokerEBSVolumeInfo": [{"kafkaBrokerNodeId": "2", "volumeSizeGB": 1500}]},
       {"clusterOperationArn": f"arn:aws:kafka:{REGION}:{ACCOUNT}:cluster-operation/security-events-cluster/6a1f/op-91"}, ip="192.0.2.55")
    ev(DAY.replace(hour=13, minute=58, second=30), "ecs.amazonaws.com", "RegisterTaskDefinition", "role:github-actions-deploy",
       {"family": "report-renderer", "containerDefinitions": [{"image": f"{ACCOUNT}.dkr.ecr.{REGION}.amazonaws.com/report-renderer:2026.09.30-1358-b07c4de"}]},
       {"taskDefinition": {"revision": 112}})
    ev(DAY.replace(hour=13, minute=58, second=41), "ecs.amazonaws.com", "UpdateService", "role:github-actions-deploy",
       {"cluster": "prod-batch", "service": "report-renderer", "taskDefinition": "report-renderer:112"})
    ev(DAY.replace(hour=14, minute=1, second=48), "ecs.amazonaws.com", "RegisterTaskDefinition", "role:github-actions-deploy",
       {"family": "alert-ingest", "containerDefinitions": [{"image": f"{ACCOUNT}.dkr.ecr.{REGION}.amazonaws.com/alert-ingest:2026.09.30-1402-a91f3c7"}]},
       {"taskDefinition": {"revision": 57}})
    ev(DAY.replace(hour=14, minute=2, second=3), "ecs.amazonaws.com", "UpdateService", "role:github-actions-deploy",
       {"cluster": "prod", "service": "alert-ingest", "taskDefinition": "alert-ingest:57", "desiredCount": 8})
    ev(DAY.replace(hour=14, minute=11), "ecs.amazonaws.com", "DescribeServices", "role:monitoring-reader", {"cluster": "prod-batch"}, ip="203.0.113.40")
    ev(DAY.replace(hour=14, minute=24, second=30), "ecs.amazonaws.com", "DescribeServices", "oncall-sam", {"cluster": "prod", "services": ["alert-ingest"]}, ip="192.0.2.77")
    ct.sort(key=lambda e: e["eventTime"])
    (out / "cloudtrail").mkdir(parents=True, exist_ok=True)
    (out / "cloudtrail" / "events.jsonl").write_text("".join(json.dumps(e, separators=(",", ":")) + "\n" for e in ct))

    # ---- deploys
    img = lambda s, t: f"{ACCOUNT}.dkr.ecr.{REGION}.amazonaws.com/{s}:{t}"
    deploys = [
        {"service": "alert-ingest", "cluster": "prod", "id": "ecs-svc/4401", "startedAt": "2026-09-28T12:15:00Z", "completedAt": "2026-09-28T12:21:10Z", "status": "COMPLETED",
         "taskDefinition": "alert-ingest:55", "imageTag": "2026.09.28-1215-3c8e2f0", "image": img("alert-ingest", "2026.09.28-1215-3c8e2f0"),
         "commit": {"sha": "3c8e2f0", "author": "Mateo Okafor", "pr": 4163, "message": "bump kafka-python to 2.0.4"}},
        {"service": "alert-ingest", "cluster": "prod", "id": "ecs-svc/4409", "startedAt": "2026-09-29T16:40:00Z", "completedAt": "2026-09-29T16:46:20Z", "status": "COMPLETED",
         "taskDefinition": "alert-ingest:56", "imageTag": "2026.09.29-1640-5e1d9b2", "image": img("alert-ingest", "2026.09.29-1640-5e1d9b2"),
         "commit": {"sha": "5e1d9b2", "author": "Lena Fischer", "pr": 4171, "message": "add dlq headers (original topic/partition/offset)"}},
        {"service": "alert-ingest", "cluster": "prod", "id": "ecs-svc/4417", "startedAt": "2026-09-30T14:02:03Z", "completedAt": "2026-09-30T14:07:20Z", "status": "COMPLETED",
         "taskDefinition": "alert-ingest:57", "previousTaskDefinition": "alert-ingest:56", "imageTag": "2026.09.30-1402-a91f3c7", "image": img("alert-ingest", "2026.09.30-1402-a91f3c7"),
         "rollout": "ROLLING (min 100% / max 200%), health check GET /healthz only, circuit breaker enabled, no canary gate",
         "commit": {"sha": "a91f3c7", "author": "Mateo Okafor", "pr": 4182, "message": "simplify geoip client\n\nDrop the LRU cache and the batch lookup; call /v1/lookup once per record. Less code, one code path."}},
        {"service": "geoip-svc", "cluster": "prod", "id": "ecs-svc/3920", "startedAt": "2026-09-17T10:30:00Z", "completedAt": "2026-09-17T10:34:00Z", "status": "COMPLETED",
         "taskDefinition": "geoip-svc:31", "imageTag": "2026.09.17-1030-0d44a6e", "image": img("geoip-svc", "2026.09.17-1030-0d44a6e"),
         "commit": {"sha": "0d44a6e", "author": "Ravi Menon", "pr": 977, "message": "update MaxMind mmdb to 2026-09"}},
        {"service": "report-renderer", "cluster": "prod-batch", "id": "ecs-svc/880", "startedAt": "2026-09-30T13:58:41Z", "completedAt": "2026-09-30T14:00:10Z", "status": "COMPLETED",
         "taskDefinition": "report-renderer:112", "imageTag": "2026.09.30-1358-b07c4de", "image": img("report-renderer", "2026.09.30-1358-b07c4de"),
         "commit": {"sha": "b07c4de", "author": "Ines Duarte", "pr": 2210, "message": "render monthly PDFs in-process instead of shelling out to wkhtmltopdf"}},
    ]
    wj(out / "deploys.json", deploys)

    # ---- config before/after
    before = {"consumer": {"group_id": "alert-ingest", "max_poll_records": 500, "topic": "security-events"},
              "geoip": {"url": "https://geoip-svc.internal.example.com", "mode": "batch", "batch_size": 500, "cache": "lru",
                        "cache_ttl_s": 3600, "max_attempts": 5, "backoff_ms": 250, "jitter": True, "timeout_ms": 2000}}
    after = {"consumer": dict(before["consumer"]),
             "geoip": {"url": "https://geoip-svc.internal.example.com", "mode": "sync", "batch_size": 1, "cache": "none",
                       "max_attempts": 5, "backoff_ms": 0, "jitter": False, "timeout_ms": 2000}}
    wj(out / "config" / "alert-ingest.before.json", before)
    wj(out / "config" / "alert-ingest.after.json", after)
    gs = {"ratelimit": {"per_client_rpm": {"alert-ingest": 1200, "risk-engine": 1200}, "response": 429}, "mmdb": "2026-09"}
    wj(out / "config" / "geoip-svc.before.json", gs)
    wj(out / "config" / "geoip-svc.after.json", gs)

    # ---- resources
    res = out / "resources"
    wj(res / "msk" / "security-events-cluster.json", {
        "ClusterInfo": {"ClusterName": "security-events-cluster", "State": "ACTIVE", "ClusterArn": f"arn:aws:kafka:{REGION}:{ACCOUNT}:cluster/security-events-cluster/6a1f",
                        "BrokerNodeGroupInfo": {"InstanceType": "kafka.m5.large", "ClientSubnets": 3, "StorageInfo": {"EbsStorageInfo": {"VolumeSize": 1500}}},
                        "NumberOfBrokerNodes": 3, "CreationTime": "2025-11-04T09:12:00Z"},
        "Topics": [{"Name": "security-events", "Partitions": 12, "ReplicationFactor": 3, "RetentionHours": 72}],
        "ConsumerGroups": [{"GroupId": "alert-ingest", "State": "Stable", "Members": 8, "AssignedPartitions": 12}]})
    svc = lambda name, cluster, rev, cpu_, mem, launch, extra=None: {"services": [dict({
        "serviceName": name, "clusterArn": f"arn:aws:ecs:{REGION}:{ACCOUNT}:cluster/{cluster}", "status": "ACTIVE", "desiredCount": 8 if name == "alert-ingest" else 3,
        "runningCount": 8 if name == "alert-ingest" else 3, "launchType": launch, "taskDefinition": f"{name}:{rev}",
        "cpu": cpu_, "memory": mem}, **(extra or {}))]}
    wj(res / "ecs" / "alert-ingest.json", svc("alert-ingest", "prod", 57, 1024, 2048, "FARGATE", {
        "deployments": [{"status": "PRIMARY", "taskDefinition": "alert-ingest:57", "rolloutState": "COMPLETED", "createdAt": "2026-09-30T14:02:03Z", "updatedAt": "2026-09-30T14:07:20Z"}],
        "deploymentConfiguration": {"minimumHealthyPercent": 100, "maximumPercent": 200, "deploymentCircuitBreaker": {"enable": True, "rollback": True}},
        "healthCheck": "GET /healthz (process alive; does not look at consumer lag or enrichment errors)", "autoScaling": "none (fixed 8 tasks)"}))
    wj(res / "ecs" / "geoip-svc.json", svc("geoip-svc", "prod", 31, 1024, 2048, "FARGATE", {"autoScaling": "target tracking CPU 60%, min 3 max 6", "note": "per-client rate limit lives in config (see: config show geoip-svc)"}))
    wj(res / "ecs" / "report-renderer.json", svc("report-renderer", "prod-batch", 112, 2048, 4096, "FARGATE", {"note": "separate cluster, separate Fargate tasks: no CPU shared with prod"}))
    wj(res / "rds" / "alerts-prod.json", {"DBInstances": [{"DBInstanceIdentifier": "alerts-prod", "Engine": "postgres", "EngineVersion": "15.7", "DBInstanceClass": "db.r6g.xlarge",
                                                           "DBInstanceStatus": "available", "MultiAZ": True, "AllocatedStorage": 1000}]})
    wj(res / "sqs" / "security-events-dlq.json", {"Attributes": {"QueueName": "security-events-dlq", "ApproximateNumberOfMessages": int(round(last["dlq"])),
                                                                  "MessageRetentionPeriod": 1209600, "note": "application-level DLQ: the consumer publishes enrichment failures here"}})

    summary = dict(lag_cross_50k=iso(cross), lag_alarm=iso(lag_t), renderer_alarm=iso(rend_t), b2_alarm=iso(b2_hi), b2_ok=iso(b2_ok),
                   final_lag=round(last["lag"]), final_dlq=round(last["dlq"]), consumed_after=round(last["consumed"], 1))
    return summary


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
