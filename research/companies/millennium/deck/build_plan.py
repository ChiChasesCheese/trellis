"""Build the Millennium sprint deck plans: uv run python research/companies/millennium/deck/build_plan.py

Writes sources/local/plan/millennium/plan.json (deck 6 Millennium) and lc_plan.json (deck 7 Millennium 力扣) in the
format scripts/company_deck.py deals: [{"label": "<NN part>", "ids": [card id, …]}, …]. The plans stay local: some
parts borrow private cards (his Braintree examples). Company cards come from the millennium domain in skeleton order;
the rest are borrowed from their own domains and go home on `company_deck.py --deck … release`.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT))
from anki_refresh import call  # noqa: E402
from trellis.skeleton import load_skeleton  # noqa: E402

OUT = ROOT / "sources/local/plan/millennium"
CARDS = ROOT / "vault/interviews/companies/millennium/deck/cards"

# Python leaves the Millennium question bank maps to (vault/domains/python/BUILD.md §3): the first 3 cards of each.
PY_LEAVES = ["functions.decorators", "concurrency.gil", "concurrency.choosing", "asyncio.event-loop", "asyncio.coroutines-tasks",
             "asyncio.debugging", "iteration.generators", "iteration.context-managers", "model.names-objects", "model.mutability",
             "model.dict-set-internals", "model.numbers", "memory.refcounting", "memory.cyclic-gc", "memory.allocator",
             "memory.leaks-tracemalloc", "concurrency.locks-races", "functions.arguments", "functions.first-class",
             "runtime.import-system", "performance.containers", "performance.numpy-vectorization", "performance.pandas-at-scale",
             "engineering.money-time"]
# His Braintree examples (private) that answer project deep-dive questions for a data-engineering role.
BT_SLUGS = ["pay-correctness", "pay-ledger", "pay-reconciliation", "change-data-capture", "kafka", "idempotency",
            "long-running-tasks", "multi-step-processes", "estimation", "numbers-to-know"]
# System-design tour decks that a market-data service draws on: their three overview cards.
TOUR = ["realtime-updates", "kafka", "time-series-databases", "caching", "scaling-reads", "scaling-writes", "change-data-capture"]
LC_SEEN = ["trapping-rain-water", "container-with-most-water", "subarray-sums-divisible-by-k", "subarray-sum-equals-k",
           "merge-intervals", "best-time-to-buy-and-sell-stock", "lru-cache", "find-median-from-data-stream", "valid-parentheses",
           "palindromic-substrings", "powx-n", "find-the-smallest-divisor-given-a-threshold", "maximal-square",
           "partition-array-into-two-arrays-to-minimize-sum-difference"]


def fm(path: Path) -> dict:
    head = path.read_text(encoding="utf-8").split("---")[1]
    return {k: v.strip() for k, v in re.findall(r"^(\w+):\s*(.*)$", head, re.M)}


def company(branches: list[str]) -> list[str]:
    """The millennium domain's cards under these branches, in skeleton order, then by step."""
    sk = load_skeleton(ROOT / "skeleton/millennium.yaml")
    place = {n.id: i for i, n in enumerate(sk.walk())}
    rows = []
    for f in CARDS.rglob("*.md"):
        m = fm(f)
        if m.get("node", "").split(".")[0] in branches:
            rows.append((place.get(m["node"], 9999), int(m.get("step", 99)), m["id"]))
    return [r[2] for r in sorted(rows)]


def vault_ids(folder: Path, nodes: list[str], per: int) -> list[str]:
    by: dict[str, list] = {}
    for f in folder.rglob("*.md"):
        m = fm(f)
        if m.get("node") in nodes:
            by.setdefault(m["node"], []).append((int(m.get("step", 99)), m["id"]))
    return [i for n in nodes for _, i in sorted(by.get(n, []))[:per]]


def anki_ids(query: str, limit: int) -> list[str]:
    """Cards picked from a deck the first time, then the same ids every time: once dealt, they are no longer in that deck."""
    picks_f = OUT / "picks.json"
    picks = json.loads(picks_f.read_text(encoding="utf-8")) if picks_f.exists() else {}
    key = f"{query}|{limit}"
    if key not in picks:
        picks[key] = _anki_ids(query, limit)
        OUT.mkdir(parents=True, exist_ok=True)
        picks_f.write_text(json.dumps(picks, ensure_ascii=False, indent=1), encoding="utf-8")
    return picks[key]


def _anki_ids(query: str, limit: int) -> list[str]:
    cids = call("findCards", query=query)
    cards = sorted(call("cardsInfo", cards=cids), key=lambda c: c["due"]) if cids else []
    nids = list(dict.fromkeys(c["note"] for c in cards))
    tags = {n["noteId"]: n["tags"] for n in call("notesInfo", notes=nids)} if nids else {}
    out = []
    for n in nids[:limit]:
        ident = next((t[4:] for t in tags[n] if t.startswith("id::")), None)
        if not ident:  # an older domain built before notes carried their id: give it one so a sprint deck can borrow it
            ident = f"anki-{n}"
            call("addTags", notes=[n], tags=f"id::{ident}")
        out.append(ident)
    return out


# The 2026-11 refresh: problems in the company tag lists and the recent OA reports (sliding-window substring, spreadsheet
# column notation) that the September kit did not have; 2484 and 2603 are not on the tree and are left out.
LC_RECENT = ["design-circular-queue", "longest-substring-without-repeating-characters", "minimum-window-substring",
             "excel-sheet-column-title"]
SIBLINGS = 8   # same-pattern problems per leaf: 19 problems open about a hundred


def lc_plan(targets: list[str]) -> list[dict]:
    """One sub-deck per pattern (tree leaf), in the order its first target is listed: the leaf's learning card, the
    targets' own tree cards, then the recognition questions of the targets and of up to SIBLINGS more problems of the
    same leaf (most asked first). A recognition question's back carries the problem's whole tree card."""
    import daily_quiz as dq
    import lc_tree
    tree = dq.tree_cards()
    have = {c["slug"] for c in tree.values()}
    num = {c["slug"]: n for n, c in tree.items()}
    recog = {}
    for q in dq.jsonl("recog.jsonl"):
        recog.setdefault(dq.lc_number(q.get("title", "")), q)
    leaf_of, info = {}, {}
    for lst in lc_tree.build()["lists"]:
        for path, leaf in lc_tree.leaves(lst):
            for s in leaf["problems"]:
                if s not in leaf_of:
                    leaf_of[s] = leaf["id"]
                    info.setdefault(leaf["id"], (path, [x for x in leaf["problems"] if x in have]))
    learn = {p.stem for p in (ROOT / "vault/interviews/core/leetcode/tree/cards").rglob("lct-learn-*.md")}
    groups: dict[str, list[str]] = {}
    for s in targets:
        if s in leaf_of:
            groups.setdefault(leaf_of[s], []).append(s)
    plan, tag = [], []
    for k, (lid, ts) in enumerate(groups.items(), 1):
        path, probs = info[lid]
        sibs = [p for p in probs if p not in ts][:SIBLINGS]
        qs = [recog[num[p]] for p in ts + sibs if num.get(p) in recog]
        tag += [(int(q["note"]), q["id"]) for q in qs]
        ids = ([lc_tree.card_id(lid)] if lc_tree.card_id(lid) in learn else []) + [f"lct-{s}" for s in ts] + [q["id"] for q in qs]
        generic = {"综合应用", "其他", "基础", "进阶", "求最小", "求最大", "设计"}   # a leaf name that needs its parent to say anything
        name = " · ".join(path[-2:]) if path[-1] in generic or path[-1].startswith("其他") or "/" in path[-1] else path[-1]
        if path[-1] == "基础":
            name = " · ".join(path[-3:-1])
        plan.append({"label": f"{k:02d} {name}", "ids": ids})
    for nid, qid in tag:   # recognition notes carry recog::id:: tags; the sprint deck borrows by id::
        call("addTags", notes=[nid], tags=f"id::{qid}")
    return plan


def main() -> int:
    bt = ROOT / "vault/private/braintree/cards"
    bt_ids = [fm(f)["id"] for s in BT_SLUGS for f in sorted((bt / s).glob("*.md"))] if bt.exists() else []
    tour = [f"hi-ov-{s}-{k}" for s in TOUR for k in ("1-map", "2-options", "3-when")]
    plan = [
        {"label": "01 招聘方电话", "ids": company(["call"])},
        {"label": "02 公司与岗位", "ids": company(["company"])},
        {"label": "03 编程题", "ids": company(["coding"]) + company(["traps"])},   # code reading sits with coding
        {"label": "04 经理面与行为面", "ids": company(["hm"])},
        {"label": "05 项目深挖", "ids": company(["deepdive"]) + bt_ids},
        {"label": "06 Python 内功", "ids": vault_ids(ROOT / "vault/domains/python/cards", PY_LEAVES, 3)},
        {"label": "07 数据处理", "ids": company(["data"])},
        {"label": "08 设计轮", "ids": company(["design"]) + tour},
        {"label": "09 金融常识", "ids": company(["finance"])
         + anki_ids('"deck:📦 其他::Quant Infrastructure::02 Data Correctness"', 25)
         + anki_ids('"deck:📦 其他::Markets & Factors::01 Return Foundations"', 12)},
        {"label": "10 AI 与 LLM 产品", "ids": anki_ids('"deck:AI 应用工程::01 先修：大模型的基本概念（从零）"', 99)
         + anki_ids('"deck:AI 应用工程::02 起点：什么时候该做、怎么选"', 99)},
        {"label": "11 谈判", "ids": anki_ids('"deck:职业发展与谈判::05 Compensation anatomy"', 99)
         + anki_ids('"deck:职业发展与谈判::06 Negotiation"', 99)},
    ]
    tagged = [i[4:] for i in anki_ids('"tag:公司::Millennium"', 99) if i[4:] not in LC_SEEN]
    lc = lc_plan(LC_SEEN + tagged + [s for s in LC_RECENT if s not in LC_SEEN + tagged])
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=1), encoding="utf-8")
    (OUT / "lc_plan.json").write_text(json.dumps(lc, ensure_ascii=False, indent=1), encoding="utf-8")
    for p in plan + lc:
        print(f"{len(p['ids']):4}  {p['label']}")
    print(f"{sum(len(p['ids']) for p in plan)} + {sum(len(p['ids']) for p in lc)} cards")
    return 0


if __name__ == "__main__":
    sys.exit(main())
