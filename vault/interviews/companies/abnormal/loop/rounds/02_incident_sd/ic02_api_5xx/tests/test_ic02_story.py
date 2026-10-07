"""The snapshot must support the story: lock phase (09:40-09:52) then missing-index phase (09:52-10:05); the red herrings
(certificate rotation, tenant traffic doubling) are really benign; every timestamp is UTC ISO 8601."""
from __future__ import annotations

import json

from ic02_helpers import ENV, ISO_ANY, ISO_OK, at, awsim, q, series, window_vals

DAY = "2026-10-02"
NOW = f"{DAY}T10:05:00Z"
LB = "LoadBalancer=app/portal-alb/7f3e2b1c9d4a6e05"
TG = "TargetGroup=targetgroup/portal-api/3c9a1e7d2b6f4a80"


def alb(name, stat="Sum", tg=False):
    return series("AWS/ApplicationELB", name, stat, [LB] + ([TG] if tg else []))


def rate5xx():
    req, t5, e5 = alb("RequestCount"), alb("HTTPCode_Target_5XX_Count", tg=True), alb("HTTPCode_ELB_5XX_Count")
    return {k: 100 * (t5[k] + e5[k]) / req[k] for k in req}


# ---------------------------------------------------------------- timestamps and shape
def test_every_timestamp_literal_is_utc_iso8601_with_seconds():
    bad = []
    for p in ENV.rglob("*"):
        if p.is_file():
            for m in ISO_ANY.finditer(p.read_text()):
                if not ISO_OK.fullmatch(m.group(0)):
                    bad.append((p.name, m.group(0)))
    assert not bad, bad[:5]


def test_meta_and_time_ranges():
    meta = awsim.meta()
    assert meta["now"] == NOW and meta["windowStart"] == f"{DAY}T08:30:00Z"
    lo, hi = meta["windowStart"], meta["now"]
    for p in (ENV / "cloudwatch" / "metrics").rglob("*.csv"):
        seen = {}
        for line in p.read_text().splitlines()[1:]:
            ts, _, dims = line.split(",")[:3]
            assert lo <= ts <= hi, (p.name, ts)
            seen.setdefault(dims, []).append(ts)
        for dims, ts in seen.items():
            assert ts == sorted(ts) and len(set(ts)) == len(ts), (p.name, dims)
            if "Route=timeline" not in dims:
                assert len(ts) == 96, (p.name, dims)                   # 08:30..10:05, one per minute
    for p in (ENV / "cloudwatch" / "logs").rglob("*.jsonl"):
        for line in p.read_text().splitlines():
            t = json.loads(line)["timestamp"]
            assert lo <= t <= hi, (p, t)
    for e in q("trail", "lookup")["Events"]:
        assert lo <= e["EventTime"] <= hi
    for d in q("deploys")["deployments"]:
        assert d["startedAt"] < d["completedAt"] <= hi


def test_alb_counts_add_up():
    req, ok, t4 = alb("RequestCount"), alb("HTTPCode_Target_2XX_Count", tg=True), alb("HTTPCode_Target_4XX_Count", tg=True)
    t5, e5 = alb("HTTPCode_Target_5XX_Count", tg=True), alb("HTTPCode_ELB_5XX_Count")
    e504 = alb("HTTPCode_ELB_504_Count")
    for k in req:
        assert abs(req[k] - (ok[k] + t4[k] + t5[k] + e5[k])) < 0.1, k
        assert e5[k] == e504[k]


# ---------------------------------------------------------------- phase A: the lock
def test_page_alarm_matches_the_metric_math():
    a = q("alarms", "--name", "portal-api-5xx-rate-and-p99", "--history")["MetricAlarms"][0]
    assert a["StateValue"] == "ALARM" and a["StateUpdatedTimestamp"] == f"{DAY}T09:42:00Z"
    r, p99 = rate5xx(), alb("TargetResponseTime", "p99", tg=True)
    assert max(window_vals(r, "08:30", "09:40")) < 0.1 and max(window_vals(p99, "08:30", "09:40")) < 0.5
    assert all(at(r, m) > 5 and at(p99, m) > 3 for m in ("09:40", "09:41", "09:42"))
    assert all(v > 5 for v in window_vals(r, "09:40", "10:06"))      # never recovers below the threshold


def test_migration_runs_in_one_transaction_and_holds_the_lock_until_killed():
    mig = q("describe", "migrations", "0142_alerts_timeline")
    assert mig["transactional"] is True and mig["status"] == "ROLLED_BACK" and "CONCURRENTLY" not in " ".join(mig["statements"])
    log = [e["message"] for e in q("logs", "tail", "--group", "/ecs/portal-api-migrate", "-n", "50")["events"]]
    assert any("BEGIN" in m for m in log) and any("timeout 720s exceeded" in m for m in log)
    ct = {e["EventName"]: e["EventTime"] for e in q("trail", "lookup", "--event-source", "ecs.amazonaws.com", "--start", "09:39")["Events"]
          if e["EventName"] in ("RunTask", "StopTask")}
    assert ct == {"RunTask": f"{DAY}T09:40:05Z", "StopTask": f"{DAY}T09:52:10Z"}
    waits = q("logs", "filter", "--group", "/aws/rds/instance/portal-prod/postgresql", "--pattern", "still waiting for AccessShareLock", "--limit", "1000")
    stamps = [e["timestamp"] for e in waits["events"]]
    assert waits["matched"] > 100 and min(stamps) >= f"{DAY}T09:40:07Z" and max(stamps) < f"{DAY}T09:52:14Z"
    assert all("Process holding the lock: 40117" in e["message"] for e in waits["events"])
    lost = q("logs", "filter", "--group", "/aws/rds/instance/portal-prod/postgresql", "--pattern", "connection to client lost")["events"]
    assert [e["timestamp"] for e in lost] == [f"{DAY}T09:52:14Z"] and '"pid":40117' in lost[0]["message"]
    pi = q("describe", "pi", "portal-prod")["Windows"][1]
    assert pi["TopWaits"][0]["wait"] == "Lock:relation" and pi["Blockers"][0]["pid"] == 40117
    assert q("describe", "pg", "portal-prod.alerts")["oid"] == 16421


def test_lock_phase_pool_exhausted_and_connections_at_max():
    pool = series("Portal/API", "DbPoolInUse", "Maximum")
    assert max(window_vals(pool, "08:30", "09:40")) < 40 and min(window_vals(pool, "09:40", "10:06")) >= 240
    conn = series("AWS/RDS", "DatabaseConnections", "Maximum")
    assert max(window_vals(conn, "08:30", "09:40")) < 170 and max(conn.values()) == 297      # 300 - 3 superuser-reserved
    load = series("AWS/RDS", "DBLoad")
    assert min(window_vals(load, "09:41", "09:52")) > 200 and max(window_vals(load, "09:53", "10:06")) < 50
    cpu = series("AWS/RDS", "CPUUtilization")
    assert max(window_vals(cpu, "09:41", "09:52")) < 30                      # the DB is waiting, not working
    slots = q("logs", "filter", "--group", "/aws/rds/instance/portal-prod/postgresql", "--pattern", "remaining connection slots")
    assert slots["matched"] >= 5 and all(e["timestamp"] < f"{DAY}T09:44:00Z" for e in slots["events"])


def test_lock_phase_fails_every_db_route_but_not_the_others():
    rl = lambda r: series("Portal/API", "RouteLatencyMs", "p99", [f"Route={r}"])
    for r in ("alerts_list", "alert_detail", "users_risk"):         # users_risk does not touch `alerts`: it is the shared pool
        assert min(window_vals(rl(r), "09:41", "09:52")) >= 10000
    for r in ("config", "me"):
        assert max(rl(r).values()) < 100
    rows = q("logs", "insights", "--group", "/ecs/portal-api", "--start", "09:42", "--end", "09:52",
             "--query", "filter status >= 500 | stats sum(sample_rate) as n by route")["results"]
    routes = {r[0]["value"] for r in rows}
    assert "/api/v2/users/{id}/risk" in routes and "/api/v2/config" not in routes and "/api/v2/me" not in routes


# ---------------------------------------------------------------- phase B: lock gone, index missing
def test_after_the_lock_it_improves_but_does_not_recover():
    r, avg = rate5xx(), alb("TargetResponseTime", "Average", tg=True)
    assert min(window_vals(r, "09:42", "09:52")) > 60 and 6 < min(window_vals(r, "09:54", "10:06")) and max(window_vals(r, "09:54", "10:06")) < 10
    assert min(window_vals(avg, "09:42", "09:52")) > 6 and max(window_vals(avg, "09:54", "10:06")) < 3 and min(window_vals(avg, "09:54", "10:06")) > 1.5
    cpu, io = series("AWS/RDS", "CPUUtilization"), series("AWS/RDS", "ReadIOPS")
    assert min(window_vals(cpu, "09:53", "10:06")) > 85 and min(window_vals(io, "09:53", "10:06")) > 11000
    assert q("alarms", "--name", "rds-portal-prod-cpu-high")["MetricAlarms"][0]["StateUpdatedTimestamp"] == f"{DAY}T09:57:00Z"
    assert q("describe", "rds", "portal-prod")["DBInstances"][0]["Iops"] == 12000


def test_the_index_the_endpoint_needs_does_not_exist():
    t = q("describe", "pg", "portal-prod.alerts")
    assert not any("user_id" in i["def"] for i in t["indexes"]) and t["rows_by_tenant_top"][0]["tenant_id"] == "tn-orbit"
    pi = q("describe", "pi", "portal-prod")["Windows"][2]
    assert pi["TopWaits"][0]["wait"] == "IO:DataFileRead" and "user_id = $2" in pi["TopSQL"][0]["sql"] and not pi["Blockers"]
    plan = q("logs", "filter", "--group", "/aws/rds/instance/portal-prod/postgresql", "--pattern", "Rows Removed by Filter")
    assert plan["matched"] >= 5 and all("alerts_tenant_created_idx" in e["message"] and "tn-orbit" in e["message"] for e in plan["events"])
    assert all(e["timestamp"] >= f"{DAY}T09:52:14Z" for e in plan["events"])
    d = [x for x in q("deploys", "--service", "portal-api-migrate")["deployments"]]
    assert len(d) == 1 and d[0]["status"] == "FAILED"


def test_timeline_is_the_hot_route_and_the_big_tenant_is_slowest():
    tl = series("Portal/API", "RouteLatencyMs", "Average", ["Route=timeline"])
    lst = series("Portal/API", "RouteLatencyMs", "Average", ["Route=alerts_list"])
    assert min(window_vals(tl, "09:54", "10:06")) > 2 * max(window_vals(lst, "09:54", "10:06"))
    rows = q("logs", "insights", "--group", "/ecs/portal-api", "--start", "09:55", "--end", "10:05",
             "--query", 'filter route like "timeline" and status = 200 | stats pct(duration_ms, 50) as p50 by tenant')["results"]
    p50 = {r[0]["value"]: float(r[1]["value"]) for r in rows}
    assert p50["tn-orbit"] > 6000 and max(v for k, v in p50.items() if k != "tn-orbit") < 4000
    rows = q("logs", "insights", "--group", "/ecs/portal-api", "--start", "09:55", "--end", "10:05",
             "--query", "filter status >= 500 | stats sum(sample_rate) as n by route")["results"]
    n = {r[0]["value"]: int(r[1]["value"]) for r in rows}
    reqs = series("Portal/API", "RouteRequestCount", "Sum", ["Route=timeline"])
    total = series("AWS/ApplicationELB", "RequestCount", "Sum", [LB])
    share = sum(window_vals(reqs, "09:55", "10:05")) / sum(window_vals(total, "09:55", "10:05"))
    assert share < 0.15 and n["/api/v2/users/{id}/timeline"] / sum(n.values()) > 0.25   # ~11% of traffic, >25% of the 5xx


def test_app_500_with_client_disconnected_is_what_the_alb_counts_as_504():
    rows = q("logs", "insights", "--group", "/ecs/portal-api", "--start", "09:55", "--end", "10:05",
             "--query", "filter client_disconnected = 1 or status = 500 | stats sum(sample_rate) as n, min(duration_ms) as fastest by status")["results"]
    assert rows and rows[0][0]["value"] == "500" and float(rows[0][2]["value"]) > 25000
    cfg = q("config", "show", "portal-api")
    assert cfg["db"]["statement_timeout_ms"] == 30000 and q("config", "show", "portal-alb")["attributes"]["idle_timeout.timeout_seconds"] == 15


# ---------------------------------------------------------------- red herrings
def test_red_herring_certificate_rotation_is_benign():
    ev = q("trail", "lookup", "--username", "ops-kim")["Events"]
    assert [e["EventName"] for e in ev] == ["ImportCertificate", "ModifyListener"] and ev[1]["EventTime"] == f"{DAY}T09:38:20Z"
    tls = alb("ClientTLSNegotiationErrorCount")
    assert max(tls.values()) <= 2 and max(window_vals(tls, "09:38", "10:06")) <= 2
    r = rate5xx()
    assert max(window_vals(r, "09:38", "09:40")) < 0.1                       # two clean minutes on the new certificate
    diff = q("config", "diff", "portal-alb")
    assert list(diff["changed"]) == ["listener.certificateArn"]
    assert q("alarms", "--name", "acm-portal-cert-days-to-expiry")["MetricAlarms"][0]["StateValue"] == "OK"


def test_red_herring_tenant_doubling_is_an_amplifier_not_the_cause():
    t = series("Portal/API", "TenantRequestCount", "Sum", ["Tenant=tn-orbit"])
    assert at(t, "09:25") > 1.8 * at(t, "08:45")
    r = rate5xx()
    assert max(window_vals(r, "09:20", "09:40")) < 0.1                        # 20 minutes at double traffic, no errors
    rows = q("logs", "insights", "--group", "/ecs/portal-api", "--start", "09:55", "--end", "10:05",
             "--query", "filter status >= 500 | stats count_distinct(tenant) as tenants")["results"]
    assert int(rows[0][0]["value"]) >= 8                                      # everyone is failing, not just tn-orbit


def test_web_deploy_404s_are_the_frontend_arriving_before_the_api():
    t4 = alb("HTTPCode_Target_4XX_Count", tg=True)
    assert at(t4, "09:34") < 100 and at(t4, "09:37") > 1500 and at(t4, "09:44") < 100
    d = q("deploys", "--service", "portal-web")["deployments"][0]
    assert "timeline" in d["commit"]["message"] and d["completedAt"] == f"{DAY}T09:35:40Z"


def test_app_is_not_cpu_bound_and_autoscaling_would_not_fire():
    cpu = series("AWS/ECS", "CPUUtilization", "Average", ["ServiceName=portal-api"])
    assert max(window_vals(cpu, "09:41", "10:06")) < 20 and min(window_vals(cpu, "08:30", "09:40")) > 28
    assert "CPUUtilization 60%" in q("describe", "ecs", "portal-api")["services"][0]["autoScaling"]
