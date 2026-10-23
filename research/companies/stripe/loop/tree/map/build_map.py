import json
import re
import sys
from pathlib import Path

W = Path(__file__).resolve().parents[2]  # loop/
sys.path.insert(0, str(W / "tree"))
from check_tree import parse, resolve  # noqa: E402

rounds, prereq = parse((W / "tree/interview-loop.yaml").read_text())
yaml = (W / "tree/interview-loop.yaml").read_text().splitlines()
# skill names + round names + durations
names = {}
rname = {}
rdur = {}
cur = None
for ln in yaml:
    m = re.match(r"^(\s*)- id: (\S+)", ln)
    if m:
        cur = m.group(2)
        continue
    m = re.match(r"^\s*name: (.+)$", ln)
    if m and cur:
        names[cur] = m.group(1).strip()
    m = re.match(r"^\s*duration_min: (\d+)", ln)
    if m and cur:
        rdur[cur] = int(m.group(1))
CORE = {
    "A": (
        "解析 · 聚合 · 定序输出",
        [
            "parse_aggregate",
            "tiered_rules",
            "string_expansion",
            "validation_error_codes",
            "format_validation",
            "log_redaction",
            "comparator_api",
            "self_tests_while_coding",
            "json_etl_join",
        ],
    ),
    "B": ("规则 · 状态机 · 类设计", ["scheduler_state_machine", "rule_engine", "oo_design_followups"]),
    "C": (
        "窗口 · 索引 · 并发",
        ["sliding_window_topk", "sliding_window", "lru_locking", "rate_limiter_4part", "concurrency_races"],
    ),
    "D": (
        "HTTP · API · 工具集成",
        [
            "http_client",
            "pagination_retry_idempotency",
            "geo_nearest",
            "read_repo_fast",
            "git_diff_tooling",
            "ai_pair_programming",
        ],
    ),
    "E": (
        "调试方法论",
        ["reproduce_first", "debugger_breakpoints", "ast_visitor_paths", "io_streams", "parser_edge_cases"],
    ),
    "F": ("系统设计 · 钱的正确性", ["problem_framing", "api_contract", "failure_modes", "ledger_invariants"]),
    "G": (
        "行为 · 沟通",
        [
            "self_intro_why_stripe",
            "logistics",
            "operating_principles_mapping",
            "project_deep_dive",
            "star_l",
            "principles_coverage",
        ],
    ),
}
skill2core = {s: k for k, (_, ss) in CORE.items() for s in ss}
# catalog rows
cat = (W / "CATALOG.md").read_text().splitlines()
probs = {}
for ln in cat:
    m = re.match(r"^\| (ps\d\d|cd\d\d|bs\d\d|int\d\d|sd\d\d|rc|hm|bq) \|(.*)\|\s*$", ln)
    if not m:
        continue
    pid = m.group(1)
    cells = [c.strip() for c in m.group(2).split("|")]
    t = cells[0]
    b = re.search(r"\*\*(.+?)\*\*", t)
    title = b.group(1) if b else t[:60]
    alias = re.sub(r"\*\*(.+?)\*\*", "", t).strip(" ·")
    conf = next((c for c in cells if re.search(r"high|medium|low", c)), "")
    refs = next((c for c in cells if re.fullmatch(r"\d+(（.*?）)?", c)), "")
    probs[pid] = {
        "id": pid,
        "title": title,
        "alias": alias,
        "detail": cells[1] if len(cells) > 1 else "",
        "recent": cells[2] if len(cells) > 3 else "",
        "refs": refs,
        "conf": conf,
        "extra": cells[3] if pid.startswith("bs") else (cells[5] if len(cells) > 6 else ""),
    }
out_rounds = []
for r in rounds:
    skills = []
    for s in r["skills"]:
        skills.append(
            {
                "id": s["id"],
                "name": names.get(s["id"], s["id"]),
                "core": skill2core.get(s["id"], "?"),
                "problems": s["problems"],
            }
        )
    out_rounds.append(
        {
            "id": r["id"],
            "name": names.get(r["id"], r["id"]),
            "dur": rdur.get(r["id"]),
            "skills": skills,
            "study": r["study"],
        }
    )
for pid, p in probs.items():
    p["built"] = resolve(pid) is not None
    p["round"] = next((r["id"] for r in out_rounds for s in r["skills"] if pid in s["problems"]), "")
    p["skills"] = [s["id"] for r in out_rounds for s in r["skills"] if pid in s["problems"]]
    cores = sorted(
        {skill2core.get(s, "?") for s in p["skills"]},
        key=lambda k: -sum(1 for s in p["skills"] if skill2core.get(s) == k),
    )
    p["core"] = cores[0] if cores else "?"
    p["cores"] = cores
data = {"cores": {k: v[0] for k, v in CORE.items()}, "rounds": out_rounds, "problems": probs}
print(json.dumps(data, ensure_ascii=False))
