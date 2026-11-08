"""Evidence for the study planner's weights: how often each design question and concept is actually asked.

    uv run python scripts/plan_evidence.py          # writes sources/local/plan/evidence/{bank.json, EVIDENCE.md}

Source 1, the Hello Interview question bank (sources/local/hello-interview/premium/questions.json): every report carries
company, level and date, and some carry the candidate's own description of what was probed. Raw counts are biased:
one company (Meta) files about 40% of all reports, so a question Meta likes would dominate. The frequency index is
therefore company-normalised and mixed by target:

    share(q, c)  = recency- and level-weighted reports of q at company c / all such reports at c
    freq(q)      = sum over company groups g of  w_g * mean over companies c in g of share(q, c)

with groups and weights from sources/local/plan/config.json (`targets`), recency a half-life (`half_life_months`), and
senior-and-above reports weighted up. A concept's direct evidence is the same index computed over the reports whose
description mentions it (keyword lists below), on top of what it inherits from the questions that need it.

Source 2, external public reports (sources/local/plan/evidence/external.jsonl, collected by an agent from 1point3acres,
LeetCode Discuss, Glassdoor, GitHub compilations, with URL and date for each) is folded in the same way as one more
company group when present.

Coverage: the share of the target-weighted interview mass that falls on questions the deck has a topic for.
"""
from __future__ import annotations

import json
import math
import re
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
BANK = ROOT / "sources/local/hello-interview/premium/questions.json"
EXTERNAL = ROOT / "sources/local/plan/evidence/external.jsonl"
OUT = ROOT / "sources/local/plan/evidence"

SENIOR = {"SENIOR", "STAFF", "PRINCIPAL", "MANAGER", "SENIOR_MANAGER", "DIRECTOR", "SENIOR_DIRECTOR"}
# what a report's own words say was probed -> concept topics (Chinese and English; lower-case match)
CONCEPTS = {
    "t.idempotency": ["idempot", "exactly once", "exactly-once", "double charg", "duplicate payment", "dedup", "幂等", "重复扣"],
    "t.caching": ["cache", "caching", "redis", "缓存"],
    "t.kafka": ["kafka", "message queue", "queue", "pub/sub", "pubsub", "消息队列"],
    "t.sharding": ["shard", "partition", "分片", "分库"],
    "t.consistent-hashing": ["consistent hash", "一致性哈希"],
    "t.cap": ["consisten", "cap theorem", "replica", "replication", "一致性"],
    "t.contention": ["race condition", "concurren", "lock", "oversell", "contention", "double book", "并发", "超卖"],
    "t.multi-step": ["saga", "two phase", "2pc", "outbox", "distributed transaction", "workflow", "分布式事务"],
    "t.scaling-reads": ["read heavy", "read-heavy", "hot key", "fan-out", "fanout", "feed", "timeline"],
    "t.scaling-writes": ["write heavy", "write-heavy", "high write", "throughput", "batch"],
    "t.realtime": ["websocket", "real time", "real-time", "server-sent", "long poll", "push notification", "实时推送"],
    "t.rdbms": ["sql", "postgres", "mysql", "relational", "transaction", "index"],
    "t.data-modeling": ["schema", "data model", "table", "数据模型"],
    "t.api": ["api design", "rest", "endpoint", "grpc", "pagination", "接口"],
    "t.network": ["load balanc", "dns", "cdn", "tcp", "http"],
    "t.reliability": ["fault", "failure", "retry", "circuit breaker", "availability", "outage", "容错", "重试"],
    "t.numbers": ["estimat", "capacity", "qps", "back of the envelope", "scale", "估算"],
    "t.long-tasks": ["cron", "schedul", "job", "delay", "定时"],
    "t.ranking": ["top k", "top-k", "leaderboard", "ranking", "排行"],
    "t.proximity": ["geo", "location", "nearby", "proximity", "quadtree", "geohash"],
    "t.es": ["search", "elasticsearch", "inverted index", "full text"],
    "t.blobs": ["upload", "s3", "blob", "presigned", "multipart", "chunk", "large file", "大文件"],
    "t.security": ["auth", "oauth", "token", "encrypt", "security", "鉴权"],
    "t.dlock": ["distributed lock", "分布式锁"],
    "t.observability": ["monitor", "alert", "metric", "logging"],
    "t.pay-correctness": ["payment", "psp", "refund", "charge", "支付"],
    "t.pay-ledger": ["ledger", "balance", "wallet", "double entry", "账本", "余额"],
    "t.pay-reconciliation": ["reconcil", "settlement", "对账", "结算"],
    "t.rate-limit": ["rate limit", "throttl", "限流"],
}


def months_ago(d: str) -> float:
    if not d:
        return 24.0
    y, m = int(d[:4]), int(d[5:7])
    t = date.today()
    return max(0.0, (t.year - y) * 12 + t.month - m)


def report_weight(r: dict, half_life: float) -> float:
    w = 0.5 ** (months_ago(r.get("approxAskedOn") or "") / half_life)
    return w * (1.2 if r.get("level") in SENIOR else 1.0)


def source_agreement(a: dict[str, float], b: dict[str, float]) -> dict:
    """Spearman rank correlation of two frequency indexes over the covered topics both contain, plus top-20 overlap."""
    keys = [k for k in a if k in b and not k.startswith("uncovered:")]
    if len(keys) < 3:
        return {"n": len(keys), "rho": 0.0, "top20_overlap": 0}
    ra = {k: i for i, k in enumerate(sorted(keys, key=lambda k: -a[k]))}
    rb = {k: i for i, k in enumerate(sorted(keys, key=lambda k: -b[k]))}
    n = len(keys)
    rho = 1 - 6 * sum((ra[k] - rb[k]) ** 2 for k in keys) / (n * (n * n - 1))
    top = lambda d: {k for k in sorted((k for k in d if not k.startswith("uncovered:")), key=lambda k: -d[k])[:20]}
    return {"n": n, "rho": rho, "top20_overlap": len(top(a) & top(b))}


def group_of(company: str, targets: dict) -> str:
    for g, spec in targets.items():
        if company in spec.get("companies", []):
            return g
    return "others"


SHRINK = 30.0  # pseudo-reports: a company's mix is pulled toward the pooled mix, harder the fewer reports it has


def mixed_index(per_company: dict[str, dict[str, float]], targets: dict) -> tuple[dict[str, float], dict]:
    """per_company[c][key] = weighted reports; returns key -> sum_g w_g * mean_{c in g} share(key, c), where each
    company's share is shrunk toward the pooled share (empirical Bayes): (n_qc + SHRINK * p_q) / (n_c + SHRINK).
    A company with 9 reports then nudges the pooled mix instead of overwriting it."""
    pooled = defaultdict(float)
    for rows in per_company.values():
        for k, v in rows.items():
            pooled[k] += v
    z = sum(pooled.values()) or 1.0
    prior = {k: v / z for k, v in pooled.items()}
    by_group = defaultdict(list)
    for c, rows in per_company.items():
        total = sum(rows.values())
        if total > 0:
            by_group[group_of(c, targets)].append(
                {k: (rows.get(k, 0.0) + SHRINK * p) / (total + SHRINK) for k, p in prior.items()})
    out = defaultdict(float)
    used = {}
    for g, shares in by_group.items():
        w = targets.get(g, {}).get("weight", targets.get("others", {}).get("weight", 0.1))
        used[g] = {"companies": len(shares), "weight": w}
        for s in shares:
            for k, v in s.items():
                out[k] += w * v / len(shares)
    return dict(out), used


def main() -> int:
    import study_plan as S
    cfg = S.config()
    targets = cfg.get("targets") or {
        "bytedance": {"weight": 0.35, "companies": ["TikTok", "ByteDance"]},
        "bigtech": {"weight": 0.45, "companies": ["Meta", "Google", "Amazon", "Microsoft", "Apple", "Netflix", "Uber", "Airbnb",
                                                  "LinkedIn", "Stripe", "OpenAI", "Anthropic", "Databricks", "Snowflake",
                                                  "DoorDash", "Salesforce", "Oracle", "Pinterest", "Snapchat", "Coinbase"]},
        "others": {"weight": 0.20, "companies": []},
    }
    half = float(cfg.get("half_life_months", 18))
    tree = S.Tree()
    slug_topic = {}
    for n in tree.sk.walk():
        if ".pre-" in n.id:
            continue  # a 先修 leaf keeps its old question's name but now lives under a concept topic
        m = re.match(r"^(qb|tt)\.(sd|lld)\.([a-z0-9-]+)(?:\.|$)", n.id)  # the question node, or a leaf under it
        if m:
            slug_topic.setdefault(m.group(3), tree.topic(n.id))
        m = re.match(r"^sd\.problem-breakdowns\.([a-z0-9-]+)(?:\.|$)", n.id)
        if m:
            slug_topic.setdefault("bd:" + m.group(1), tree.topic(n.id))
    alias_file = OUT / "aliases.json"  # same question, another name; reviewed by hand
    if alias_file.exists():
        for k, v in json.loads(alias_file.read_text(encoding="utf-8")).items():
            if not k.startswith("_") and v in tree.node:
                slug_topic[k] = tree.topic(v) if tree.node[v].children == [] else v
    bank = json.loads(BANK.read_text(encoding="utf-8"))
    sd_types = {"SYSTEM_DESIGN", "OBJECT_ORIENTED_DESIGN"}
    q_company = defaultdict(lambda: defaultdict(float))
    c_company = defaultdict(lambda: defaultdict(float))
    meta = {}
    for q in bank:
        if q["defaultInterviewType"] not in sd_types:
            continue
        page = (q.get("detailsLink") or "").rsplit("/", 1)[-1]
        topic = slug_topic.get(q["slug"]) or (slug_topic.get("bd:" + page) if page else None)
        key = topic or f"uncovered:{q['slug']}"
        meta.setdefault(key, {"titles": set(), "reports": 0, "bytedance": 0, "last": ""})
        meta[key]["titles"].add(q["title"])
        for r in q["upvotes"]:
            w = report_weight(r, half)
            q_company[r["company"]][key] += w
            meta[key]["reports"] += 1
            meta[key]["bytedance"] += r["company"] in ("TikTok", "ByteDance")
            meta[key]["last"] = max(meta[key]["last"], (r.get("approxAskedOn") or "")[:7])
            text = (r.get("description") or "").lower()
            for concept, kws in CONCEPTS.items():
                if any(k in text for k in kws):
                    c_company[r["company"]][concept] += w
    external = []
    if EXTERNAL.exists():
        for line in EXTERNAL.read_text(encoding="utf-8").splitlines():
            try:
                external.append(json.loads(line))
            except json.JSONDecodeError:
                pass
        external = [e for e in external if e.get("primary", True)]  # cross-vendor duplicates are merged into one primary row
        q_bank = {c: dict(v) for c, v in q_company.items()}
        q_ext: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
        for e in external:  # each public report counts once for its company, like a bank report
            company = e.get("company") or "unknown"
            level = (e.get("level") or "").lower()
            r = {"approxAskedOn": (e.get("date") or "") + "-01" if e.get("date") else "",
                 "level": "SENIOR" if any(k in level for k in ("senior", "staff", "principal", "资深", "高级")) else ""}
            w = report_weight(r, half) * {"high": 1.0, "medium": 0.7, "low": 0.4}.get(e.get("confidence"), 0.5)
            if e.get("campus") or any(k in level for k in ("intern", "实习", "校招", "new grad")):
                w *= 0.5  # campus and intern loops ask less design
            topics = e.get("topics_union") or e.get("topics") or []
            q = re.sub(r"\s+", " ", (e.get("question") or "").lower()).strip()
            if not topics and re.match(r"(system design: )?design\b", q) and not re.search(r"hidden|not given|not stated|not named", q):
                topics = ["uncovered:ext:" + q[:80]]  # a named design prompt we have no topic for still counts
            for t in topics:  # one report is one unit, shared by the topics it names
                q_company[company][t] += w / len(topics)
                q_ext[company][t] += w / len(topics)
                meta.setdefault(t, {"titles": set(), "reports": 0, "bytedance": 0, "last": ""})
                if t.startswith("uncovered:"):
                    meta[t]["titles"].add(e.get("question") or "")
                meta[t]["reports"] += 1
                meta[t]["bytedance"] += company in ("TikTok", "ByteDance")
                meta[t]["last"] = max(meta[t]["last"], e.get("date") or "")
            for t in e.get("concepts_union") or e.get("concepts") or []:
                c_company[company][t] += w
    else:
        q_bank, q_ext = q_company, {}
    qfreq, used = mixed_index(q_company, targets)
    agreement = source_agreement(mixed_index(q_bank, targets)[0], mixed_index(q_ext, targets)[0]) if q_ext else None
    cfreq, _ = mixed_index(c_company, targets)
    total = sum(qfreq.values()) or 1.0
    covered = sum(v for k, v in qfreq.items() if not k.startswith("uncovered:"))
    out = {
        "method": {"targets": targets, "half_life_months": half, "senior_weight": 1.2, "groups_used": used,
                   "bank_reports": sum(len(q["upvotes"]) for q in bank if q["defaultInterviewType"] in sd_types),
                   "external_reports": len(external), "agreement": agreement},
        "coverage": covered / total,
        "questions": {k: {"freq": v / total, "reports": meta[k]["reports"], "bytedance": meta[k]["bytedance"], "last": meta[k]["last"],
                          "titles": sorted(meta[k]["titles"])[:3]} for k, v in sorted(qfreq.items(), key=lambda kv: -kv[1])},
        "concepts": {k: v / (sum(cfreq.values()) or 1) for k, v in sorted(cfreq.items(), key=lambda kv: -kv[1])},
    }
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "bank.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    qs = list(out["questions"].items())
    cum, n80 = 0.0, 0
    for i, (_, v) in enumerate(qs):
        cum += v["freq"]
        if cum >= 0.8:
            n80 = i + 1
            break
    lines = ["# 系统设计考频证据", "",
             f"题库系统设计与面向对象设计报告 {out['method']['bank_reports']} 条，外部公开报告 {len(external)} 条（跨站重复已合并）。",
             *([f"**两路数据是否一致：** 两边都出现的 {agreement['n']} 个主题，排名的 Spearman 相关 {agreement['rho']:.2f}；"
                f"题库前 20 里有 {agreement['top20_overlap']} 个也在外部前 20。"] if agreement else []),
             f"按公司归一化后按目标混合：" + "，".join(f"{g} {s['weight']:.0%}（{used.get(g, {}).get('companies', 0)} 家公司有数据）" for g, s in targets.items()) + "。",
             f"时间半衰期 {half:.0f} 个月，Senior 及以上报告权重 1.2；每家公司的分布向整体分布收缩（经验贝叶斯，伪计数 {SHRINK:.0f}）。", "",
             f"**覆盖率：** 按这个口径，deck 里已有主题的题目占全部面试考频的 {out['coverage']:.1%}。",
             f"**二八：** 考频最高的 {n80} 道题（共 {len(qs)} 道）占 80%。", "", "## 考频前 30 的题", "",
             "| 排名 | 主题 / 题 | 考频占比 | 报告数 | 字节/TikTok | 最近 |", "|---|---|---|---|---|---|"]
    for i, (k, v) in enumerate(qs[:30], 1):
        name = tree.title(k) if k in tree.node else "（未覆盖）" + v["titles"][0] if v["titles"] else k
        lines.append(f"| {i} | {name} | {v['freq']:.2%} | {v['reports']} | {v['bytedance']} | {v['last']} |")
    unc = [(k, v) for k, v in qs if k.startswith("uncovered:")][:15]
    lines += ["", "## 考频高但 deck 里没有的题", ""] + [f"- {v['titles'][0] if v['titles'] else k}：{v['freq']:.2%}，{v['reports']} 条报告" for k, v in unc]
    lines += ["", "## 报告里直接点名的概念（按同样口径）", ""] + [f"- {tree.title(k) if k in tree.node else k}：{v:.1%}" for k, v in list(out["concepts"].items())[:20]]
    (OUT / "EVIDENCE.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"coverage {out['coverage']:.1%} · top {n80}/{len(qs)} questions = 80% · external {len(external)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
