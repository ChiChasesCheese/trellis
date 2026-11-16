"""Export LeetCode Project workspaces (README, template, tests, every file) through Chi's own Chrome.

    uv run python scripts/lcp_export.py rate-limiter [url-shortener ...]   # one or more projects, one after another
    uv run python scripts/lcp_export.py --all                              # every project in the public list
    uv run python scripts/lcp_export.py --force rate-limiter               # export again even if done

A project's files exist only inside a timed cloud workspace (Eclipse Theia in an iframe) that a practice start
creates; the page's own GraphQL has no file API, and the browser tools can neither read the cross-origin iframe nor
return file text unfiltered. So a helper Claude Code session with Claude in Chrome (`claude --chrome -p`, the local
browser, where Chi is signed in) starts the practice in Python, lists the expanded file tree, uses Theia's own
Download on every top-level item except environments, and ends the practice without submitting
(research/domains/low-level-design/lc-project/EXPORT_PROMPT.md). This script then moves the download out of
~/Downloads (needs Full Disk Access for the tmux server) into sources/local/lc-project/workspaces/<slug>/ and unpacks
it into files/. Everything stays local: LeetCode's problem material never goes into the public repository.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tarfile
import time
import urllib.request
import zipfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
PROMPT = ROOT / "research/domains/low-level-design/lc-project/EXPORT_PROMPT.md"
OUT = ROOT / "sources/local/lc-project/workspaces"
HELPER_CWD = Path.home() / "sessions/lcproj-chrome"  # outside the repo: the helper needs no project instructions
DOWNLOADS = Path.home() / "Downloads"
WAIT = 90  # seconds to wait for the download to finish after the helper returns


def all_slugs() -> list[str]:
    q = "query { projectProblemList(skip: 0, limit: 200) { nodes { slug } } }"
    req = urllib.request.Request("https://leetcode.com/graphql/", data=json.dumps({"query": q}).encode(),
                                 headers={"Content-Type": "application/json", "Referer": "https://leetcode.com/project/",
                                          "User-Agent": "Mozilla/5.0"})
    return [n["slug"] for n in json.loads(urllib.request.urlopen(req, timeout=30).read())["data"]["projectProblemList"]["nodes"]]


def snapshot() -> dict[str, float]:
    return {p.name: p.stat().st_mtime for p in DOWNLOADS.iterdir()}


def new_download(before: dict[str, float]) -> Path | None:
    deadline = time.time() + WAIT
    while time.time() < deadline:
        fresh = [p for p in DOWNLOADS.iterdir() if p.name not in before and not p.name.endswith((".crdownload", ".download"))]
        partial = [p for p in DOWNLOADS.iterdir() if p.name.endswith((".crdownload", ".download"))]
        if fresh and not partial:
            return max(fresh, key=lambda p: p.stat().st_mtime)
        time.sleep(2)
    return None


def safe_members(names: list[str]) -> bool:
    return all(not PurePosixPath(n).is_absolute() and ".." not in PurePosixPath(n).parts for n in names)


def unpack(archive: Path, dest: Path) -> int:
    dest.mkdir(parents=True, exist_ok=True)
    if zipfile.is_zipfile(archive):
        with zipfile.ZipFile(archive) as z:
            if not safe_members(z.namelist()):
                raise RuntimeError(f"{archive.name}: unsafe paths")
            z.extractall(dest)
            return len(z.namelist())
    if tarfile.is_tarfile(archive):
        with tarfile.open(archive) as t:
            members = [m for m in t.getmembers() if m.isfile() or m.isdir()]
            if not safe_members([m.name for m in members]):
                raise RuntimeError(f"{archive.name}: unsafe paths")
            t.extractall(dest, members=members, filter="data")
            return len(members)
    shutil.copy2(archive, dest / archive.name)  # a single file is delivered as itself
    return 1


def export(slug: str, force: bool) -> bool:
    home = OUT / slug
    if (home / ".done").exists() and not force:
        print(f"{slug}: already exported")
        return True
    home.mkdir(parents=True, exist_ok=True)
    HELPER_CWD.mkdir(parents=True, exist_ok=True)
    before = snapshot()
    prompt = PROMPT.read_text(encoding="utf-8").replace("{SLUG}", slug)
    r = subprocess.run(["claude", "--chrome", "--model", "sonnet", "-p", prompt,
                        "--allowedTools", "mcp__claude-in-chrome__*,ToolSearch"],
                       cwd=HELPER_CWD, stdin=subprocess.DEVNULL, capture_output=True, text=True, timeout=1500)
    (home / "export.log").write_text(r.stdout + ("\n--- stderr ---\n" + r.stderr if r.stderr else ""), encoding="utf-8")
    got = new_download(before)
    if not got:
        print(f"{slug}: no download arrived; see {home / 'export.log'}")
        return False
    target = home / got.name
    shutil.move(str(got), target)
    n = unpack(target, home / "files")
    (home / ".done").write_text(time.strftime("%Y-%m-%dT%H:%M:%S"), encoding="utf-8")
    print(f"{slug}: {got.name}, {n} entries -> {home / 'files'}")
    return True


def main() -> int:
    args = sys.argv[1:]
    force = "--force" in args
    slugs = [a for a in args if not a.startswith("--")]
    if "--all" in args:
        slugs = all_slugs()
    if not slugs:
        print(__doc__)
        return 2
    try:
        DOWNLOADS.iterdir().__next__()
    except PermissionError:
        print("~/Downloads is not readable: give the tmux server Full Disk Access first")
        return 1
    except StopIteration:
        pass
    return 0 if all([export(s, force) for s in slugs]) else 1


if __name__ == "__main__":
    sys.exit(main())
