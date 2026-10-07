"""awsim query-subset tests, against a tiny hand-made snapshot (independent of the ic01 story)."""
from __future__ import annotations

import json
import subprocess
import sys

import pytest

from ic01_helpers import DRILL, awsim, q


@pytest.fixture()
def tiny(tmp_path, monkeypatch):
    env = tmp_path / "env"
    m = env / "cloudwatch" / "metrics" / "Test_Svc"
    m.mkdir(parents=True)
    rows = ["timestamp,value,dimensions,p99"]
    for i in range(6):        # 10:00..10:05, host=a: values 1..6, p99 = 10*value
        rows.append(f"2026-01-02T10:0{i}:00Z,{i + 1},Host=a,{(i + 1) * 10}")
    for i in range(2):
        rows.append(f"2026-01-02T10:0{i}:00Z,100,Host=b,500")
    (m / "Latency.csv").write_text("\n".join(rows) + "\n")
    (m / "Solo.csv").write_text("timestamp,value,dimensions\n2026-01-02T10:00:00Z,4,K=v\n2026-01-02T10:01:00Z,8,K=v\n2026-01-02T10:02:00Z,2,K=v\n"
                                "2026-01-02T10:03:00Z,6,K=v\n")
    lg = env / "cloudwatch" / "logs" / "web"
    lg.mkdir(parents=True)
    ev = [
        ("10:00:05", "INFO", "started ok", {"ms": 5, "path": "/a"}),
        ("10:00:30", "ERROR", "db timeout after 30s", {"ms": 30000, "path": "/b", "tenant": "t1"}),
        ("10:01:10", "WARN", "slow request", {"ms": 900, "path": "/a", "tenant": "t2"}),
        ("10:01:40", "ERROR", "db timeout after 5s", {"ms": 5000, "path": "/b", "tenant": "t1"}),
        ("10:02:00", "ERROR", "cache miss storm", {"ms": 120, "path": "/c", "tenant": "t3"}),
    ]
    (lg / "i-1.jsonl").write_text("".join(json.dumps({"timestamp": f"2026-01-02T{t}Z", "level": lv, "message": msg, **f}) + "\n" for t, lv, msg, f in ev[:3]))
    (lg / "i-2.jsonl").write_text("".join(json.dumps({"timestamp": f"2026-01-02T{t}Z", "level": lv, "message": msg, **f}) + "\n" for t, lv, msg, f in ev[3:]))
    (env / "cloudtrail").mkdir()
    (env / "cloudtrail" / "events.jsonl").write_text("".join(json.dumps(e) + "\n" for e in [
        {"eventTime": "2026-01-02T09:58:00Z", "eventSource": "rds.amazonaws.com", "eventName": "ModifyDBInstance", "eventID": "1", "userIdentity": {"type": "IAMUser", "userName": "ann"}},
        {"eventTime": "2026-01-02T10:01:00Z", "eventSource": "ecs.amazonaws.com", "eventName": "UpdateService", "eventID": "2", "userIdentity": {"type": "AssumedRole", "sessionContext": {"sessionIssuer": {"userName": "ci"}}}},
    ]))
    (env / "deploys.json").write_text(json.dumps([
        {"service": "a", "startedAt": "2026-01-02T09:00:00Z"}, {"service": "b", "startedAt": "2026-01-02T10:00:00Z"}]))
    (env / "meta.json").write_text(json.dumps({"now": "2026-01-02T10:10:00Z"}))
    (env / "config").mkdir()
    (env / "config" / "x.before.json").write_text(json.dumps({"a": 1, "n": {"k": "old", "gone": True}}))
    (env / "config" / "x.after.json").write_text(json.dumps({"a": 1, "n": {"k": "new"}, "added": 2}))
    (env / "alarms.json").write_text(json.dumps([
        {"AlarmName": "A", "StateValue": "ALARM", "History": [1]}, {"AlarmName": "B", "StateValue": "OK", "History": []}]))
    (env / "resources" / "ecs").mkdir(parents=True)
    (env / "resources" / "ecs" / "svc.json").write_text(json.dumps({"serviceName": "svc"}))
    monkeypatch.setenv("AWSIM_ENV", str(env))
    return env


def pts(res, stat):
    return [p[stat] for p in res["Datapoints"]]


M = ["metrics", "get", "--namespace", "Test/Svc", "--name", "Latency", "--dim", "Host=a"]


def test_metric_stats_over_period(tiny):
    assert pts(q(*M, "--period", "120", "--stat", "Sum"), "Sum") == [3, 7, 11]
    assert pts(q(*M, "--period", "120", "--stat", "Average"), "Average") == [1.5, 3.5, 5.5]
    assert pts(q(*M, "--period", "180", "--stat", "Maximum"), "Maximum") == [3, 6]
    assert pts(q(*M, "--period", "180", "--stat", "Minimum"), "Minimum") == [1, 4]
    assert pts(q(*M, "--period", "180", "--stat", "SampleCount"), "SampleCount") == [3, 3]


def test_metric_window_is_start_inclusive_end_exclusive(tiny):
    r = q(*M, "--start", "10:01", "--end", "10:03", "--stat", "Sum")
    assert [p["Timestamp"] for p in r["Datapoints"]] == ["2026-01-02T10:01:00Z", "2026-01-02T10:02:00Z"]


def test_metric_percentile_uses_p99_column_or_computes(tiny):
    assert pts(q(*M, "--period", "180", "--stat", "p99"), "p99") == [30, 60]       # worst minute of the period
    r = q("metrics", "get", "--namespace", "Test/Svc", "--name", "Solo", "--period", "240", "--stat", "p50")
    assert pts(r, "p50") == [4]                                                    # nearest-rank p50 of [4,8,2,6]


def test_metric_dimensions_must_be_unambiguous(tiny):
    with pytest.raises(awsim.SimError, match="ambiguous"):
        q("metrics", "get", "--namespace", "Test/Svc", "--name", "Latency")
    with pytest.raises(awsim.SimError, match="no datapoints"):
        q("metrics", "get", "--namespace", "Test/Svc", "--name", "Latency", "--dim", "Host=zzz")
    assert len(q("metrics", "get", "--namespace", "Test/Svc", "--name", "Latency", "--dim", "Host=b")["Datapoints"]) == 2


def test_metrics_list(tiny):
    got = {(m["MetricName"], tuple((d["Name"], d["Value"]) for d in m["Dimensions"])) for m in q("metrics", "list")["Metrics"]}
    assert got == {("Latency", (("Host", "a"),)), ("Latency", (("Host", "b"),)), ("Solo", (("K", "v"),))}


def test_logs_groups_tail_and_filter(tiny):
    assert q("logs", "groups")["logGroups"][0]["logGroupName"] == "/web"
    assert [e["timestamp"][-9:-1] for e in q("logs", "tail", "--group", "/web", "-n", "2")["events"]] == ["10:01:40", "10:02:00"]
    r = q("logs", "filter", "--group", "/web", "--pattern", "ERROR timeout")
    assert r["matched"] == 2
    assert q("logs", "filter", "--group", "/web", "--pattern", '"timeout after 5s"')["matched"] == 1
    assert q("logs", "filter", "--group", "/web", "--pattern", "?WARN ?storm")["matched"] == 2
    assert q("logs", "filter", "--group", "/web", "--pattern", "ERROR -timeout")["matched"] == 1
    assert q("logs", "filter", "--group", "/web", "--pattern", "ERROR", "--stream", "i-2")["matched"] == 2
    r = q("logs", "filter", "--group", "/web", "--pattern", "", "--limit", "2")
    assert r["matched"] == 5 and r["truncated"] and len(r["events"]) == 2
    r = q("logs", "filter", "--group", "/web", "--pattern", "ERROR", "--start", "10:01", "--end", "10:02")
    assert r["matched"] == 1


def ins(query, *extra):
    r = q("logs", "insights", "--group", "/web", "--query", query, *extra)
    return [{c["field"]: c["value"] for c in row} for row in r["results"]], r


def test_insights_fields_filter_sort_limit(tiny):
    rows, r = ins('fields @timestamp, level | filter level = "ERROR" | sort @timestamp asc | limit 2')
    assert [x["@timestamp"][-9:-1] for x in rows] == ["10:00:30", "10:01:40"]
    assert set(rows[0]) == {"@timestamp", "level"}
    assert r["statistics"] == {"recordsMatched": 2, "recordsScanned": 5} or r["statistics"]["recordsScanned"] == 5


def test_insights_default_order_is_newest_first(tiny):
    rows, _ = ins("fields @timestamp | limit 2")
    assert [x["@timestamp"][-9:-1] for x in rows] == ["10:02:00", "10:01:40"]


def test_insights_like_regex_substring_and_negation(tiny):
    assert len(ins("filter message like /timeout after \\d+s/")[0]) == 2
    assert len(ins('filter message like "storm"')[0]) == 1
    assert len(ins('filter message not like "timeout"')[0]) == 3
    assert len(ins("filter message like /(?i)STARTED/")[0]) == 1


def test_insights_comparisons_and_boolean_logic(tiny):
    assert len(ins("filter ms > 800")[0]) == 3
    assert len(ins("filter ms >= 900 and level != 'ERROR'")[0]) == 1
    assert len(ins("filter level = 'WARN' or ms < 10")[0]) == 2
    assert len(ins("filter not (level = 'ERROR' or ms < 10)")[0]) == 1
    assert len(ins("filter tenant = 't1'")[0]) == 2          # records without the field never match


def test_insights_stats(tiny):
    rows, _ = ins("stats count() as n, sum(ms) as total, max(ms) as worst, min(ms) as best, avg(ms) as mean by level")
    by = {r["level"]: r for r in rows}
    assert by["ERROR"] == {"level": "ERROR", "n": "3", "total": "35120", "worst": "30000", "best": "120", "mean": "11706.67"}
    assert by["INFO"]["n"] == "1"
    rows, _ = ins("stats count_distinct(tenant) as t, count(tenant) as c, pct(ms, 50) as p50")
    assert rows == [{"t": "3", "c": "4", "p50": "900"}]


def test_insights_stats_by_bin_and_sort(tiny):
    rows, _ = ins("stats count() as n by bin(1m)")
    assert [(r["bin(1m)"], r["n"]) for r in rows] == [("2026-01-02T10:00:00Z", "2"), ("2026-01-02T10:01:00Z", "2"), ("2026-01-02T10:02:00Z", "1")]
    rows, _ = ins("stats count() as n by path | sort n desc, path asc | limit 2")
    assert [(r["path"], r["n"]) for r in rows] == [("/a", "2"), ("/b", "2")]
    rows, _ = ins("stats count() as n by level | filter n > 1")
    assert [r["level"] for r in rows] == ["ERROR"]


def test_insights_window_and_malformed(tiny):
    rows, r = ins("fields level", "--start", "10:01", "--end", "10:02")
    assert len(rows) == 2 and r["statistics"]["recordsScanned"] == 2
    with pytest.raises(awsim.SimError, match="Malformed"):
        ins("parse message /x/")
    with pytest.raises(awsim.SimError, match="Malformed"):
        ins("filter level =")


def test_trail_deploys_describe_config_alarms(tiny):
    assert [e["EventName"] for e in q("trail", "lookup")["Events"]] == ["ModifyDBInstance", "UpdateService"]
    assert q("trail", "lookup", "--username", "ci")["Events"][0]["EventName"] == "UpdateService"
    assert q("trail", "lookup", "--event-name", "ModifyDBInstance", "--start", "09:00", "--end", "09:59")["Events"][0]["Username"] == "ann"
    assert q("trail", "lookup", "--start", "10:00")["Events"][0]["EventName"] == "UpdateService"
    assert [d["service"] for d in q("deploys", "--service", "b")["deployments"]] == ["b"]
    assert len(q("deploys", "--start", "09:30")["deployments"]) == 1
    assert q("describe")["types"] == {"ecs": ["svc"]}
    assert q("describe", "ecs", "svc")["serviceName"] == "svc"
    with pytest.raises(awsim.SimError):
        q("describe", "ecs", "nope")
    d = q("config", "diff", "x")
    assert d["changed"] == {"n.k": {"before": "old", "after": "new"}} and d["added"] == {"added": 2} and d["removed"] == {"n.gone": True}
    assert q("config", "show", "x", "--version", "before")["a"] == 1
    assert [a["AlarmName"] for a in q("alarms", "--state", "ALARM")["MetricAlarms"]] == ["A"]
    assert "History" not in q("alarms")["MetricAlarms"][0] and q("alarms", "--history")["MetricAlarms"][0]["History"] == [1]


def test_time_parsing(tiny):
    assert awsim.iso(awsim.parse_ts("10:05")) == "2026-01-02T10:05:00Z"
    assert awsim.iso(awsim.parse_ts("2026-01-02T10:05:00+02:00")) == "2026-01-02T08:05:00Z"
    with pytest.raises(awsim.SimError):
        awsim.parse_ts("yesterday")


def test_cli_exit_codes_and_table(tiny):
    env = {"AWSIM_ENV": str(tiny), "PATH": ""}
    ok = subprocess.run([sys.executable, str(DRILL / "awsim.py"), "metrics", "get", "--namespace", "Test/Svc", "--name", "Solo", "--table"],
                        capture_output=True, text=True, env=env)
    assert ok.returncode == 0 and ok.stdout.splitlines()[0] == "2026-01-02T10:00:00Z  4"
    bad = subprocess.run([sys.executable, str(DRILL / "awsim.py"), "logs", "tail", "--group", "/nope"], capture_output=True, text=True, env=env)
    assert bad.returncode == 254 and "ResourceNotFoundException" in bad.stderr
