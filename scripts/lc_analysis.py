"""LeetCode analysis: for each pattern, technique, pitfall and Python idiom, how much it matters, how much of it is
covered and held, where the learner slips, and what to work on next.

    uv run python scripts/lc_analysis.py            # -> sources/local/lc/{analysis.json, index.html, METHOD.md}

Dimensions of a problem:
- 题型 (pattern): the knowledge-map file that lists it (vault/interviews/core/leetcode/knowledge-map/NN-*.md).
- 思路 (technique) and 易错点 (pitfall): tags from sources/local/lc/tags_*.jsonl against taxonomy.json, assigned by
  agents reading each solution's 一句话 / 识别 / 易错点 sections (research/lc-analysis/CLASSIFY_AGENT.md).
- 语法 (idiom): parsed from the solution's Python with `ast`: the library calls and constructs it relies on.

Importance of a problem (config in sources/local/lc/config.json, defaults below), every input traceable:
    0.50 x TikTok/ByteDance company-tag frequency (LeetCode Premium 0-100, /100; x1.2 if asked in the last 6 months)
  + 0.15 x Amazon company-tag frequency
  + 0.25 x all-company popularity, 1 / (1 + rank / 50)
  + 0.10 x share of the four classic lists it is on (Blind 75, NeetCode 150, Hot 100, Top Interview 150)
Company frequencies come from the generated lists in vault/interviews/core/leetcode/companies/ (sources:
liquidslr/leetcode-company-wise-problems and snehasishroy/leetcode-companywise-interview-questions).

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
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from trellis.plan import card_mastery  # noqa: E402
from trellis.traces import Trace  # noqa: E402

LC = ROOT / "vault/interviews/core/leetcode"
OUT = ROOT / "sources/local/lc"
DECKS = ["LeetCode Tops", "LeetCode"]
LISTS = ["Blind 75", "NeetCode 150", "LeetCode Hot 100", "Top Interview 150"]
DEFAULT = {"w_tiktok": 0.50, "w_amazon": 0.15, "w_popularity": 0.25, "w_lists": 0.10, "recent_bonus": 1.2}

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


def call(action, **params):
    body = json.dumps({"action": action, "version": 6, "params": params}).encode()
    for _ in range(60):
        with urllib.request.urlopen(urllib.request.Request("http://127.0.0.1:8765", body), timeout=600) as r:
            out = json.load(r)
        if out["error"] and "lifecycle" in out["error"]:
            time.sleep(3)
            continue
        if out["error"]:
            raise RuntimeError(f"{action}: {out['error']}")
        return out["result"]
    raise RuntimeError("Anki stayed busy")


# ---------------------------------------------------------------- problems and their dimensions


def problems() -> dict[str, dict]:
    rows = {}
    for line in (OUT / "sections.jsonl").read_text(encoding="utf-8").splitlines():
        r = json.loads(line)
        m = re.match(r"LC (\d+)\s*(.*)", r["title"])
        rows[r["slug"]] = {"slug": r["slug"], "title": r["title"], "num": int(m.group(1)) if m else None,
                           "patterns": [], "techniques": [], "pitfalls": [], "idioms": [], "insight": "",
                           "tiktok": 0.0, "tiktok_recent": False, "amazon": 0.0, "rank": None, "lists": 0}
    for f in sorted((LC / "knowledge-map").glob("[0-9][0-9]-*.md")):
        for line in f.read_text(encoding="utf-8").splitlines():
            m = re.search(r"\[\[tlc-([a-z0-9-]+?)-0-whole\|", line)
            if m and m.group(1) in rows:
                p = rows[m.group(1)]
                if f.stem not in p["patterns"]:
                    p["patterns"].append(f.stem)
                p["lists"] = max(p["lists"], sum(1 for x in LISTS if x in line))
    for co, key in (("tiktok", "tiktok"), ("bytedance", "tiktok"), ("amazon", "amazon")):
        f = LC / "companies" / f"{co}.md"
        if not f.exists():
            continue
        for line in f.read_text(encoding="utf-8").splitlines():
            m = re.match(r"\|\s*(\d+)\s*\|\s*\[[^\]]+\]\(https://leetcode\.com/problems/([a-z0-9-]+)/\)\s*\|[^|]*\|\s*(\d+)\s*\|\s*(✓?)\s*\|", line)
            if m and m.group(2) in rows:
                p = rows[m.group(2)]
                freq = int(m.group(3)) / 100
                if freq > p[key]:
                    p[key] = freq
                if key == "tiktok" and m.group(4):
                    p["tiktok_recent"] = True
    sk = (ROOT / "skeleton/leetcode-tops.yaml").read_text(encoding="utf-8")
    for m in re.finditer(r"- id: [a-z0-9-]+\.([a-z0-9-]+)\n\s+title: [^\n]*\n\s+summary: ([^\n]*)", sk):
        slug, summary = m.group(1), m.group(2)
        r = re.search(r"热度第 (\d+) 名", summary)
        if slug in rows and r:
            rows[slug]["rank"] = int(r.group(1))
        if slug in rows:
            rows[slug]["lists"] = max(rows[slug]["lists"], sum(1 for x in LISTS if x in summary))
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
    tiktok = p["tiktok"] * (cfg["recent_bonus"] if p["tiktok_recent"] else 1.0)
    pop = 1 / (1 + p["rank"] / 50) if p["rank"] else 0.0
    return cfg["w_tiktok"] * tiktok + cfg["w_amazon"] * p["amazon"] + cfg["w_popularity"] * pop + cfg["w_lists"] * p["lists"] / 4


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
    q = " OR ".join(f'"deck:{d}"' for d in DECKS)
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
    per = defaultdict(lambda: {"cards": 0, "seen": 0, "mastery": [], "reviews": 0, "again": 0, "hard": 0, "last": 0})
    for c in info:
        ident = next((t[4:] for t in tags.get(c["note"], []) if t.startswith("id::")), None)
        slug, idiom = resolve(ident, slugs_of, known)
        key = slug or (f"idiom:{idiom}" if idiom else None)
        if not key:
            continue
        slug = key
        log = revs.get(str(c["cardId"]), [])
        tr = Trace(card_id=ident, reps=c["reps"], lapses=c["lapses"], interval=max(c["interval"], 0), type=c["type"],
                   last_review=max((r["id"] for r in log), default=0))
        s = per[slug]
        s["cards"] += 1
        s["seen"] += bool(c["reps"])
        s["mastery"].append(card_mastery(tr, now))
        s["reviews"] += len(log)
        s["again"] += sum(1 for r in log if r["ease"] == 1)
        s["hard"] += sum(1 for r in log if r["ease"] == 2)
        s["last"] = max(s["last"], tr.last_review)
    return per


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
        p["mastery"] = sum(s["mastery"]) / len(s["mastery"]) if s and s["mastery"] else 0.0
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
    ranked = sorted(rows.values(), key=lambda p: -p["importance"])
    cum, n80, cards80 = 0.0, 0, 0
    for i, p in enumerate(ranked):
        cum += p["importance"]
        if cum >= 0.8 * total_imp:
            n80 = i + 1
            break
    return {"generated": datetime.now().strftime("%Y-%m-%d %H:%M"), "global_slip": g, "reviews": tot_rev, "config": cfg,
            "problems": rows, "dims": dims, "pareto_n80": n80, "n": len(rows),
            "held": sum(p["importance"] * p["mastery"] for p in rows.values()) / total_imp,
            "covered": sum(p["importance"] * p["seen"] for p in rows.values()) / total_imp,
            "tagged": sum(1 for p in rows.values() if p["techniques"])}


def main() -> int:
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
    for d, v in top.items():
        print(f"  {d}: {', '.join(v)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
