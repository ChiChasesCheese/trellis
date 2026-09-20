"""Read the survey files and count, per problem, the independent sources that teach it.

    uv run python scripts/design_problem_survey.py            # frequency table
    uv run python scripts/design_problem_survey.py --names     # every canonical name seen, unmapped first

The survey agents normalised names on their own, so the same problem arrives
under several. ALIASES folds them; anything not in it stands as itself.
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

SURVEY = Path(__file__).resolve().parents[1] / "vault/domains/system-design/survey"
ROW = re.compile(r"^\|(.+)\|\s*$")


def rows():
    """(source section, canonical name, url, access, depth) for every table row."""
    for path in sorted(SURVEY.glob("sd-problems-survey-*.md")):
        section = ""
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.startswith("## "):
                section = line[3:].strip()
            m = ROW.match(line)
            if not m:
                continue
            cells = [c.strip() for c in m.group(1).split("|")]
            if len(cells) < 5 or cells[1] in ("Canonical name", "") or set(cells[1]) <= {"-", ":"}:
                continue
            url = re.search(r"https?://[^\s)>\]]+", cells[2])
            yield section, cells[1], url.group(0) if url else "", cells[3], cells[4]


def main(argv):
    try:
        from design_problem_aliases import ALIASES, OUT_OF_SCOPE
    except ImportError:
        ALIASES, OUT_OF_SCOPE = {}, ()
    by_name = defaultdict(list)
    for section, name, url, access, depth in rows():
        by_name[ALIASES.get(name, name)].append((section, url, access, depth))
    if argv == ["--names"]:
        for name in sorted(by_name, key=lambda n: (-len({s for s, *_ in by_name[n]}), n)):
            print(f"{len({s for s, *_ in by_name[name]}):>3}  {name}")
        return 0
    kept = {n: v for n, v in by_name.items()
            if not any(n.startswith(p) for p in OUT_OF_SCOPE)}
    print(f"{sum(len(v) for v in by_name.values())} rows, {len(by_name)} names, {len(kept)} in scope")
    for name in sorted(kept, key=lambda n: (-len({s for s, *_ in kept[n]}), n)):
        sources = {s for s, *_ in kept[name]}
        free = sum(1 for _, _, a, d in kept[name] if a == "free" and d != "outline")
        print(f"{len(sources):>3} src  {free:>2} free worked  {name}")
    return 0


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent))
    sys.exit(main(sys.argv[1:]))
