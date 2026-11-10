"""Refuse a commit or push that would carry private material to GitHub.

    python3 scripts/private_guard.py staged     # pre-commit: added lines and paths in the index
    python3 scripts/private_guard.py push       # pre-push: everything about to be pushed (reads the refs on stdin)
    python3 scripts/private_guard.py scan       # every tracked file, for an audit

Private material (an employer's internals, interview notes a company must not see) lives only in gitignored places
(`sources/local/private/<name>/`, `vault/private/`, `skeleton/private-*.yaml`) and in Anki. The terms that identify it
are kept outside the repository, one per line, in ~/.config/trellis/private_terms.txt (the list is itself private).
Matches are whole words, case-sensitive. Installed as git hooks by `scripts/install_private_guard.sh`.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

TERMS = Path.home() / ".config/trellis/private_terms.txt"
PRIVATE_PATHS = ("sources/local/", "vault/private/", "skeleton/private-", "research/private/")


def terms() -> list[str]:
    if not TERMS.exists():
        return []
    return [t.strip() for t in TERMS.read_text(encoding="utf-8").splitlines() if t.strip() and not t.startswith("#")]


def pattern(ts: list[str]) -> re.Pattern | None:
    if not ts:
        return None
    return re.compile(r"(?<![A-Za-z0-9_])(" + "|".join(re.escape(t) for t in sorted(ts, key=len, reverse=True)) + r")(?![A-Za-z0-9_])")


def check_diff(diff: str, pat: re.Pattern | None) -> list[str]:
    hits, path = [], ""
    for line in diff.splitlines():
        if line.startswith("+++ b/"):
            path = line[6:]
            if path.startswith(PRIVATE_PATHS):
                hits.append(f"{path}: private path")
        elif line.startswith("+") and not line.startswith("+++") and pat:
            m = pat.search(line)
            if m:
                hits.append(f"{path}: '{m.group(1)}' in: {line[1:120]}")
    return hits


def main() -> int:
    mode = sys.argv[1] if len(sys.argv) > 1 else "staged"
    pat = pattern(terms())
    if mode == "staged":
        diff = subprocess.run(["git", "diff", "--cached", "-U0", "--no-color"], capture_output=True, text=True).stdout
        hits = check_diff(diff, pat)
    elif mode == "push":
        hits = []
        for line in sys.stdin.read().splitlines():
            local_ref, local_sha, remote_ref, remote_sha = line.split()
            if set(local_sha) == {"0"}:
                continue
            base = remote_sha if set(remote_sha) != {"0"} else "origin/main"
            diff = subprocess.run(["git", "diff", "-U0", "--no-color", f"{base}..{local_sha}"], capture_output=True, text=True).stdout
            hits += check_diff(diff, pat)
    else:
        hits = []
        for f in subprocess.run(["git", "ls-files"], capture_output=True, text=True).stdout.splitlines():
            if f.startswith(PRIVATE_PATHS):
                hits.append(f"{f}: private path is tracked")
            elif pat:
                try:
                    for n, line in enumerate(Path(f).read_text(encoding="utf-8", errors="ignore").splitlines(), 1):
                        m = pat.search(line)
                        if m:
                            hits.append(f"{f}:{n}: '{m.group(1)}'")
                except (IsADirectoryError, FileNotFoundError):
                    pass
    if hits:
        print("private_guard: refusing; private material would leave this machine:", file=sys.stderr)
        for h in hits[:40]:
            print("  " + h, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
