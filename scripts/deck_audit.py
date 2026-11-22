"""Audit every Anki deck: size, progress, length outliers, duplicates, format problems. Read-only.

    uv run python scripts/deck_audit.py              # sync, read the collection, write sources/local/audit/
    uv run python scripts/deck_audit.py --no-sync    # skip the AnkiConnect sync
    uv run python scripts/deck_audit.py --sample 40  # notes per domain in the review packs (default 40)

Outputs (all under sources/local/audit/, gitignored: the collection holds private decks):
- summary.md        one table: per domain, notes / cards / seen / mature / suspended / lengths / flags / duplicates
- flags.tsv         one row per flagged note (domain, note id, flag, question start)
- dups.tsv          duplicate clusters: exact question, near-duplicate (shingle Jaccard >= --jaccard), with domains
- notes.jsonl       every note as plain text (id, domain, deck, model, tags, q, a, lengths) for other tools
- leaves.tsv / overlap.tsv  notes per leaf (Crumb), and leaf names that appear in more than one domain
- review/<domain>.md  a pack for a human or agent reviewer: random sample + the flagged notes, plain text

A note's domain is the root of its first tag that names a skeleton (skeleton/<d>.yaml), else its top-level deck
("📦 其他::X" counts as X). Daily view decks (1 今日计划 …) only move cards, so the tag decides.
Flags: empty, short (answer < 30 chars incl. code), long (prose > 1500 chars), english (CJK < 5% of prose),
meta (本卡/本题/如上/本章/本书…), no-source-line is not flagged (older decks never had one).
"""
from __future__ import annotations

import argparse
import collections
import html
import json
import os
import random
import re
import sqlite3
import statistics
import sys
import urllib.request
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "sources/local/audit"
COLLECTION = Path(os.path.expanduser("~/Library/Application Support/Anki2/User 1/collection.anki2"))
META = re.compile(r"本卡|本题|如上所述|上一张|本章|本书|这张卡|前文|见上文")
Q_FIELDS = ("Question", "Front", "Title", "Text")
A_FIELDS = ("Answer", "Back", "Body", "Extra", "Why", "Solution", "Key")


def sync() -> None:
    req = urllib.request.Request("http://127.0.0.1:8765", json.dumps({"action": "sync", "version": 6}).encode())
    try:
        urllib.request.urlopen(req, timeout=120).read()
    except OSError as exc:  # Anki closed: the collection on disk is still readable
        print(f"warning: no AnkiConnect sync ({exc}); reading the collection as it is", file=sys.stderr)


def plain(field: str) -> tuple[str, int, bool]:
    """(prose, code chars, has diagram) of one HTML field."""
    diagram = bool(re.search(r"<svg|<img", field))
    field = re.sub(r"<svg.*?</svg>", " ", field, flags=re.S)
    code = sum(len(re.sub(r"<[^>]+>", "", m)) for m in re.findall(r"<pre.*?</pre>", field, flags=re.S))
    field = re.sub(r"<pre.*?</pre>", " ", field, flags=re.S)
    field = re.sub(r"<(br|/p|/li|/tr|/div|/h\d)[^>]*>", "\n", field)
    text = html.unescape(re.sub(r"<[^>]+>", "", field))
    return re.sub(r"[ \t]+", " ", re.sub(r"\n\s*\n+", "\n", text)).strip(), code, diagram


def norm(text: str) -> str:
    return re.sub(r"[\W_]+", "", text.lower())


def load(domains: set[str]) -> list[dict]:
    db = sqlite3.connect(f"file:{COLLECTION}?mode=ro", uri=True)
    db.create_collation("unicase", lambda a, b: (a.lower() > b.lower()) - (a.lower() < b.lower()))
    models = dict(db.execute("select id, name from notetypes"))
    fields: dict[int, list[str]] = collections.defaultdict(list)
    for ntid, name in db.execute("select ntid, name from fields order by ntid, ord"):
        fields[ntid].append(name)
    decks = {i: n.replace("\x1f", "::") for i, n in db.execute("select id, name from decks")}
    cards: dict[int, list[tuple]] = collections.defaultdict(list)
    for nid, did, odid, ctype, queue, ivl, lapses in db.execute("select nid, did, odid, type, queue, ivl, lapses from cards"):
        cards[nid].append((decks.get(odid or did, "?"), ctype, queue, ivl, lapses))
    notes = []
    for nid, mid, tags, flds in db.execute("select id, mid, tags, flds from notes"):
        vals = dict(zip(fields[mid], flds.split("\x1f")))
        q_raw = next((vals[f] for f in Q_FIELDS if vals.get(f)), "")
        a_raw = "\n".join(vals[f] for f in A_FIELDS if vals.get(f) and vals[f] != q_raw)
        q, _, qd = plain(q_raw)
        a, code, ad = plain(a_raw)
        tag_list = tags.split()
        deck = cards[nid][0][0] if cards[nid] else "?"
        top = deck.split("::")[1] if deck.startswith("📦") and "::" in deck else deck.split("::")[0]
        domain = next((t.split("::")[0] for t in tag_list if t.split("::")[0] in domains), top)
        cjk = len(re.findall(r"[一-鿿]", a))
        notes.append({
            "id": nid, "domain": domain, "deck": deck, "model": models.get(mid, "?"), "tags": tag_list,
            "ident": next((t[4:] for t in tag_list if t.startswith("id::")), ""),
            "crumb": plain(vals.get("Crumb", ""))[0],
            "q": q, "a": a, "q_len": len(q), "a_len": len(a), "code": code, "diagram": qd or ad,
            "cjk": cjk / max(1, len(re.sub(r"\s", "", a))),
            "cards": len(cards[nid]), "seen": sum(1 for c in cards[nid] if c[1] > 0),
            "mature": sum(1 for c in cards[nid] if c[3] >= 21), "suspended": sum(1 for c in cards[nid] if c[2] == -1),
            "lapses": sum(c[4] for c in cards[nid]),
        })
    return notes


def pack_name(dom: str, used: set[str]) -> str:
    """File name for a domain's review pack; domains that differ only in case get a numeric suffix (macOS folds case)."""
    base = re.sub(r"[^0-9A-Za-z一-鿿-]+", "_", dom)
    name, i = base, 2
    while name.lower() in used:
        name, i = f"{base}-{i}", i + 1
    used.add(name.lower())
    return name


def flags(n: dict) -> list[str]:
    out = []
    if not n["a"] and not n["code"] and "Cloze" not in n["model"]:
        out.append("empty")
    elif n["a_len"] + n["code"] < 30 and "Cloze" not in n["model"] and "Quick" not in n["model"]:
        out.append("short")
    if n["a_len"] > 1500:
        out.append("long")
    if n["a_len"] > 80 and n["cjk"] < 0.05:
        out.append("english")
    if META.search(n["a"]) or META.search(n["q"]):
        out.append("meta")
    return out


def duplicates(notes: list[dict], jaccard: float) -> list[tuple[str, list[dict]]]:
    clusters: list[tuple[str, list[dict]]] = []
    by_q: dict[str, list[dict]] = collections.defaultdict(list)
    for n in notes:
        key = norm(n["q"])
        if len(key) >= 12:
            by_q[key].append(n)
    exact_ids = set()
    for group in by_q.values():
        if len(group) > 1:
            clusters.append(("exact-q", group))
            exact_ids.update(x["id"] for x in group)
    # near-duplicates: 5-gram shingles of question + answer start; candidates share one of the 6 smallest hashes
    shingles: dict[int, set[int]] = {}
    buckets: dict[int, list[int]] = collections.defaultdict(list)
    by_id = {n["id"]: n for n in notes}
    for n in notes:
        text = norm(n["q"] + n["a"][:500])
        if len(text) < 40:
            continue
        s = {zlib.crc32(text[i:i + 5].encode()) for i in range(len(text) - 4)}
        shingles[n["id"]] = s
        for h in sorted(s)[:6]:
            buckets[h].append(n["id"])
    parent: dict[int, int] = {}

    def find(x: int) -> int:
        while parent.setdefault(x, x) != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    seen_pairs = set()
    for ids in buckets.values():
        if not 1 < len(ids) <= 40:
            continue
        for i, a in enumerate(ids):
            for b in ids[i + 1:]:
                if (a, b) in seen_pairs:
                    continue
                seen_pairs.add((a, b))
                sa, sb = shingles[a], shingles[b]
                if len(sa & sb) / len(sa | sb) >= jaccard:
                    parent[find(a)] = find(b)
    groups: dict[int, list[int]] = collections.defaultdict(list)
    for x in list(parent):
        groups[find(x)].append(x)
    for ids in groups.values():
        if len(ids) > 1 and not all(i in exact_ids for i in ids):
            clusters.append(("near", [by_id[i] for i in ids]))
    return clusters


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--no-sync", action="store_true")
    ap.add_argument("--sample", type=int, default=40)
    ap.add_argument("--jaccard", type=float, default=0.6)
    args = ap.parse_args()
    if not args.no_sync:
        sync()
    domains = {p.stem for p in (ROOT / "skeleton").glob("*.yaml")}
    notes = load(domains)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "review").mkdir(exist_ok=True)
    with (OUT / "notes.jsonl").open("w", encoding="utf-8") as fh:
        for n in notes:
            fh.write(json.dumps(n, ensure_ascii=False) + "\n")
    clusters = duplicates(notes, args.jaccard)
    dup_extra: collections.Counter = collections.Counter()   # redundant notes per domain (cluster size - 1)
    dup_cross = 0
    in_dup: dict[int, str] = {}
    with (OUT / "dups.tsv").open("w", encoding="utf-8") as fh:
        fh.write("kind\tsize\tdomains\tnote ids\tquestion\n")
        for kind, group in sorted(clusters, key=lambda c: -len(c[1])):
            doms = sorted({g["domain"] for g in group})
            dup_cross += len(doms) > 1
            for g in group[1:]:
                dup_extra[g["domain"]] += 1
            for g in group:
                in_dup[g["id"]] = kind
            fh.write(f"{kind}\t{len(group)}\t{','.join(doms)}\t{','.join(str(g['id']) for g in group)}\t{group[0]['q'][:80]!r}\n")
    by_dom: dict[str, list[dict]] = collections.defaultdict(list)
    flag_rows = []
    for n in notes:
        n["flags"] = flags(n)
        by_dom[n["domain"]].append(n)
        for f in n["flags"]:
            flag_rows.append(f"{n['domain']}\t{n['id']}\t{f}\t{n['q'][:70]!r}")
    (OUT / "flags.tsv").write_text("domain\tnote\tflag\tquestion\n" + "\n".join(flag_rows) + "\n", encoding="utf-8")
    head = ("| domain | notes | cards | seen | mature | susp | med Q | med A | short | long | english | meta | dup extra | diagram |\n"
            "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|\n")
    rows, total = [], collections.Counter()
    rng = random.Random(20261121)
    used: set[str] = set()
    for dom, ns in sorted(by_dom.items(), key=lambda kv: -len(kv[1])):
        c = collections.Counter(f for n in ns for f in n["flags"])
        cards = sum(n["cards"] for n in ns)
        seen = sum(n["seen"] for n in ns)
        row = {"notes": len(ns), "cards": cards, "seen": seen, "mature": sum(n["mature"] for n in ns),
               "susp": sum(n["suspended"] for n in ns), "short": c["short"] + c["empty"], "long": c["long"],
               "english": c["english"], "meta": c["meta"], "dup": dup_extra[dom]}
        total.update(row)
        rows.append(f"| {dom} | {len(ns)} | {cards} | {seen} ({100 * seen // max(1, cards)}%) | {row['mature']} | {row['susp']} "
                    f"| {int(statistics.median(n['q_len'] for n in ns))} | {int(statistics.median(n['a_len'] for n in ns))} "
                    f"| {row['short']} | {row['long']} | {row['english']} | {row['meta']} | {row['dup']} "
                    f"| {100 * sum(n['diagram'] for n in ns) // len(ns)}% |")
        flagged = [n for n in ns if n["flags"] or n["id"] in in_dup]
        sample = rng.sample(ns, min(args.sample, len(ns)))
        pack = [f"# {dom}: {len(ns)} notes — review pack ({len(sample)} random, then up to 60 flagged)\n"]
        for label, group in (("random", sample), ("flagged", flagged[:60])):
            for n in group:
                marks = ",".join(n["flags"] + ([f"dup:{in_dup[n['id']]}"] if n["id"] in in_dup else []))
                pack.append(f"\n## [{label}] note {n['id']} {n['ident']} · {n['model']} · A {n['a_len']} chars, code {n['code']}"
                            f"{' · ' + marks if marks else ''}\n**Q:** {n['q'][:600]}\n\n**A:** {n['a'][:1800]}\n")
        (OUT / "review" / f"{pack_name(dom, used)}.md").write_text("".join(pack), encoding="utf-8")
    # leaves.tsv: how many notes each leaf (Crumb) holds; overlap.tsv: leaf names taught in more than one domain
    leaf_count: collections.Counter = collections.Counter((n["domain"], n["crumb"].split("›")[-1].strip()) for n in notes if n["crumb"])
    (OUT / "leaves.tsv").write_text("domain\tleaf\tnotes\n" + "\n".join(
        f"{d}\t{leaf}\t{c}" for (d, leaf), c in sorted(leaf_count.items(), key=lambda kv: (kv[0][0], -kv[1]))) + "\n", encoding="utf-8")
    by_leaf: dict[str, dict[str, int]] = collections.defaultdict(dict)
    for (d, leaf), c in leaf_count.items():
        key = norm(re.sub(r"[（(].*?[)）]", "", leaf))
        if len(key) >= 3:
            by_leaf[key][d] = by_leaf[key].get(d, 0) + c
    shared = {k: v for k, v in by_leaf.items() if len(v) > 1}
    (OUT / "overlap.tsv").write_text("leaf\tdomains\tnotes\n" + "\n".join(
        f"{k}\t{','.join(f'{d}:{c}' for d, c in sorted(v.items()))}\t{sum(v.values())}"
        for k, v in sorted(shared.items(), key=lambda kv: -sum(kv[1].values()))) + "\n", encoding="utf-8")
    tot = (f"| **total** | {total['notes']} | {total['cards']} | {total['seen']} ({100 * total['seen'] // max(1, total['cards'])}%) "
           f"| {total['mature']} | {total['susp']} | | | {total['short']} | {total['long']} | {total['english']} | {total['meta']} "
           f"| {total['dup']} | |")
    kinds = collections.Counter(k for k, _ in clusters)
    summary = (f"# Deck audit\n\n{len(notes)} notes; duplicate clusters: {kinds['exact-q']} exact-question, {kinds['near']} near "
               f"(Jaccard ≥ {args.jaccard}); {dup_cross} clusters span more than one domain; {total['dup']} notes are redundant "
               f"copies (cluster size − 1).\n\n{head}" + "\n".join(rows) + "\n" + tot + "\n")
    (OUT / "summary.md").write_text(summary, encoding="utf-8")
    print(summary)
    return 0


if __name__ == "__main__":
    sys.exit(main())
