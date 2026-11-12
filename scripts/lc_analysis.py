"""LeetCode analysis: for each pattern, technique, pitfall and Python idiom, how much it matters, how much of it is
covered and held, where the learner slips, and what to work on next.

    uv run python scripts/lc_analysis.py            # -> sources/local/lc/{analysis.json, index.html, METHOD.md}

Dimensions of a problem:
- 题型 (pattern): the knowledge-map file that lists it (vault/interviews/core/leetcode/knowledge-map/NN-*.md).
- 思路 (technique) and 易错点 (pitfall): tags from sources/local/lc/tags_*.jsonl against taxonomy.json, assigned by
  agents reading each solution's 一句话 / 识别 / 易错点 sections (research/lc-analysis/CLASSIFY_AGENT.md).
- 语法 (idiom): parsed from the solution's Python with `ast`: the library calls and constructs it relies on.

Importance of a problem: GitHub company-wise frequency only (liquidslr/leetcode-company-wise-problems: 470 companies,
LeetCode Premium frequency 0-100 per company and window, cloned to sources/local/lc/github/):
    0.6 x target   max over TikTok, ByteDance of 0.5 x All + 0.5 x max(30 days, 3 months, 6 months), /100
  + 0.4 x breadth  sum over all companies of All / 100, divided by the largest such sum (Two Sum)
Weights in sources/local/lc/config.json. The same score over every problem in the repository gives the deck's coverage
of what is asked (bank_coverage) and the 80/20 line.

Mastery of a problem: the mean card mastery (trellis/plan.card_mastery) over the Anki cards that open its solution.
Slip rate of a dimension: (Again + 0.5 x Hard + 15 x global rate) / (reviews + 15), i.e. smoothed toward the
learner's overall rate with 15 pseudo-reviews, so one forget cannot make a dimension look terrible. Priority of a dimension:
    importance x (1 - mastery) x clip(1 + 0.5 x (slip / global slip - 1), 1, 1.5)
so a weakness raises priority but never outweighs how much the dimension is asked.
"""
from __future__ import annotations

import ast
import json
import re
import sys
import time
from collections import defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from trellis.plan import card_mastery  # noqa: E402
from trellis.traces import Trace  # noqa: E402
sys.path.insert(0, str(ROOT / "scripts"))
from lc_data import DECKS, GH, LC, OUT, PLAN_DECKS, call, classic_lists, github_frequency, recent_slugs  # noqa: E402

DEFAULT = {"w_target": 0.6, "w_breadth": 0.4}

IDIOMS = {  # id -> (Chinese name, matcher over (module, attr) calls / names / node types)
    "heapq": "heapq 堆操作", "bisect": "bisect 二分插入", "deque": "deque 双端队列", "defaultdict": "defaultdict",
    "counter": "Counter 计数", "ordereddict": "OrderedDict", "lru-cache": "@cache / lru_cache 记忆化",
    "sort-key": "sorted / sort 的 key 与 reverse", "lambda": "lambda", "comprehension": "列表 / 字典 / 集合推导式",
    "generator": "生成器表达式", "enumerate-zip": "enumerate / zip", "itertools": "itertools", "accumulate": "accumulate 前缀和",
    "reduce": "functools.reduce", "inf": "float('inf') / math.inf 哨兵", "nonlocal": "nonlocal 闭包变量",
    "recursion-limit": "sys.setrecursionlimit", "divmod": "divmod / // 与 % 语义", "bit-ops": "位运算 & | ^ << >>",
    "ord-chr": "ord / chr 字符编码", "slicing": "切片与步长", "set-ops": "集合运算", "dict-get": "dict.get / setdefault",
    "walrus": ":= 海象运算符", "tuple-unpack": "元组解包与交换", "class-node": "自定义节点类 / dataclass",
    "string-methods": "字符串方法（join / split / isalnum …）", "math": "math 模块", "while-loop": "while 双指针 / 循环不变式",
}
BASIC_IDIOMS = {"while-loop", "tuple-unpack", "comprehension", "enumerate-zip", "generator", "divmod"}  # everywhere, so uninformative
CALLS = {("heapq", None): "heapq", ("bisect", None): "bisect", ("collections", "deque"): "deque", ("deque", None): "deque",
         ("collections", "defaultdict"): "defaultdict", ("defaultdict", None): "defaultdict", ("collections", "Counter"): "counter",
         ("Counter", None): "counter", ("collections", "OrderedDict"): "ordereddict", ("OrderedDict", None): "ordereddict",
         ("functools", "lru_cache"): "lru-cache", ("functools", "cache"): "lru-cache", ("lru_cache", None): "lru-cache",
         ("cache", None): "lru-cache", ("itertools", None): "itertools", ("accumulate", None): "accumulate",
         ("functools", "reduce"): "reduce", ("reduce", None): "reduce", ("sys", "setrecursionlimit"): "recursion-limit",
         ("divmod", None): "divmod", ("ord", None): "ord-chr", ("chr", None): "ord-chr", ("enumerate", None): "enumerate-zip",
         ("zip", None): "enumerate-zip", ("math", None): "math", ("dataclass", None): "class-node"}


# ---------------------------------------------------------------- problems and their dimensions


def problems() -> dict[str, dict]:
    rows = {}
    for line in (OUT / "sections.jsonl").read_text(encoding="utf-8").splitlines():
        r = json.loads(line)
        m = re.match(r"LC (\d+)\s*(.*)", r["title"])
        rows[r["slug"]] = {"slug": r["slug"], "title": r["title"], "num": int(m.group(1)) if m else None,
                           "patterns": [], "techniques": [], "pitfalls": [], "idioms": [], "insight": "",
                           "tiktok": 0.0, "tiktok_recent": False, "breadth": 0.0, "companies": 0}
    for f in sorted((LC / "knowledge-map").glob("[0-9][0-9]-*.md")):
        for line in f.read_text(encoding="utf-8").splitlines():
            m = re.search(r"\[\[tlc-([a-z0-9-]+?)-0-whole\|", line)
            if m and m.group(1) in rows:
                p = rows[m.group(1)]
                if f.stem not in p["patterns"]:
                    p["patterns"].append(f.stem)
    gh = github_frequency()
    for slug, p in rows.items():
        p.update(gh.get(slug, {}))
    sk = (ROOT / "skeleton/leetcode-tops.yaml").read_text(encoding="utf-8")
    branch_pattern = {"arrays-hashing": "01-hashing", "prefix-sum": "02-prefix-sum", "two-pointers": "03-two-pointers",
                      "sliding-window": "04-sliding-window", "stack": "05-monotonic-stack", "monotonic-stack": "05-monotonic-stack",
                      "binary-search": "06-binary-search", "heap": "07-heap", "intervals": "08-intervals", "linked-list": "09-linked-list",
                      "trees": "10-tree-dfs", "tree": "10-tree-dfs", "bst": "11-tree-bfs-bst", "graphs": "12-graph", "graph": "12-graph",
                      "topological-sort": "13-topo-sort", "union-find": "14-union-find", "shortest-path": "15-shortest-path",
                      "backtracking": "16-backtracking", "dp": "17-dp", "dynamic-programming": "17-dp", "greedy": "18-greedy",
                      "trie": "19-trie", "design": "20-design", "strings": "21-string", "string": "21-string", "math": "22-math-bit",
                      "bit-manipulation": "22-math-bit", "math-bit": "22-math-bit"}
    for m in re.finditer(r"- id: ([a-z0-9-]+)\.([a-z0-9-]+)\n", sk):
        branch, slug = m.group(1), m.group(2)
        if slug in rows and not rows[slug]["patterns"]:
            pat = branch_pattern.get(branch) or next((v for k, v in branch_pattern.items() if branch.startswith(k)), None)
            if pat:
                rows[slug]["patterns"].append(pat)
    tax = json.loads((OUT / "taxonomy.json").read_text(encoding="utf-8")) if (OUT / "taxonomy.json").exists() else {}
    for f in sorted(OUT.glob("tags_*.jsonl")):
        for line in f.read_text(encoding="utf-8").splitlines():
            t = json.loads(line)
            if t["slug"] in rows:
                rows[t["slug"]].update({k: t.get(k, []) for k in ("techniques", "pitfalls")})
                rows[t["slug"]]["insight"] = t.get("insight", "")
    tech_pattern = {t["id"]: t["pattern"] for t in tax.get("techniques", [])}
    for slug, p in rows.items():
        p["idioms"] = idioms(slug)
        if not p["patterns"] and p["techniques"] and p["techniques"][0] in tech_pattern:
            p["patterns"].append(tech_pattern[p["techniques"][0]])  # a problem outside the maps: its main technique's pattern
    return rows, tax


def idioms(slug: str) -> list[str]:
    text = (LC / "problems" / f"{slug}.md").read_text(encoding="utf-8")
    found = set()
    for code in re.findall(r"```python\n(.*?)```", text, re.S):
        try:
            tree = ast.parse(code)
        except SyntaxError:
            continue
        for n in ast.walk(tree):
            if isinstance(n, ast.Call):
                f = n.func
                if isinstance(f, ast.Attribute) and isinstance(f.value, ast.Name):
                    found.add(CALLS.get((f.value.id, f.attr)) or CALLS.get((f.value.id, None)))
                    if f.attr in ("sort",) and any(k.arg in ("key", "reverse") for k in n.keywords):
                        found.add("sort-key")
                    if f.attr in ("get", "setdefault") :
                        found.add("dict-get")
                    if f.attr in ("join", "split", "isalnum", "isdigit", "isalpha", "lower", "upper", "strip", "startswith"):
                        found.add("string-methods")
                elif isinstance(f, ast.Name):
                    found.add(CALLS.get((f.id, None)))
                    if f.id == "sorted" and any(k.arg in ("key", "reverse") for k in n.keywords):
                        found.add("sort-key")
                    if f.id == "float" and n.args and isinstance(n.args[0], ast.Constant) and "inf" in str(n.args[0].value):
                        found.add("inf")
            elif isinstance(n, (ast.ListComp, ast.DictComp, ast.SetComp)):
                found.add("comprehension")
            elif isinstance(n, ast.GeneratorExp):
                found.add("generator")
            elif isinstance(n, ast.Lambda):
                found.add("lambda")
            elif isinstance(n, ast.Nonlocal):
                found.add("nonlocal")
            elif isinstance(n, ast.NamedExpr):
                found.add("walrus")
            elif isinstance(n, ast.BinOp) and (isinstance(n.op, (ast.BitXor, ast.LShift, ast.RShift)) or (
                    isinstance(n.op, (ast.BitAnd, ast.BitOr)) and any(isinstance(x, ast.Constant) and isinstance(x.value, int)
                                                                     for x in (n.left, n.right)))):
                found.add("bit-ops")  # shifts, xor, or masking with an integer; & and | on sets or flags are not bit tricks
            elif isinstance(n, ast.BinOp) and isinstance(n.op, (ast.FloorDiv, ast.Mod)):
                found.add("divmod")
            elif isinstance(n, ast.Subscript) and isinstance(n.slice, ast.Slice) and n.slice.step is not None:
                found.add("slicing")
            elif isinstance(n, ast.BinOp) and isinstance(n.op, (ast.BitAnd, ast.BitOr, ast.Sub)) and isinstance(n.left, ast.Set):
                found.add("set-ops")
            elif isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Tuple) and isinstance(n.value, ast.Tuple):
                found.add("tuple-unpack")
            elif isinstance(n, ast.ClassDef) and n.name not in ("Solution",):
                found.add("class-node")
            elif isinstance(n, ast.While):
                found.add("while-loop")
            elif isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name) and n.value.id == "math" and n.attr == "inf":
                found.add("inf")
    found.discard(None)
    return sorted(found)


def importance(p: dict, cfg: dict) -> float:
    return cfg["w_target"] * p["tiktok"] + cfg["w_breadth"] * p["breadth"]


# ---------------------------------------------------------------- the learner's record


def card_slugs() -> dict[str, str]:
    """trellis card id -> problem slug, from every stub that opens a shared solution."""
    out = {}
    for f in (ROOT / "vault/interviews").rglob("*.md"):
        head = f.read_text(encoding="utf-8", errors="replace")[:600]
        m = re.search(r"^body: \S*?leetcode/problems/([a-z0-9-]+)", head, re.M)
        i = re.search(r"^id: (\S+)", head, re.M)
        if m and i:
            out[i.group(1)] = m.group(1)
    return out


PREFIXES = ("lca-", "lcb-", "lct-", "leetcode-q-", "leetcode-c-", "tlc-", "lt-")
IDIOM_WORDS = {"counter": "counter", "defaultdict": "defaultdict", "deque": "deque", "ordereddict": "ordereddict", "heapq": "heapq",
               "heap": "heapq", "bisect": "bisect", "sort": "sort-key", "sorted": "sort-key", "lambda": "lambda", "lru": "lru-cache",
               "cache": "lru-cache", "itertools": "itertools", "accumulate": "accumulate", "comprehension": "comprehension",
               "generator": "generator", "nonlocal": "nonlocal", "recursion": "recursion-limit", "divmod": "divmod",
               "bit": "bit-ops", "ord": "ord-chr", "slice": "slicing", "set": "set-ops", "dict": "dict-get", "walrus": "walrus",
               "string": "string-methods", "str": "string-methods", "math": "math", "inf": "inf", "dataclass": "class-node"}


def resolve(ident: str, slugs_of: dict[str, str], known: set[str]) -> tuple[str | None, str | None]:
    """(problem slug, idiom) for a card id: the stub's body, else the slug inside the id (lca-two-sum, lct-two-sum-x),
    else for a Python technique card (tlc-python-*, uth-python-*) the idiom it drills."""
    if ident in slugs_of:
        return slugs_of[ident], None
    if not ident:
        return None, None
    if ident.startswith(("tlc-python-", "uth-python-")):
        rest = ident.split("-python-", 1)[1]
        for word in re.split(r"[-_]", rest):
            if word in IDIOM_WORDS:
                return None, IDIOM_WORDS[word]
        return None, None
    rest = ident
    for pre in PREFIXES:
        if rest.startswith(pre):
            rest = rest[len(pre):]
            break
    best = None
    for slug in known:  # the longest known slug the rest of the id starts with
        if (rest == slug or rest.startswith(slug + "-")) and (best is None or len(slug) > len(best)):
            best = slug
    return best, None


def record(slugs_of: dict[str, str], known: set[str] = frozenset()):
    now = int(time.time() * 1000)
    q = " OR ".join(f'"deck:{d}"' for d in [*DECKS, *PLAN_DECKS])  # the daily decks borrow cards from these decks
    cids = call("findCards", query=q)
    info = []
    for i in range(0, len(cids), 500):
        info += call("cardsInfo", cards=cids[i:i + 500])
    nids = sorted({c["note"] for c in info})
    tags = {}
    for i in range(0, len(nids), 500):
        for n in call("notesInfo", notes=nids[i:i + 500]):
            tags[n["noteId"]] = n["tags"]
    seen = [c["cardId"] for c in info if c["reps"]]
    revs = call("getReviewsOfCards", cards=seen) if seen else {}
    per = defaultdict(lambda: {"cards": 0, "seen": 0, "mastery": [], "reviews": 0, "again": 0, "hard": 0, "last": 0, "logs": []})
    for c in info:
        ident = next((t[4:] for t in tags.get(c["note"], []) if t.startswith("id::")), None)
        if c["deckName"].startswith(PLAN_DECKS) and not (ident or "").startswith(PREFIXES):
            continue  # a system-design card in the plan
        slug, idiom = resolve(ident, slugs_of, known)
        key = slug or (f"idiom:{idiom}" if idiom else None)
        if not key:
            continue
        slug = key
        log = revs.get(str(c["cardId"]), [])
        tr = Trace(card_id=ident, reps=c["reps"], lapses=c["lapses"], interval=max(c["interval"], 0), type=c["type"],
                   last_review=max((r["id"] for r in log), default=0), delayed=sum(1 for r in log if r["type"] == 1 and r["ease"] > 1))
        s = per[slug]
        s["cards"] += 1
        s["seen"] += bool(c["reps"])
        s["mastery"].append(card_mastery(tr, now))
        s["reviews"] += len(log)
        s["again"] += sum(1 for r in log if r["ease"] == 1)
        s["hard"] += sum(1 for r in log if r["ease"] == 2)
        s["last"] = max(s["last"], tr.last_review)
        if log:
            s["logs"].append(sorted(log, key=lambda r: r["id"]))
    return per


def mastery_at(log: list[dict], t: int) -> float:
    """A card's mastery as it stood at time t, rebuilt from its review log."""
    past = [r for r in log if r["id"] < t]
    if not past:
        return 0.0
    last = past[-1]
    tr = Trace(card_id="", reps=len(past), lapses=sum(1 for r in past if r["ease"] == 1 and r["type"] == 1),
               interval=max(last["ivl"], 0), type=2 if last["ivl"] > 0 else 1, last_review=last["id"], delayed=sum(1 for r in past if r["type"] == 1 and r["ease"] > 1))
    return card_mastery(tr, t)


WEEK = 7 * 86_400_000
HELD = 0.5  # a problem counts as held once its best card is past this mastery (about a 4-day interval)


def views(rows: dict[str, dict], per: dict, names: dict[str, str]) -> dict[str, list[dict]]:
    """Progress over fixed problem sets: the classic lists, each target company's last six months, each module. A
    problem's mastery is its best card, so learning it in any deck (TikTok, Amazon, a module) counts everywhere."""
    now = int(time.time() * 1000)
    points = [now - k * WEEK for k in range(8, -1, -1)]
    hist = {slug: [max((mastery_at(log, t) for log in s["logs"]), default=0.0) for t in points] for slug, s in per.items()}
    by_num = {p["num"]: slug for slug, p in rows.items() if p["num"]}
    other = classic_lists()

    def view(name: str, members: list[str], note: str = "") -> dict:
        n = len(members)
        h = [sum(hist.get(m, [0.0] * len(points))[i] for m in members) / n if n else 0.0 for i in range(len(points))]
        seen = [sum(1 for m in members if hist.get(m) and hist[m][i] > 0) for i in range(len(points))]
        held = [sum(1 for m in members if hist.get(m) and hist[m][i] >= HELD) for i in range(len(points))]
        return {"name": name, "note": note, "n": n, "in_deck": sum(1 for m in members if m in rows),
                "mastery": h[-1], "seen": seen[-1], "held": held[-1],
                "hist": [{"t": t, "mastery": a, "seen": b, "held": c} for t, a, b, c in zip(points, h, seen, held)],
                "missing": [m for m in members if m not in rows]}

    lists = [view(label, [by_num.get(x, f"#{x}") for x in other[key]])
             for label, key in (("Blind 75", "Blind 75"), ("NeetCode 150", "NeetCode 150"), ("LeetCode Hot 100", "LeetCode Hot 100"),
                                ("Top Interview 150", "Top Interview 150"))]  # progress only; lists never enter importance
    tiktok = sorted(set(recent_slugs("TikTok")) | set(recent_slugs("ByteDance")))
    companies = [view("TikTok / 字节 近半年", tiktok, "GitHub 公司题频里近 6 个月出现过的题"),
                 view("Amazon 近半年", recent_slugs("Amazon"), "GitHub 公司题频里近 6 个月出现过的题")]
    modules = [view(names.get(pat, pat), sorted(slug for slug, p in rows.items() if p["patterns"] and p["patterns"][0] == pat))
               for pat in sorted(names)]
    return {"lists": lists, "companies": companies, "modules": [m for m in modules if m["n"]]}


# ---------------------------------------------------------------- aggregate


def analyse() -> dict:
    cfgf = OUT / "config.json"
    cfg = {**DEFAULT, **(json.loads(cfgf.read_text(encoding="utf-8")) if cfgf.exists() else {})}
    rows, tax = problems()
    per = record(card_slugs(), set(rows))
    tot_rev = sum(s["reviews"] for s in per.values())
    tot_slip = sum(s["again"] + 0.5 * s["hard"] for s in per.values())
    g = tot_slip / tot_rev if tot_rev else 0.05
    for slug, p in rows.items():
        s = per.get(slug)
        p["importance"] = importance(p, cfg)
        p["in_anki"] = bool(s)
        p["seen"] = bool(s and s["seen"])
        p["mastery"] = max(s["mastery"]) if s and s["mastery"] else 0.0  # the problem's best card: copies share one body
        p["reviews"], p["again"], p["hard"] = (s["reviews"], s["again"], s["hard"]) if s else (0, 0, 0)
    names = {"patterns": {f.stem: re.sub(r"^# ", "", f.read_text(encoding="utf-8").splitlines()[0])
                          for f in (LC / "knowledge-map").glob("[0-9][0-9]-*.md")},
             "techniques": {t["id"]: t["name"] for t in tax.get("techniques", [])},
             "pitfalls": {t["id"]: t["name"] for t in tax.get("pitfalls", [])},
             "idioms": IDIOMS}
    prior = 15.0  # pseudo-reviews pulling a dimension's slip rate toward the learner's overall rate
    dims = {}
    total_imp = sum(p["importance"] for p in rows.values()) or 1.0
    for dim in ("patterns", "techniques", "pitfalls", "idioms"):
        agg = defaultdict(lambda: {"imp": 0.0, "imp_seen": 0.0, "imp_held": 0.0, "rev": 0, "slip": 0.0, "problems": []})
        for p in rows.values():
            vals = p[dim]
            for k, v in enumerate(vals):
                share = 1.0 if dim in ("pitfalls", "idioms") else (1.0 if k == 0 else 0.5)
                a = agg[v]
                a["imp"] += p["importance"] * share
                a["imp_seen"] += p["importance"] * share * p["seen"]
                a["imp_held"] += p["importance"] * share * p["mastery"]
                a["rev"] += p["reviews"]
                a["slip"] += p["again"] + 0.5 * p["hard"]
                a["problems"].append(p["slug"])
        out = []
        for v, a in agg.items():
            mastery = a["imp_held"] / a["imp"] if a["imp"] else 0.0
            drill = per.get(f"idiom:{v}") if dim == "idioms" else None
            if drill and drill["mastery"]:  # cards that drill the idiom itself count as much as the problems that use it
                mastery = 0.5 * mastery + 0.5 * sum(drill["mastery"]) / len(drill["mastery"])
                a["rev"] += drill["reviews"]
                a["slip"] += drill["again"] + 0.5 * drill["hard"]
            slip = (a["slip"] + prior * g) / (a["rev"] + prior) if (a["rev"] + prior) else g
            boost = min(1.5, max(1.0, 1 + 0.5 * (slip / g - 1))) if g else 1.0
            out.append({"id": v, "name": names[dim].get(v, v), "importance": a["imp"] / total_imp,
                        "coverage": a["imp_seen"] / a["imp"] if a["imp"] else 0.0, "mastery": mastery,
                        "reviews": a["rev"], "slip": slip, "slip_ratio": slip / g if g else 1.0,
                        "priority": 0.0 if (dim == "idioms" and v in BASIC_IDIOMS) else a["imp"] / total_imp * (1 - mastery) * boost,
                        "basic": dim == "idioms" and v in BASIC_IDIOMS, "problems": a["problems"]})
        dims[dim] = sorted(out, key=lambda x: -x["priority"])
    bank = {slug: importance(o, cfg) for slug, o in github_frequency().items()}
    bank_total = sum(bank.values()) or 1.0
    bank_rank = sorted(bank, key=lambda x: -bank[x])
    acc, bank_n80 = 0.0, 0
    for i, slug in enumerate(bank_rank):
        acc += bank[slug]
        if acc >= 0.8 * bank_total:
            bank_n80 = i + 1
            break
    in_deck = set(rows)
    missing = [{"slug": x, "importance": bank[x]} for x in bank_rank[:300] if x not in in_deck]
    bank_stats = {"problems": len(bank), "companies": sum(1 for x in GH.iterdir() if x.is_dir() and not x.name.startswith(".")),
                  "coverage": sum(v for k, v in bank.items() if k in in_deck) / bank_total, "n80": bank_n80,
                  "top300_in_deck": sum(1 for x in bank_rank[:300] if x in in_deck), "missing_top300": missing,
                  "deck_in_top_n80": sum(1 for x in bank_rank[:bank_n80] if x in in_deck)}
    ranked = sorted(rows.values(), key=lambda p: -p["importance"])
    cum, n80 = 0.0, 0
    for i, p in enumerate(ranked):
        cum += p["importance"]
        if cum >= 0.8 * total_imp:
            n80 = i + 1
            break
    return {"generated": datetime.now().strftime("%Y-%m-%d %H:%M"), "global_slip": g, "reviews": tot_rev, "config": cfg,
            "views": views(rows, per, names["patterns"]), "problems": rows, "dims": dims, "pareto_n80": n80, "n": len(rows), "bank": bank_stats,
            "held": sum(p["importance"] * p["mastery"] for p in rows.values()) / total_imp,
            "covered": sum(p["importance"] * p["seen"] for p in rows.values()) / total_imp,
            "tagged": sum(1 for p in rows.values() if p["techniques"])}


def main() -> int:
    call("sync")  # reviews done on the phone are only here after a sync
    a = analyse()
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "analysis.json").write_text(json.dumps(a, ensure_ascii=False, indent=1), encoding="utf-8")
    tpl = ROOT / "scripts/lc_analysis.html"
    if tpl.exists():
        (OUT / "index.html").write_text(tpl.read_text(encoding="utf-8").replace("/*DATA*/null", json.dumps(a, ensure_ascii=False)),
                                        encoding="utf-8")
    top = {d: [x["name"] for x in v[:5]] for d, v in a["dims"].items()}
    print(f"{a['n']} problems, {a['tagged']} tagged · covered {a['covered']:.0%} · held {a['held']:.1%} · "
          f"top {a['pareto_n80']} = 80% · slip {a['global_slip']:.1%} over {a['reviews']} reviews")
    b = a["bank"]
    print(f"GitHub: {b['companies']} companies, {b['problems']} problems · deck covers {b['coverage']:.0%} of frequency · "
          f"80% of it in top {b['n80']} (deck has {b['deck_in_top_n80']}) · top 300 in deck {b['top300_in_deck']}")
    print("  missing from top 300:", ", ".join(m["slug"] for m in b["missing_top300"][:25]))
    for v in a["views"]["lists"] + a["views"]["companies"]:
        h = v["hist"]
        print(f"  {v['name']}: {v['n']} problems, {v['in_deck']} in deck · seen {v['seen']} · held {v['held']} · mastery {v['mastery']:.0%}"
              f" (8 weeks ago {h[0]['mastery']:.0%}, last week {h[-2]['mastery']:.0%})")
    for d, v in top.items():
        print(f"  {d}: {', '.join(v)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
