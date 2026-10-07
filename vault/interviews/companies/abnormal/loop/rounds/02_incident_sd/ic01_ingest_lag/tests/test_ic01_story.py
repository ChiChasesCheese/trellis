"""The snapshot must support the story: the root-cause evidence is really in env/, the red herrings are really benign,
and every timestamp is UTC ISO 8601."""
from __future__ import annotations

import json
import re

import pytest

from ic01_helpers import ENV, ISO_ANY, ISO_OK, at, awsim, q, series, window_vals

KAFKA = ["--dim", "ConsumerGroup=alert-ingest", "--dim", "Topic=security-events", "--dim", "ClusterName=security-events-cluster"]
LAG = lambda **kw: series("AWS/Kafka", "SumOffsetLag", "Maximum", ["ConsumerGroup=alert-ingest", "Topic=security-events", "ClusterName=security-events-cluster"], **kw)
DAY = "2026-09-30"
NOW = f"{DAY}T14:30:00Z"


# ---------------------------------------------------------------- timestamps
def all_text_files():
    return [p for p in ENV.rglob("*") if p.is_file()]


def test_every_timestamp_literal_is_utc_iso8601_with_seconds():
    bad = []
    for p in all_text_files():
        for m in ISO_ANY.finditer(p.read_text()):
            if not ISO_OK.fullmatch(m.group(0)):
                bad.append((p.name, m.group(0)))
    assert not bad, bad[:5]


def test_meta_and_time_ranges():
    meta = awsim.meta()
    assert meta["now"] == NOW and meta["windowStart"] == f"{DAY}T12:30:00Z"
    lo, hi = meta["windowStart"], meta["now"]
    for p in (ENV / "cloudwatch" / "metrics").rglob("*.csv"):
        stamps = [l.split(",")[0] for l in p.read_text().splitlines()[1:]]
        assert stamps and min(stamps) >= lo and max(stamps) <= hi, p
        assert stamps == sorted(stamps) or len({s for s in stamps}) < len(stamps)   # sorted per dimension set, interleaved sets repeat
    for p in (ENV / "cloudwatch" / "logs").rglob("*.jsonl"):
        for line in p.read_text().splitlines():
            t = json.loads(line)["timestamp"]
            assert lo <= t <= hi, (p, t)
    for e in q("trail", "lookup")["Events"]:
        assert lo <= e["EventTime"] <= hi
    for d in q("deploys")["deployments"]:
        assert d["startedAt"] <= hi and d["completedAt"] <= hi and d["startedAt"] < d["completedAt"]
    for a in q("alarms", "--history")["MetricAlarms"]:
        assert lo <= a["StateUpdatedTimestamp"] <= hi
        for h in a["History"]:
            assert lo <= h["Timestamp"] <= hi


def test_metrics_have_one_datapoint_per_minute_per_dimension_set():
    for p in (ENV / "cloudwatch" / "metrics").rglob("*.csv"):
        seen = {}
        for line in p.read_text().splitlines()[1:]:
            ts, _, dims = line.split(",")[:3]
            seen.setdefault(dims, []).append(ts)
        for dims, ts in seen.items():
            assert len(ts) == 121 and len(set(ts)) == 121, (p.name, dims)


# ---------------------------------------------------------------- root cause evidence
def test_the_deploy_is_at_1402_and_its_commit_says_simplify_geoip_client():
    d = [x for x in q("deploys", "--service", "alert-ingest")["deployments"] if x["startedAt"] == f"{DAY}T14:02:03Z"]
    assert len(d) == 1 and "simplify geoip client" in d[0]["commit"]["message"] and d[0]["status"] == "COMPLETED"
    ct = q("trail", "lookup", "--event-name", "UpdateService", "--start", "14:00", "--end", "14:05")["Events"]
    assert [e["CloudTrailEvent"]["requestParameters"]["service"] for e in ct] == ["alert-ingest"]


def test_config_diff_shows_batch_cache_and_backoff_removed():
    diff = q("config", "diff", "alert-ingest")
    assert diff["changed"]["geoip.mode"] == {"before": "batch", "after": "sync"}
    assert diff["changed"]["geoip.cache"]["after"] == "none" and diff["changed"]["geoip.backoff_ms"]["after"] == 0
    assert diff["removed"] == {"geoip.cache_ttl_s": 3600}


def test_lag_is_flat_until_the_deploy_then_grows_linearly():
    lag = LAG()
    assert max(window_vals(lag, "12:30", "14:03")) < 1000
    assert 1000 < at(lag, "14:03") < at(lag, "14:04") < at(lag, "14:05")    # grows from the first new task on (its partitions)
    assert at(lag, "14:10") > 50000 and at(lag, "14:09") <= 50000          # first minute over the threshold
    assert at(lag, "14:30") > 150000
    growth = [at(lag, f"14:{m + 1}") - at(lag, f"14:{m}") for m in range(10, 29)]
    assert all(6500 < g < 8500 for g in growth), growth                    # ~ (produce - consume) * 60, i.e. linear


def test_lag_alarm_matches_ten_minutes_over_threshold():
    a = q("alarms", "--name", "alert-ingest-consumer-lag-high", "--history")["MetricAlarms"][0]
    assert a["StateValue"] == "ALARM" and a["StateUpdatedTimestamp"] == f"{DAY}T14:19:00Z" and a["EvaluationPeriods"] == 10
    lag = LAG()
    assert all(at(lag, f"14:{m}") > 50000 for m in range(10, 20)) and at(lag, "14:09") <= 50000
    age = series("AWS/Kafka", "EstimatedMaxTimeLag", "Maximum", ["ConsumerGroup=alert-ingest", "Topic=security-events", "ClusterName=security-events-cluster"])
    assert max(window_vals(age, "12:30", "14:03")) < 5 and 20 * 60 < at(age, "14:30") < 25 * 60   # alerts ~23 min stale at 14:30


def test_it_is_a_consumption_collapse_not_a_traffic_spike():
    prod = series("AWS/Kafka", "MessagesInPerSec", "Average", ["Topic=security-events", "ClusterName=security-events-cluster"])
    before, after = window_vals(prod, "12:30", "14:02"), window_vals(prod, "14:02", "14:30")
    assert max(before + after) < 1.15 * min(before + after)
    done = series("Abnormal/AlertIngest", "ProcessedPerSec")
    assert min(window_vals(done, "12:30", "14:02")) > 135
    assert max(window_vals(done, "14:10", "14:30")) < 40                   # consumption fell to ~22 msg/s
    assert max(window_vals(done, "14:10", "14:30")) < 0.3 * min(window_vals(prod, "14:10", "14:30"))


def test_per_message_latency_goes_from_ms_to_hundreds_of_ms():
    lat = series("Abnormal/AlertIngest", "EnrichLatencyMs")
    assert max(window_vals(lat, "12:30", "14:02")) < 5
    assert min(window_vals(lat, "14:10", "14:30")) > 300
    p99 = series("Abnormal/AlertIngest", "EnrichLatencyMs", "p99")
    assert max(window_vals(p99, "12:30", "14:02")) < 15 and min(window_vals(p99, "14:06", "14:30")) >= 700


def test_geoip_429s_start_when_new_tasks_pass_the_rate_limit():
    s429 = series("Abnormal/AlertIngest", "Geoip429Count", "Sum")
    req = series("Abnormal/AlertIngest", "GeoipRequestCount", "Sum")
    assert sum(window_vals(s429, "12:30", "14:04")) == 0 and at(s429, "14:03") == 0
    assert at(s429, "14:04") > 0 and min(window_vals(s429, "14:06", "14:30")) > 1500
    ok = [req[k] - s429[k] for k in req if k >= f"{DAY}T14:07:00Z"]
    assert all(1190 <= x <= 1210 for x in ok), ok[:3]                     # successes pinned at the 1200 rpm limit
    assert min(window_vals(req, "14:07", "14:30")) > 3000
    assert max(window_vals(req, "12:30", "14:02")) < 40                    # before: batching + cache = a trickle of requests


def test_scaling_out_cannot_help_arithmetic():
    """Successful lookups are capped at 1200/min = 20/s: the whole fleet cannot enrich more than that many messages
    per minute however many tasks run; production is ~150/s."""
    s429 = series("Abnormal/AlertIngest", "Geoip429Count", "Sum")
    req = series("Abnormal/AlertIngest", "GeoipRequestCount", "Sum")
    prod = series("AWS/Kafka", "MessagesInPerSec", "Average", ["Topic=security-events", "ClusterName=security-events-cluster"])
    ok_per_s = (at(req, "14:20") - at(s429, "14:20")) / 60
    assert 19 < ok_per_s < 21 and at(prod, "14:20") > 7 * ok_per_s
    cfg = json.loads((ENV / "config" / "geoip-svc.after.json").read_text())
    assert cfg["ratelimit"]["per_client_rpm"]["alert-ingest"] == 1200
    topic = q("describe", "msk", "security-events-cluster")["Topics"][0]
    assert topic["Partitions"] == 12                                       # consumers beyond 12 sit idle anyway


def test_dlq_fills_after_the_deploy_and_matches_describe():
    dlq = series("AWS/SQS", "ApproximateNumberOfMessagesVisible", "Maximum", ["QueueName=security-events-dlq"])
    assert max(window_vals(dlq, "12:30", "14:04")) == 0 and at(dlq, "14:30") > 3000
    assert list(dlq.values()) == sorted(dlq.values())
    assert q("describe", "sqs", "security-events-dlq")["Attributes"]["ApproximateNumberOfMessages"] == round(at(dlq, "14:30"))


# ---------------------------------------------------------------- the logs agree with the metrics
def test_logs_show_old_and_new_client_modes():
    rows = q("logs", "insights", "--group", "/ecs/alert-ingest", "--query", 'filter message like "geoip client mode" | stats count() as n by version')["results"]
    by = {r[0]["value"]: r[1]["value"] for r in rows}
    assert by == {"2026.09.29-1640-5e1d9b2": "8", "2026.09.30-1402-a91f3c7": "8"}
    new = q("logs", "filter", "--group", "/ecs/alert-ingest", "--pattern", "mode=sync", "--limit", "1")["events"][0]["message"]
    assert "cache=none" in new and "backoff_ms=0" in new


def test_no_warnings_before_the_deploy_then_throttle_and_dlq_lines():
    pre = q("logs", "insights", "--group", "/ecs/alert-ingest", "--query", 'filter level != "INFO"', "--end", "14:03")
    assert pre["results"] == []
    rows = q("logs", "insights", "--group", "/ecs/alert-ingest", "--query", "stats count() as n by level", "--start", "14:07")["results"]
    by = {r[0]["value"]: int(r[1]["value"]) for r in rows}
    assert by["WARN"] > 500 and by["ERROR"] > 500


def test_suppressed_counts_in_logs_reconcile_with_the_429_metric():
    logs = q("logs", "insights", "--group", "/ecs/alert-ingest", "--query", "filter status = 429 | stats sum(suppressed) as s, count() as n",
             "--start", "14:10", "--end", "14:20")["results"][0]
    s, n = int(logs[0]["value"]), int(logs[1]["value"])
    metric = sum(window_vals(series("Abnormal/AlertIngest", "Geoip429Count", "Sum"), "14:10", "14:20"))
    assert 0.9 * metric < s + n < 1.1 * metric


def test_geoip_server_side_is_healthy_and_just_rate_limiting():
    assert max(series("Abnormal/GeoipSvc", "Http5xxCount", "Sum", ["Service=geoip-svc"]).values()) == 0
    assert max(series("Abnormal/GeoipSvc", "ServerLatencyMs", "p99", ["Service=geoip-svc"]).values()) < 60
    thr = series("Abnormal/GeoipSvc", "ThrottledCount", "Sum", ["Client=risk-engine"])
    assert max(thr.values()) == 0                                          # the other client is untouched: it is this client's pattern
    assert q("config", "diff", "geoip-svc") == {"name": "geoip-svc", "changed": {}, "added": {}, "removed": {}}
    gs = [d for d in q("deploys", "--service", "geoip-svc")["deployments"]]
    assert all(d["startedAt"] < "2026-09-20" for d in gs)
    lim = q("logs", "filter", "--group", "/ecs/geoip-svc", "--pattern", "client=alert-ingest status=429", "--start", "14:00", "--limit", "1")
    assert lim["matched"] > 100
    assert q("alarms", "--name", "geoip-svc-5xx-high")["MetricAlarms"][0]["StateValue"] == "OK"     # 429 is not 5xx: the alarm gap


def test_alert_ingest_is_not_cpu_or_memory_bound():
    cpu = series("AWS/ECS", "CPUUtilization", "Average", ["ClusterName=prod", "ServiceName=alert-ingest"])
    assert min(window_vals(cpu, "12:30", "14:02")) > 30 and max(window_vals(cpu, "14:08", "14:30")) < 10
    mem = series("AWS/ECS", "MemoryUtilization", "Average", ["ClusterName=prod", "ServiceName=alert-ingest"])
    assert max(mem.values()) - min(mem.values()) < 6
    tasks = series("ECS/ContainerInsights", "RunningTaskCount", "Maximum", ["ClusterName=prod", "ServiceName=alert-ingest"])
    assert at(tasks, "14:30") == 8 and max(tasks.values()) == 10 and at(tasks, "14:03") == 10


# ---------------------------------------------------------------- red herrings are benign
def test_red_herring_rds_is_idle():
    cpu = series("AWS/RDS", "CPUUtilization", "Maximum")
    assert max(cpu.values()) < 30
    conn = series("AWS/RDS", "DatabaseConnections", "Maximum")
    assert max(conn.values()) - min(conn.values()) <= 3
    assert max(series("AWS/RDS", "WriteLatency", "Maximum").values()) < 0.002
    w = series("AWS/RDS", "WriteIOPS")
    assert at(w, "14:20") < 0.2 * at(w, "13:30")                         # the DB is starved by the consumer, not the reverse
    assert q("alarms", "--name", "alerts-prod-rds-cpu-high")["MetricAlarms"][0]["StateValue"] == "OK"


def test_red_herring_report_renderer_is_a_separate_cluster_with_its_own_deploy():
    a = q("alarms", "--name", "report-renderer-cpu-high", "--history")["MetricAlarms"][0]
    assert a["StateValue"] == "ALARM" and a["StateUpdatedTimestamp"] == f"{DAY}T14:07:00Z"
    cpu = series("AWS/ECS", "CPUUtilization", "Average", ["ClusterName=prod-batch", "ServiceName=report-renderer"])
    assert max(window_vals(cpu, "12:30", "14:05")) < 30 and min(window_vals(cpu, "14:06", "14:30")) > 85
    d = q("deploys", "--service", "report-renderer")["deployments"][-1]
    assert d["startedAt"] == f"{DAY}T13:58:41Z" and "in-process" in d["commit"]["message"] and d["cluster"] == "prod-batch"
    desc = q("describe", "ecs", "report-renderer")["services"][0]
    assert desc["clusterArn"].endswith("/prod-batch") and desc["launchType"] == "FARGATE"


def test_red_herring_broker_disk_alarm_came_and_went_before_the_incident():
    a = q("alarms", "--name", "msk-broker-2-disk-high", "--history")["MetricAlarms"][0]
    assert a["StateValue"] == "OK" and [h["To"] for h in a["History"]] == ["ALARM", "OK"]
    assert a["History"][0]["Timestamp"] == f"{DAY}T12:55:00Z" and a["History"][1]["Timestamp"] < f"{DAY}T13:30:00Z"
    disk = series("AWS/Kafka", "KafkaDataLogsDiskUsed", "Maximum", ["BrokerID=2", "ClusterName=security-events-cluster"])
    assert max(window_vals(disk, "12:30", "14:30")) >= 86 and max(window_vals(disk, "13:10", "14:31")) < 70
    assert max(window_vals(LAG(), "12:30", "13:30")) < 1000               # the lag never noticed
    trail = q("trail", "lookup", "--event-name", "UpdateBrokerStorage")["Events"]
    assert len(trail) == 1 and trail[0]["Username"] == "ops-dana" and trail[0]["EventTime"] < f"{DAY}T13:30:00Z"
