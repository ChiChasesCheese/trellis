#!/usr/bin/env python3
"""Synthesise a plausible review history so the loop can be seen working
before a single card has been reviewed.

`trellis pull` needs desktop Anki running; this needs nothing. It invents
Traces with a deterministic seed — some topics held, some slipping, some
never shown — writes them under a throwaway root, and prints the Brief
and the Feed exactly as the real commands would.

    python3 scripts/demo_traces.py            # print the Brief and Feed
    python3 scripts/demo_traces.py --keep DIR # leave the demo root behind

Nothing is written to traces/. The numbers are fiction and the file says
so, so a demo run can never be mistaken for your own history.
"""

from __future__ import annotations

import argparse
import random
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from trellis.cards import load_cards                      # noqa: E402
from trellis.skeleton import load_skeleton                # noqa: E402
from trellis.traces import Trace, TraceFile, save_traces  # noqa: E402

# Leaves whose branch matches one of these get a deliberately rough ride,
# so the Brief has something to point at. Everything else is drawn from a
# generally-healthy distribution.
STRUGGLING = ("distributed", "concurrency", "correctness", "async")


def synthesise(root: Path, out_root: Path, seed: int = 7) -> list[str]:
    rng = random.Random(seed)
    written: list[str] = []
    for skeleton_path in sorted((root / "skeleton").glob("*.yaml")):
        skeleton = load_skeleton(skeleton_path)
        cards_dir = root / "vault" / skeleton.domain / "cards"
        if not cards_dir.exists():
            continue
        cards, _ = load_cards(cards_dir)
        traces: dict[str, Trace] = {}
        for card in cards:
            # a third of the collection has never come up yet
            if rng.random() < 0.33:
                continue
            rough = card.node.split(".")[0] in STRUGGLING
            reps = rng.randint(3, 9) if rough else rng.randint(2, 25)
            lapses = rng.randint(1, max(2, reps // 2)) if rough else \
                rng.choice([0, 0, 0, 1, 2])
            interval = rng.choice([1, 2, 3, 5]) if rough else \
                rng.choice([8, 14, 21, 35, 60, 120])
            traces[card.id] = Trace(
                card_id=card.id, reps=reps, lapses=lapses, interval=interval,
                ease=round(rng.uniform(1.8, 2.7), 2),
                type=3 if (rough and rng.random() < 0.3) else 2,
            )
        if traces:
            path = out_root / "traces" / f"{skeleton.domain}.json"
            save_traces(path, TraceFile(
                domain=skeleton.domain,
                pulled_at="2026-08-30T06:00:00+00:00",
                traces=traces,
            ))
            written.append(f"{skeleton.domain}: {len(traces)} synthetic traces")
    return written


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--keep", type=Path, help="write the demo root here and "
                                              "leave it behind")
    ap.add_argument("--seed", type=int, default=7)
    args = ap.parse_args()

    root = Path(__file__).resolve().parent.parent
    out_root = args.keep or Path(tempfile.mkdtemp(prefix="trellis-demo-"))
    out_root.mkdir(parents=True, exist_ok=True)
    # The demo root borrows the real skeleton and vault and owns only its
    # own traces/, so nothing it does can touch your history.
    for name in ("skeleton", "vault"):
        link = out_root / name
        if not link.exists():
            link.symlink_to(root / name)

    for line in synthesise(root, out_root, args.seed):
        print(line, file=sys.stderr)
    print(file=sys.stderr)

    for argv in (["brief", "--print"], ["feed"]):
        print(f"$ trellis {' '.join(argv)}", flush=True)
        subprocess.run([sys.executable, "-m", "trellis.cli",
                        "--root", str(out_root), *argv], cwd=root, check=False)
        print()

    if not args.keep:
        shutil.rmtree(out_root, ignore_errors=True)
    else:
        print(f"demo root kept at {out_root}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
