"""Read the survey files and count, per problem, the independent sources that teach it.

    uv run python scripts/design_problem_survey.py            # frequency table (system-design)
    uv run python scripts/design_problem_survey.py --names     # every canonical name seen
    uv run python scripts/design_problem_survey.py --domain low-level-design [--names]

Each domain has its own survey folder and alias module (`design_problem_aliases`,
`lld_problem_aliases`). Rows with fewer than five cells — outline tables — are ignored.

The survey agents normalised names on their own, so the same problem arrives
under several. ALIASES folds them; anything not in it stands as itself.
"""

from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

DOMAINS = {"system-design": ("sd-problems-survey-*.md", "design_problem_aliases"),
           "low-level-design": ("lld-survey-*.md", "lld_problem_aliases")}
ROW = re.compile(r"^\|(.+)\|\s*$")


def rows(domain: str = "system-design"):
    """(source section, canonical name, url, access, depth) for every table row."""
    folder = Path(__file__).resolve().parents[1] / "vault/domains" / domain / "survey"
    for path in sorted(folder.glob(DOMAINS[domain][0])):
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
    domain = "system-design"
    if "--domain" in argv:
        i = argv.index("--domain")
        domain = argv[i + 1]
        argv = argv[:i] + argv[i + 2:]
    try:
        module = __import__(DOMAINS[domain][1])
        ALIASES, OUT_OF_SCOPE = module.ALIASES, module.OUT_OF_SCOPE
        normalise = getattr(module, "normalise", lambda n: n)
    except ImportError:
        ALIASES, OUT_OF_SCOPE, normalise = {}, (), (lambda n: n)
    by_name = defaultdict(list)
    for section, name, url, access, depth in rows(domain):
        name = normalise(name)
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
        free = sum(1 for _, _, a, d in kept[name] if a == "free" and not d.startswith("outline"))
        print(f"{len(sources):>3} src  {free:>2} free worked  {name}")
    return 0


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).parent))
    sys.exit(main(sys.argv[1:]))
