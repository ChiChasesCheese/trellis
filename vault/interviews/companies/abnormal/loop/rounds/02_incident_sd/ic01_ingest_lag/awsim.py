#!/usr/bin/env python3
"""awsim - query an offline AWS snapshot with an AWS-CLI-shaped interface (stdlib only).

The snapshot lives in ./env (override with AWSIM_ENV=<dir>).  Every timestamp is UTC ISO 8601
("2026-09-30T14:02:00Z"); --start/--end also accept "HH:MM" (the snapshot's date).

  python3 awsim.py now
  python3 awsim.py alarms [--state ALARM|OK] [--name N] [--history]
  python3 awsim.py metrics list [--namespace N]
  python3 awsim.py metrics get --namespace N --name M [--dim k=v ...] [--start T] [--end T]
                               [--stat Average|Sum|Maximum|Minimum|SampleCount|p99] [--period 60] [--table]
  python3 awsim.py logs groups
  python3 awsim.py logs tail   --group G [--stream S] [-n 20] [--table]
  python3 awsim.py logs filter --group G --pattern 'ERROR "timeout"' [--stream S] [--start T] [--end T] [--limit 50]
  python3 awsim.py logs insights --group G --query 'fields @timestamp, level | filter level = "ERROR" | limit 5'
        subset: fields | filter (= != < <= > >= like /re/ "substr", not like, and/or/not, parentheses)
                | stats count() count(f) sum(f) avg(f) min(f) max(f) pct(f,99) count_distinct(f) [as x] by f, bin(1m)
                | sort f [asc|desc] | limit N     (@timestamp, @message, @logStream are available)
  python3 awsim.py trail lookup [--event-name X] [--username U] [--event-source S] [--start T] [--end T]
  python3 awsim.py deploys [--service S] [--start T] [--end T]
  python3 awsim.py describe [<type> [<name>]]
  python3 awsim.py config list | show NAME [--version before|after] | diff NAME

Differences from the real CLI (on purpose): one call does start-query + get-query-results; timestamps are ISO
strings, not epoch; a metric's p50/p90/p99 come from per-minute percentile columns when the snapshot has them
(a period longer than 60 s reports the worst minute); CloudTrailEvent is an object, not a JSON string.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import os
import re
import shlex
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

UTC = timezone.utc


def env_dir() -> Path:
    return Path(os.environ.get("AWSIM_ENV") or Path(__file__).resolve().parent / "env")


class SimError(Exception):
    pass


def fail(kind: str, msg: str):
    raise SimError(f"An error occurred ({kind}): {msg}")


# ---------------------------------------------------------------- time helpers
def meta() -> dict:
    p = env_dir() / "meta.json"
    return json.loads(p.read_text()) if p.exists() else {}


def parse_ts(s: str) -> datetime:
    s = s.strip()
    m = re.fullmatch(r"(\d{1,2}):(\d{2})(?::(\d{2}))?", s)
    if m:
        now = meta().get("now")
        if not now:
            fail("ValidationError", "HH:MM needs env/meta.json with 'now'")
        d = parse_ts(now)
        return d.replace(hour=int(m[1]), minute=int(m[2]), second=int(m[3] or 0), microsecond=0)
    try:
        d = datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        fail("ValidationError", f"cannot parse time {s!r}; use 2026-09-30T14:02:00Z or HH:MM")
    return d if d.tzinfo else d.replace(tzinfo=UTC)


def iso(d: datetime) -> str:
    return d.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def window(a) -> tuple[datetime, datetime]:
    lo = parse_ts(a.start) if getattr(a, "start", None) else datetime.min.replace(tzinfo=UTC)
    hi = parse_ts(a.end) if getattr(a, "end", None) else datetime.max.replace(tzinfo=UTC)
    return lo, hi


def num(x: float):
    if isinstance(x, float) and x == int(x) and abs(x) < 1e15:
        return int(x)
    return round(x, 2) if isinstance(x, float) else x


# ---------------------------------------------------------------- metrics
def ns_dir(ns: str) -> Path:
    return env_dir() / "cloudwatch" / "metrics" / ns.replace("/", "_")


def parse_dims(s: str) -> dict:
    return dict(kv.split("=", 1) for kv in s.split(";") if kv)


def load_metric(ns: str, name: str) -> list[dict]:
    p = ns_dir(ns) / f"{name}.csv"
    if not p.exists():
        fail("ResourceNotFound", f"metric {ns}/{name} not found (try: metrics list)")
    rows = []
    with p.open(newline="") as f:
        for r in csv.DictReader(f):
            r["_ts"] = parse_ts(r["timestamp"])
            r["_v"] = float(r["value"])
            r["_dims"] = parse_dims(r.get("dimensions", ""))
            rows.append(r)
    return rows


def percentile(vals: list[float], p: float) -> float:
    vals = sorted(vals)
    k = max(0, math.ceil(p / 100 * len(vals)) - 1)
    return vals[k]


def cmd_metrics_list(a):
    out = []
    root = env_dir() / "cloudwatch" / "metrics"
    for nsd in sorted(root.iterdir()) if root.exists() else []:
        ns = nsd.name.replace("_", "/", 1)
        if a.namespace and a.namespace.replace("/", "_") != nsd.name:
            continue
        for f in sorted(nsd.glob("*.csv")):
            sets = sorted({r.get("dimensions", "") for r in load_metric(ns, f.stem)})
            for ds in sets:
                out.append({"Namespace": ns, "MetricName": f.stem,
                            "Dimensions": [{"Name": k, "Value": v} for k, v in parse_dims(ds).items()]})
    return {"Metrics": out}


def cmd_metrics_get(a):
    rows = load_metric(a.namespace, a.name)
    want = dict(d.split("=", 1) for d in (a.dim or []))
    rows = [r for r in rows if all(r["_dims"].get(k) == v for k, v in want.items())]
    sets = sorted({r.get("dimensions", "") for r in rows})
    if not rows:
        fail("ResourceNotFound", f"no datapoints for {a.namespace}/{a.name} with dimensions {want or '{}'}")
    if len(sets) > 1:
        fail("ValidationError", "dimensions are ambiguous, add --dim; available sets: " + " | ".join(s or "(none)" for s in sets))
    lo, hi = window(a)
    stat = a.stat
    buckets: dict[int, list[dict]] = {}
    for r in rows:
        if lo <= r["_ts"] < hi:
            buckets.setdefault(int(r["_ts"].timestamp()) // a.period, []).append(r)
    pts = []
    for b in sorted(buckets):
        rs = buckets[b]
        vals = [r["_v"] for r in rs]
        if stat == "Average":
            v = sum(vals) / len(vals)
        elif stat == "Sum":
            v = sum(vals)
        elif stat == "Maximum":
            v = max(vals)
        elif stat == "Minimum":
            v = min(vals)
        elif stat == "SampleCount":
            v = float(len(vals))
        elif re.fullmatch(r"p\d+(\.\d+)?", stat):
            if stat in rs[0]:
                v = max(float(r[stat]) for r in rs if r.get(stat) not in (None, ""))
            else:
                v = percentile(vals, float(stat[1:]))
        else:
            fail("ValidationError", f"unknown statistic {stat}")
        pts.append({"Timestamp": iso(datetime.fromtimestamp(b * a.period, UTC)), stat: num(v)})
    return {"Label": a.name, "Namespace": a.namespace, "Dimensions": want, "Period": a.period, "Statistic": stat, "Datapoints": pts}


# ---------------------------------------------------------------- logs
def group_dir(g: str) -> Path:
    return env_dir() / "cloudwatch" / "logs" / g.strip("/").replace("/", "__")


def load_events(group: str, stream: str | None = None) -> list[dict]:
    d = group_dir(group)
    if not d.is_dir():
        fail("ResourceNotFoundException", f"log group {group} does not exist (try: logs groups)")
    ev = []
    for f in sorted(d.glob("*.jsonl")):
        sname = f.stem.replace("__", "/")
        if stream and sname != stream:
            continue
        for line in f.read_text().splitlines():
            if not line.strip():
                continue
            rec = json.loads(line)
            rec["@timestamp"] = rec["timestamp"]
            rec["@logStream"] = sname
            rec["@raw"] = line
            rec["@message"] = line
            rec["_ts"] = parse_ts(rec["timestamp"])
            ev.append(rec)
    ev.sort(key=lambda r: (r["_ts"], r["@logStream"]))
    return ev


def public(ev: dict) -> dict:
    return {"logStreamName": ev["@logStream"], "timestamp": ev["timestamp"], "message": ev["@raw"]}


def cmd_logs_groups(a):
    root = env_dir() / "cloudwatch" / "logs"
    out = []
    for d in sorted(root.iterdir()) if root.exists() else []:
        fs = sorted(d.glob("*.jsonl"))
        out.append({"logGroupName": "/" + d.name.replace("__", "/"), "streams": len(fs),
                    "storedBytes": sum(f.stat().st_size for f in fs)})
    return {"logGroups": out}


def cmd_logs_tail(a):
    ev = load_events(a.group, a.stream)
    return {"events": [public(e) for e in ev[-a.n:]]}


def match_pattern(raw: str, pattern: str) -> bool:
    toks = shlex.split(pattern)
    must = [t for t in toks if not t.startswith(("?", "-"))]
    anyof = [t[1:] for t in toks if t.startswith("?")]
    never = [t[1:] for t in toks if t.startswith("-") and len(t) > 1]
    return (all(t in raw for t in must) and (not anyof or any(t in raw for t in anyof))
            and not any(t in raw for t in never))


def cmd_logs_filter(a):
    lo, hi = window(a)
    ev = [e for e in load_events(a.group, a.stream) if lo <= e["_ts"] < hi and match_pattern(e["@raw"], a.pattern)]
    return {"matched": len(ev), "events": [public(e) for e in ev[:a.limit]],
            **({"truncated": True} if len(ev) > a.limit else {})}


# ---- Logs Insights subset
class Lexer:
    def __init__(self, s: str):
        self.s, self.i, self.toks = s, 0, []
        self.run()

    def run(self):
        s = self.s
        while True:
            while self.i < len(s) and s[self.i].isspace():
                self.i += 1
            if self.i >= len(s):
                return
            c = s[self.i]
            prev = self.toks[-1] if self.toks else None
            if c == "/" and prev and prev == ("id", "like"):
                j = self.i + 1
                while j < len(s) and s[j] != "/":
                    j += 2 if s[j] == "\\" else 1
                self.toks.append(("re", s[self.i + 1:j]))
                self.i = j + 1
            elif c in "\"'":
                j = s.index(c, self.i + 1)
                self.toks.append(("str", s[self.i + 1:j]))
                self.i = j + 1
            elif m := re.compile(r"-?\d+(?:\.\d+)?").match(s, self.i):
                self.toks.append(("num", float(m[0])))
                self.i = m.end()
            elif m := re.compile(r"[@A-Za-z_][\w@.]*").match(s, self.i):
                w = m[0]
                self.toks.append(("id", w.lower() if w.lower() in ("and", "or", "not", "like") else w))
                self.i = m.end()
            elif m := re.compile(r"!=|<=|>=|=|<|>|\(|\)").match(s, self.i):
                self.toks.append(("op", m[0]))
                self.i = m.end()
            else:
                fail("MalformedQueryException", f"unexpected character {c!r} in filter: {s}")


class FilterParser:
    def __init__(self, expr: str):
        self.t = Lexer(expr).toks
        self.p = 0
        self.ast = self.or_()
        if self.p != len(self.t):
            fail("MalformedQueryException", f"unexpected token {self.t[self.p]} in filter: {expr}")

    def peek(self):
        return self.t[self.p] if self.p < len(self.t) else (None, None)

    def eat(self):
        self.p += 1
        return self.t[self.p - 1]

    def or_(self):
        n = self.and_()
        while self.peek() == ("id", "or"):
            self.eat()
            n = ("or", n, self.and_())
        return n

    def and_(self):
        n = self.not_()
        while self.peek() == ("id", "and"):
            self.eat()
            n = ("and", n, self.not_())
        return n

    def not_(self):
        if self.peek() == ("id", "not"):
            self.eat()
            return ("not", self.not_())
        return self.primary()

    def primary(self):
        if self.peek() == ("op", "("):
            self.eat()
            n = self.or_()
            if self.eat() != ("op", ")"):
                fail("MalformedQueryException", "missing )")
            return n
        k, field = self.eat()
        if k != "id":
            fail("MalformedQueryException", f"expected a field name, got {field!r}")
        neg = False
        if self.peek() == ("id", "not"):
            self.eat()
            neg = True
        if self.peek() == ("id", "like"):
            self.eat()
            k2, v = self.eat()
            if k2 not in ("str", "re"):
                fail("MalformedQueryException", "like needs /regex/ or a quoted string")
            return ("like", field, k2, v, neg)
        k2, op = self.eat()
        if k2 != "op" or op in "()":
            fail("MalformedQueryException", f"expected a comparison after {field}")
        k3, v = self.eat()
        if k3 not in ("str", "num"):
            fail("MalformedQueryException", f"expected a literal after {field} {op}")
        return ("cmp", field, op, v)


def as_num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def evaluate(n, rec) -> bool:
    t = n[0]
    if t == "and":
        return evaluate(n[1], rec) and evaluate(n[2], rec)
    if t == "or":
        return evaluate(n[1], rec) or evaluate(n[2], rec)
    if t == "not":
        return not evaluate(n[1], rec)
    if t == "like":
        _, f, kind, pat, neg = n
        v = rec.get(f)
        if v is None:
            return False
        s = str(v)
        hit = bool(re.search(pat, s)) if kind == "re" else pat in s
        return hit != neg
    _, f, op, lit = n
    v = rec.get(f)
    if v is None:
        return False
    a, b = (as_num(v), lit) if isinstance(lit, float) else (str(v), lit)
    if a is None:
        return False
    return {"=": a == b, "!=": a != b, "<": a < b, "<=": a <= b, ">": a > b, ">=": a >= b}[op]


def split_top(s: str, sep: str) -> list[str]:
    out, depth, q, cur = [], 0, None, ""
    i = 0
    while i < len(s):
        c = s[i]
        if q:
            if c == "\\":
                cur += s[i:i + 2]
                i += 2
                continue
            if c == q:
                q = None
        elif c in "\"'":
            q = c
        elif c == "/" and cur.rstrip().endswith("like"):
            q = "/"
        elif c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
        if c == sep and not q and depth == 0:
            out.append(cur)
            cur = ""
        else:
            cur += c
        i += 1
    out.append(cur)
    return [x.strip() for x in out]


BIN = re.compile(r"bin\(\s*(\d+)\s*([smhd])\s*\)$")


def bin_key(key: str, rec):
    m = BIN.match(key)
    secs = int(m[1]) * {"s": 1, "m": 60, "h": 3600, "d": 86400}[m[2]]
    t = int(rec["_ts"].timestamp()) // secs * secs
    return iso(datetime.fromtimestamp(t, UTC))


def do_stats(body: str, recs: list[dict]) -> tuple[list[dict], list[str]]:
    m = re.split(r"\s+by\s+", body, maxsplit=1)
    aggs_s, by_s = m[0], (m[1] if len(m) > 1 else "")
    keys = split_top(by_s, ",") if by_s else []
    aggs = []
    for a in split_top(aggs_s, ","):
        mm = re.fullmatch(r"(\w+)\((.*)\)(?:\s+as\s+(\w+))?", a)
        if not mm:
            fail("MalformedQueryException", f"cannot parse aggregation {a!r}")
        fn, arg, alias = mm[1], mm[2].strip(), mm[3]
        aggs.append((fn, arg, alias or (f"{fn}({arg or '*'})")))
    groups: dict[tuple, list[dict]] = {}
    for r in recs:
        kv = []
        for k in keys:
            v = bin_key(k, r) if BIN.match(k) else r.get(k)
            if v is None:
                break
            kv.append(str(v))
        else:
            groups.setdefault(tuple(kv), []).append(r)
    rows = []
    for kv in sorted(groups):
        rs = groups[kv]
        row = dict(zip(keys, kv))
        for fn, arg, name in aggs:
            f = arg.split(",")[0].strip()
            vals = [x for x in (as_num(r.get(f)) for r in rs) if x is not None] if f else []
            if fn == "count":
                v = len(rs) if not f else sum(1 for r in rs if r.get(f) is not None)
            elif fn == "count_distinct":
                v = len({str(r.get(f)) for r in rs if r.get(f) is not None})
            elif fn == "pct":
                v = percentile(vals, float(arg.split(",")[1])) if vals else None
            elif fn in ("sum", "avg", "min", "max"):
                v = None if not vals else {"sum": sum(vals), "avg": sum(vals) / len(vals), "min": min(vals), "max": max(vals)}[fn]
            else:
                fail("MalformedQueryException", f"unsupported function {fn}()")
            row[name] = num(float(v)) if isinstance(v, (int, float)) else v
        rows.append(row)
    return rows, keys + [n for _, _, n in aggs]


def sortkey(v):
    f = as_num(v)
    return (0, f, "") if f is not None else (1, 0.0, str(v))


def run_insights(events: list[dict], query: str) -> tuple[list[dict], list[str]]:
    recs = list(events)
    cols: list[str] = ["@timestamp", "@message"]
    for stage in split_top(query, "|"):
        if not stage:
            continue
        cmd, _, body = stage.partition(" ")
        cmd, body = cmd.lower(), body.strip()
        if cmd in ("fields", "display"):
            cols = [c for c in split_top(body, ",") if c]
        elif cmd == "filter":
            ast = FilterParser(body).ast
            recs = [r for r in recs if evaluate(ast, r)]
        elif cmd == "stats":
            recs, cols = do_stats(body, recs)
        elif cmd == "sort":
            for item in reversed(split_top(body, ",")):
                parts = item.split()
                desc = len(parts) > 1 and parts[1].lower() == "desc"
                recs = sorted(recs, key=lambda r, f=parts[0]: sortkey(r.get(f, "")), reverse=desc)
        elif cmd == "limit":
            recs = recs[:int(body)]
        else:
            fail("MalformedQueryException", f"unsupported command {cmd!r} (supported: fields filter stats sort limit)")
    return recs, cols


def cmd_logs_insights(a):
    lo, hi = window(a)
    evs = []
    for g in a.group:
        evs += [e for e in load_events(g) if lo <= e["_ts"] < hi]
    q = a.query
    stages = split_top(q, "|")
    # Insights sorts by @timestamp desc before `limit`; reproduce that by moving the default order ahead of the pipeline.
    if not any(s.lower().startswith(("sort", "stats")) for s in stages):
        evs.sort(key=lambda r: (r["_ts"], r["@logStream"]), reverse=True)
    recs, cols = run_insights(evs, q)
    limit = 1000
    rows = []
    for r in recs[:limit]:
        rows.append([{"field": c, "value": str(r[c])} for c in cols if c in r])
    return {"status": "Complete", "statistics": {"recordsMatched": len(recs), "recordsScanned": len(evs)}, "results": rows}


# ---------------------------------------------------------------- cloudtrail, deploys, describe, config, alarms
def jsonl(p: Path) -> list[dict]:
    return [json.loads(x) for x in p.read_text().splitlines() if x.strip()] if p.exists() else []


def username(e: dict) -> str:
    ui = e.get("userIdentity", {})
    return ui.get("userName") or ui.get("sessionContext", {}).get("sessionIssuer", {}).get("userName") or ui.get("type", "")


def cmd_trail_lookup(a):
    lo, hi = window(a)
    out = []
    for e in jsonl(env_dir() / "cloudtrail" / "events.jsonl"):
        t = parse_ts(e["eventTime"])
        if not lo <= t < hi:
            continue
        if a.event_name and e["eventName"] != a.event_name:
            continue
        if a.event_source and e["eventSource"] != a.event_source:
            continue
        if a.username and username(e) != a.username:
            continue
        out.append({"EventId": e["eventID"], "EventName": e["eventName"], "EventTime": e["eventTime"],
                    "EventSource": e["eventSource"], "Username": username(e), "CloudTrailEvent": e})
    out.sort(key=lambda x: x["EventTime"])
    return {"Events": out}


def cmd_deploys(a):
    lo, hi = window(a)
    ds = json.loads((env_dir() / "deploys.json").read_text())
    ds = [d for d in ds if (not a.service or d["service"] == a.service) and lo <= parse_ts(d["startedAt"]) < hi]
    return {"deployments": sorted(ds, key=lambda d: d["startedAt"])}


def cmd_describe(a):
    root = env_dir() / "resources"
    if not a.type:
        return {"types": {t.name: sorted(p.stem for p in t.glob("*.json")) for t in sorted(root.iterdir())}}
    d = root / a.type
    if not d.is_dir():
        fail("ResourceNotFoundException", f"unknown resource type {a.type}; types: {sorted(p.name for p in root.iterdir())}")
    if not a.name:
        return {a.type: sorted(p.stem for p in d.glob("*.json"))}
    p = d / f"{a.name}.json"
    if not p.exists():
        fail("ResourceNotFoundException", f"{a.type} {a.name} not found; have: {sorted(x.stem for x in d.glob('*.json'))}")
    return json.loads(p.read_text())


def flat(d, pre=""):
    out = {}
    for k, v in d.items():
        if isinstance(v, dict) and v:
            out.update(flat(v, f"{pre}{k}."))
        else:
            out[f"{pre}{k}"] = v
    return out


def cmd_config(a):
    root = env_dir() / "config"
    if a.action == "list":
        return {"configs": sorted({p.name.split(".")[0] for p in root.glob("*.json")})}
    if not a.name:
        fail("ValidationError", "config show/diff needs NAME")
    if a.action == "show":
        p = root / f"{a.name}.{a.version}.json"
        if not p.exists():
            fail("ResourceNotFoundException", f"{p.name} not found")
        return json.loads(p.read_text())
    b, f = (json.loads((root / f"{a.name}.{v}.json").read_text()) for v in ("before", "after"))
    fb, fa = flat(b), flat(f)
    return {"name": a.name,
            "changed": {k: {"before": fb[k], "after": fa[k]} for k in fb if k in fa and fb[k] != fa[k]},
            "added": {k: fa[k] for k in fa if k not in fb}, "removed": {k: fb[k] for k in fb if k not in fa}}


def cmd_alarms(a):
    al = json.loads((env_dir() / "alarms.json").read_text())
    out = []
    for x in al:
        if a.state and x["StateValue"] != a.state:
            continue
        if a.name and x["AlarmName"] != a.name:
            continue
        out.append(x if a.history else {k: v for k, v in x.items() if k != "History"})
    return {"MetricAlarms": out}


def cmd_now(a):
    return meta()


# ---------------------------------------------------------------- output + cli
def table(cmd: str, res: dict) -> str | None:
    if "Datapoints" in res:
        return "\n".join(f"{p['Timestamp']}  {p[res['Statistic']]}" for p in res["Datapoints"])
    if "Metrics" in res:
        return "\n".join(f"{m['Namespace']}  {m['MetricName']}  " + ";".join(f"{d['Name']}={d['Value']}" for d in m["Dimensions"]) for m in res["Metrics"])
    if "events" in res:
        rows = []
        for e in res["events"]:
            try:
                j = json.loads(e["message"])
                rows.append(f"{e['timestamp']}  {e['logStreamName']}  {j.get('level', '')}  {j.get('message', '')}")
            except ValueError:
                rows.append(f"{e['timestamp']}  {e['logStreamName']}  {e['message']}")
        return "\n".join(rows)
    if "results" in res:
        return "\n".join("  ".join(f"{c['field']}={c['value']}" for c in r) for r in res["results"])
    return None


def build_parser():
    p = argparse.ArgumentParser(prog="awsim", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    def common(sp, window_=True):
        if window_:
            sp.add_argument("--start")
            sp.add_argument("--end")
        sp.add_argument("--table", action="store_true", help="compact text instead of JSON")
        return sp

    common(sub.add_parser("now"), False).set_defaults(fn=cmd_now)
    al = common(sub.add_parser("alarms"), False)
    al.add_argument("--state")
    al.add_argument("--name")
    al.add_argument("--history", action="store_true")
    al.set_defaults(fn=cmd_alarms)

    m = sub.add_parser("metrics").add_subparsers(dest="sub", required=True)
    ml = common(m.add_parser("list"), False)
    ml.add_argument("--namespace")
    ml.set_defaults(fn=cmd_metrics_list)
    mg = common(m.add_parser("get"))
    mg.add_argument("--namespace", required=True)
    mg.add_argument("--name", required=True)
    mg.add_argument("--dim", action="append")
    mg.add_argument("--stat", default="Average")
    mg.add_argument("--period", type=int, default=60)
    mg.set_defaults(fn=cmd_metrics_get)

    lg = sub.add_parser("logs").add_subparsers(dest="sub", required=True)
    common(lg.add_parser("groups"), False).set_defaults(fn=cmd_logs_groups)
    lt = common(lg.add_parser("tail"), False)
    lt.add_argument("--group", required=True)
    lt.add_argument("--stream")
    lt.add_argument("-n", type=int, default=20)
    lt.set_defaults(fn=cmd_logs_tail)
    lf = common(lg.add_parser("filter"))
    lf.add_argument("--group", required=True)
    lf.add_argument("--stream")
    lf.add_argument("--pattern", default="")
    lf.add_argument("--limit", type=int, default=50)
    lf.set_defaults(fn=cmd_logs_filter)
    li = common(lg.add_parser("insights"))
    li.add_argument("--group", required=True, action="append")
    li.add_argument("--query", required=True)
    li.set_defaults(fn=cmd_logs_insights)

    tr = sub.add_parser("trail").add_subparsers(dest="sub", required=True)
    tl = common(tr.add_parser("lookup"))
    tl.add_argument("--event-name")
    tl.add_argument("--event-source")
    tl.add_argument("--username")
    tl.set_defaults(fn=cmd_trail_lookup)

    dp = common(sub.add_parser("deploys"))
    dp.add_argument("--service")
    dp.set_defaults(fn=cmd_deploys)

    ds = common(sub.add_parser("describe"), False)
    ds.add_argument("type", nargs="?")
    ds.add_argument("name", nargs="?")
    ds.set_defaults(fn=cmd_describe)

    cf = common(sub.add_parser("config"), False)
    cf.add_argument("action", choices=["list", "show", "diff"])
    cf.add_argument("name", nargs="?")
    cf.add_argument("--version", choices=["before", "after"], default="after")
    cf.set_defaults(fn=cmd_config)
    return p


def main(argv=None) -> int:
    a = build_parser().parse_args(argv)
    try:
        res = a.fn(a)
    except SimError as e:
        print(e, file=sys.stderr)
        return 254
    txt = table(a.cmd, res) if a.table else None
    print(txt if txt is not None else json.dumps(res, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
