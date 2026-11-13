"""Mock interview → weak-spot cards on the question it was about (Chi, 2026-11-12: a mock most days, on the day's deep dive).

    uv run python scripts/mock_fix.py pending                 # recorded mocks not handled yet, each with its likely question
    uv run python scripts/mock_fix.py start <folder> [topic]  # keep the mock locally; print where and how to write the cards
    uv run python scripts/mock_fix.py place <topic> [--no-deal]  # check, import, and deal the question's deck again

The mocks are recorded by the sysdesign-board tool into `mocks_dir` (plan config; default
~/Code/trellis/vault/system_design_mocks/<name>/: recap.md, transcript.md, architecture-final.png). The cards are
written by hand or by an agent following research/sysdesign/MOCK_FIX_DAILY.md, into
vault/domains/hello-interview/cards/premium/mockfix/<topic>/ (local only), with ids containing -mockfix-: the deep dive
deals them first, as part 0 of the question, and `place` makes the mock's question today's deep dive. Every card must be mapped to the question's exam points in
sources/local/plan/kp/questions/<topic>.json before `place` imports it.
"""
from __future__ import annotations

import json
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))
PLAN = ROOT / "sources/local/plan"
KEPT = PLAN / "mocks"
DONE = KEPT / "processed.json"
CARDS = ROOT / "vault/domains/hello-interview/cards/premium/mockfix"
MARK = "-mockfix-"


def mocks_dir() -> Path:
    cfg = json.loads((PLAN / "config.json").read_text(encoding="utf-8"))
    return Path(cfg.get("mocks_dir", "~/Code/trellis/vault/system_design_mocks")).expanduser()


def rel(p: Path) -> str:
    return str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p)


def processed() -> dict:
    return json.loads(DONE.read_text(encoding="utf-8")) if DONE.exists() else {}


def skeleton():
    from trellis.skeleton import load_skeleton
    return load_skeleton(ROOT / "skeleton/sysdesign.yaml")


def questions() -> dict[str, str]:
    import deep_dive
    sk = skeleton()
    return {n.id: n.title for n in sk.by_id.values() if deep_dive.is_question(n.path()[0].id, n.id) and n.parent and n.parent.id in ("s05", "tt.sd")}


def guess(folder: Path, qs: dict[str, str]) -> str | None:
    """The mock's question: today's deep dive when the names agree, else the question whose name the folder or recap carries."""
    import deep_dive
    text = folder.name.replace("_", " ").lower() + " " + ((folder / "recap.md").read_text(encoding="utf-8")[:400].lower() if (folder / "recap.md").exists() else "")
    words = lambda s: {w for w in re.split(r"[^a-z0-9]+", s.lower()) if len(w) > 2}  # noqa: E731
    best = max(qs, key=lambda q: len(words(q + " " + qs[q]) & words(text)), default=None)
    current = deep_dive.load().get("current")
    if current and words(current + " " + qs.get(current, "")) & words(text):
        return current
    return best if best and words(best + " " + qs[best]) & words(text) else current


def pending() -> int:
    qs, done = questions(), processed()
    found = [f for f in sorted(mocks_dir().iterdir()) if f.is_dir() and f.name not in done] if mocks_dir().exists() else []
    for f in found:
        q = guess(f, qs)
        print(f"{f.name}\t{q or '?'}\t{qs.get(q, '')}")
    if not found:
        print("no new mock")
    return 0


def node_for(topic: str):
    """Where the cards hang: the question's 补充 child when it has one, else its last child, else the question itself."""
    q = skeleton().by_id[topic]
    kids = q.children
    return next((k for k in kids if k.id.endswith(".more")), kids[-1] if kids else q)


def card_files(topic: str) -> list[Path]:
    return sorted((CARDS / topic).glob(f"*{MARK}*.md"))


def start(folder: str, topic: str | None) -> int:
    src = mocks_dir() / folder
    if not src.is_dir():
        print(f"no mock folder {src}")
        return 2
    qs = questions()
    topic = topic or guess(src, qs)
    if topic not in qs:
        print(f"which question? pass a topic id, e.g. {next(iter(qs))}")
        return 2
    day = date.today().isoformat()
    keep = KEPT / f"{day}-{folder}"
    keep.mkdir(parents=True, exist_ok=True)
    for f in src.iterdir():
        if f.is_file():
            shutil.copy2(f, keep / f.name)
    done = processed()
    done[folder] = {"topic": topic, "day": day, "kept": rel(keep), "placed": False}
    DONE.write_text(json.dumps(done, ensure_ascii=False, indent=1), encoding="utf-8")
    node = node_for(topic)
    kp = json.loads((ROOT / f"sources/local/plan/kp/questions/{topic}.json").read_text(encoding="utf-8"))
    points = [n["kp"] for n in kp.get("needs", [])] + [o["id"] for o in kp.get("own", [])]
    slug = topic.split(".")[-1]
    print(f"question: {topic} {qs[topic]}")
    print(f"mock kept: {rel(keep)} (recap.md, transcript.md)")
    print(f"write cards into: {rel(CARDS / topic)}/")
    print(f"  id: hi-{slug}{MARK}{day.replace('-', '')[2:]}-NN-<slug>   node: {node.id}   step: {next_step(node.id)} upwards")
    print(f"  map each card in: sources/local/plan/kp/questions/{topic}.json → \"cards\"")
    print("  exam points of this question: " + " ".join(points))
    return 0


def next_step(node: str) -> int:
    steps = [int(m.group(1)) for f in (ROOT / "vault/domains").rglob("*.md")
             if f"node: {node}" in (t := f.read_text(encoding="utf-8", errors="ignore")[:400]) and (m := re.search(r"^step: (\d+)", t, re.M))]
    return max(steps, default=0) + 1


def place(topic: str, deal: bool) -> int:
    files = card_files(topic)
    if not files:
        print(f"no {MARK} cards in {rel(CARDS / topic)}")
        return 2
    ids = [re.search(r"^id: (\S+)", f.read_text(encoding="utf-8"), re.M).group(1) for f in files]
    kp = json.loads((ROOT / f"sources/local/plan/kp/questions/{topic}.json").read_text(encoding="utf-8"))
    known = {n["kp"] for n in kp.get("needs", [])} | {o["id"] for o in kp.get("own", [])}
    unmapped = [i for i in ids if not kp.get("cards", {}).get(i)]
    unknown = sorted({k for i in ids for k in kp.get("cards", {}).get(i, []) if k not in known})
    if unmapped or unknown:
        print("not placed: map every card to this question's exam points first")
        print("  unmapped: " + " ".join(unmapped) if unmapped else "", "\n  unknown points: " + " ".join(unknown) if unknown else "")
        return 1
    v = subprocess.run(["uv", "run", "trellis", "--domain", "sysdesign", "validate"], cwd=ROOT, capture_output=True, text=True)
    if " 0 error(s)" not in v.stdout + v.stderr:
        print((v.stdout + v.stderr).strip()[-1500:])
        return 1
    listed = PLAN / "mocks" / ".ids.txt"  # exactly these ids: anki_refresh adds the missing ones and updates the rest
    listed.write_text("\n".join(ids) + "\n", encoding="utf-8")
    r = subprocess.run(["uv", "run", "python", "scripts/anki_refresh.py", "--add", f"@{listed}", "sysdesign"], cwd=ROOT, capture_output=True, text=True)
    print((r.stdout + r.stderr).strip()[-600:])
    if r.returncode:
        return 1
    import deep_dive
    state = deep_dive.load()
    if state.get("current") != topic:  # the mock's question becomes today's, so its cards are dealt now
        state["current"], state["since"] = topic, date.today().isoformat()
        deep_dive.STATE.write_text(json.dumps(state, ensure_ascii=False, indent=1), encoding="utf-8")
    if deal:
        r = subprocess.run(["uv", "run", "python", "scripts/study_plan.py", "deep"], cwd=ROOT, capture_output=True, text=True)
        print((r.stdout or r.stderr).strip().splitlines()[-1])
    done = processed()
    for v in done.values():
        if v.get("topic") == topic:
            v["placed"] = True
    DONE.write_text(json.dumps(done, ensure_ascii=False, indent=1), encoding="utf-8")
    subprocess.run(["git", "checkout", "-q", "uv.lock"], cwd=ROOT)
    return 0


def main() -> int:
    a = sys.argv[1:]
    if a[:1] == ["pending"]:
        return pending()
    if a[:1] == ["start"] and len(a) >= 2:
        return start(a[1], a[2] if len(a) > 2 else None)
    if a[:1] == ["place"] and len(a) >= 2:
        return place(a[1], "--no-deal" not in a)
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
