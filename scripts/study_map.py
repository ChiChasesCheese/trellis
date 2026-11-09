"""The system-design map as a website: a table of contents, an article per topic and question, and a mind map.

    uv run python scripts/study_map.py     # -> sources/local/plan/map/ (served with the dashboard; gitignored, it holds card text)

Left, the tree of domains, topics and exam points. Right, an article: for a topic its points, each with what to learn first, which
questions use it and in what role, and the cards that teach it, rendered exactly as in Anki; for a question the points its answer needs.
Prerequisites come from sources/local/plan/kp/dag.json when it exists. Card text and mastery stay local.
"""
from __future__ import annotations

import json
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import time
import zipfile
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
import plan_kp  # noqa: E402
import study_plan as S  # noqa: E402
from trellis.build import CSS  # noqa: E402
from trellis.plan import card_mastery  # noqa: E402

OUT = ROOT / "sources/local/plan/map"
SEP = "\x1f"


def built_fields() -> dict[str, list[str]]:
    """Card id -> its note fields, rendered as Anki shows them, from a package built the normal way and never imported."""
    folder = Path(tempfile.mkdtemp(prefix="map-build-"))
    apkg = folder / "s.apkg"
    r = subprocess.run(["uv", "run", "trellis", "--domain", S.DOMAIN, "build", "-o", str(apkg)], cwd=ROOT, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(r.stderr[-400:])
    with zipfile.ZipFile(apkg) as z:
        z.extract("collection.anki2", folder)
    db = sqlite3.connect(folder / "collection.anki2")
    out = {}
    for flds, tags in db.execute("select flds, tags from notes"):
        ident = next((t[4:] for t in tags.split() if t.startswith("id::")), None)
        if ident:
            out[ident] = flds.split(SEP)
    db.close()
    shutil.rmtree(folder, ignore_errors=True)
    return out


def cloze(html: str) -> str:
    """A cloze card read as an article: the hidden parts shown, marked."""
    return re.sub(r"\{\{c\d+::(.*?)(?:::[^{}]*)?\}\}", r'<mark class="cl">\1</mark>', html, flags=re.S)


def main() -> int:
    for _ in range(40):
        try:
            S.call("sync")
            break
        except RuntimeError:
            time.sleep(3)
    S.cfg_global.update(S.config())
    tree = S.Tree()
    cards, titles, base, edges = S.build_inputs(tree)
    traces, anki, _ = S.anki_state({c.id for c in cards})
    now = int(time.time() * 1000)
    fields = built_fields()
    st = S.kp_state
    pts, model, teach = st["points"], st["model"], st["teach"]
    m = {c.id: card_mastery(traces.get(c.id), now) for c in cards}
    held = model.mastery(m)
    total = sum(model.weight.values()) or 1.0
    req = plan_kp.required_by(pts)
    dag_file = ROOT / "sources/local/plan/kp/dag.json"
    pre: dict[str, list[str]] = json.loads(dag_file.read_text(encoding="utf-8")).get("edges", {}) if dag_file.exists() else {}
    post: dict[str, list[str]] = defaultdict(list)
    for k, ps in pre.items():
        for x in ps:
            post[x].append(k)
    title_of = lambda t: tree.title(t) if t in tree.node else t  # noqa: E731
    home = {c.id: c.topic for c in cards}
    base = re.escape(json.loads((ROOT / "sources/local/plan/config.json").read_text(encoding="utf-8")).get("map_url", "") or "\0")

    def local_links(text: str) -> str:
        """Footer links point at this site; one to a card that is not here (filed in another deck) becomes plain text."""
        def fix(m: re.Match) -> str:
            kind, rest, label = m.group(1), m.group(2), m.group(3)
            return label if kind == "c" and rest not in home else f'<a href="#{kind}/{rest}">{label}</a>'
        return re.sub(rf'<a href="{base}#([tpc])/([^"]+)">(.*?)</a>', fix, text)

    points = {}
    for k, meta in pts.meta.items():
        if k not in teach or k in plan_kp.META:
            continue
        rows = sorted(req.get(k, []), key=lambda r: -st["q_freq"].get(r[0], 0.0))
        n = Counter(r[1] for r in rows)
        points[k] = {"t": meta["title"], "s": meta.get("summary", ""), "core": bool(meta.get("core")), "kind": meta.get("kind", ""),
                     "w": model.weight.get(k, 0.0) / total, "m": held.get(k, 0.0), "n": [n["必讲"], n["追问"], n["加分"]],
                     "pre": [x for x in pre.get(k, []) if x in pts.meta], "post": [x for x in post.get(k, []) if x in pts.meta],
                     "q": [[q, title_of(q), role, why] for q, role, why in rows[:12]], "home": meta["topic"]}
    by_topic = defaultdict(list)
    for c in cards:
        by_topic[c.topic].append(c)
    leaf_pos = {n.id: i for i, n in enumerate(tree.sk.walk())}
    data_dir = OUT / "data"
    if OUT.exists():
        shutil.rmtree(OUT)
    data_dir.mkdir(parents=True)
    groups = {}
    for t, cs in by_topic.items():
        cs.sort(key=lambda c: (leaf_pos.get(c.leaf, 0), c.order))
        out_cards, topic_points = [], []
        for c in cs:
            f = fields.get(c.id)
            if not f:
                continue
            is_cloze = len(f) < 3 or "{{c" in f[0]
            ks = [k for k in pts.card.get(c.id, []) if k in points]
            topic_points += ks
            out_cards.append({"id": c.id, "t": titles.get(c.id, ""), "leaf": tree.title(c.leaf), "lv": c.level, "m": round(m[c.id], 2), "seen": bool(traces.get(c.id) and traces[c.id].reps),
                              "k": ks, "q": local_links(cloze(f[0]) if is_cloze else f[0]), "a": "" if is_cloze else local_links(f[1]), "len": c.length})
        (data_dir / f"{t}.json").write_text(json.dumps({"id": t, "cards": out_cards}, ensure_ascii=False), encoding="utf-8")
        wsum = sum(model.weight.get(k, 0.0) for k in dict.fromkeys(topic_points))
        g = tree.top(t)
        groups.setdefault(g, []).append({"id": t, "t": tree.title(t), "q": S.question_topic(tree, t), "n": len(out_cards), "seen": sum(1 for x in out_cards if x["seen"]),
                                         "w": wsum / total, "m": sum(held.get(k, 0.0) * model.weight.get(k, 0.0) for k in dict.fromkeys(topic_points)) / wsum if wsum else 0.0,
                                         "p": sorted(dict.fromkeys(topic_points), key=lambda k: -model.weight.get(k, 0.0)), "pos": leaf_pos.get(cs[0].leaf, 0)})
    roots = sorted((tree.sk.roots), key=lambda n: leaf_pos.get(n.id, 0))
    tree_out = [{"id": r.id, "t": r.title, "topics": sorted(groups[r.id], key=lambda x: x["pos"])} for r in roots if r.id in groups]
    needs = {q: [[n["kp"], n["role"], n.get("why", "")] for n in ns if n["kp"] in points] for q, ns in pts.needs.items()}
    own = {q: [[o["id"], o.get("role", ""), o["title"]] for o in os] for q, os in pts.own.items()}
    index = {"home": home, "tree": tree_out, "points": points, "needs": needs, "own": own, "covered": model.coverage(m), "dag": bool(pre), "cards": sum(t["n"] for g in tree_out for t in g["topics"]),
             "seen": sum(t["seen"] for g in tree_out for t in g["topics"]), "generated": time.strftime("%Y-%m-%d %H:%M")}
    tpl = (ROOT / "scripts/study_map.html").read_text(encoding="utf-8")
    (OUT / "index.html").write_text(tpl.replace("/*CARD_CSS*/", CSS).replace("/*DATA*/null", json.dumps(index, ensure_ascii=False)), encoding="utf-8")
    size = sum(f.stat().st_size for f in OUT.rglob("*") if f.is_file())
    print(f"{index['cards']} cards, {len(points)} points, {len(tree_out)} domains, dag {'on' if pre else 'off'}, {size / 1e6:.1f} MB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
