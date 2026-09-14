"""q06 Atlas Company Name Availability — reference solution.

One registry: normalized name -> registrant account (None for names from the REGISTERED block).
Parts differ only in whether accepted names are stored (Part 2) and whether RECLAIM is honoured
(Part 3), so a single `run(lines, persist, reclaim)` drives all three.
"""
from __future__ import annotations

import sys

SUFFIXES = {"inc", "inc.", "corp", "corp.", "llc", "l.l.c.", "llc."}
ARTICLES = {"the", "a", "an"}
AVAILABLE, NOT_AVAILABLE = "Name Available", "Name Not Available"


def normalize(name: str, strip_punctuation: bool = True) -> str:
    tokens = name.lower().replace("&", " ").replace(",", " ").split()   # steps 1-3
    while tokens and tokens[-1] in SUFFIXES:                            # step 4: repeat
        tokens.pop()
    if tokens and tokens[0] in ARTICLES:                                # step 5: once
        tokens = tokens[1:]
    tokens = [t for i, t in enumerate(tokens) if t != "and" or i == 0]  # step 6
    if strip_punctuation:                                               # step 7 (reconstructed)
        tokens = "".join(c if c.isalnum() else " " for c in " ".join(tokens)).split()
    return " ".join(tokens)


def split_input(lines: list[str]) -> tuple[list[str], list[str]]:
    registered: list[str] = []
    requests: list[str] = []
    section = "REQUESTS"
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        if line.upper() in ("REGISTERED", "REQUESTS"):
            section = line.upper()
        elif section == "REGISTERED":
            registered.append(line)
        else:
            requests.append(line)
    return registered, requests


def run(lines: list[str], persist: bool, reclaim: bool) -> list[str]:
    registered, requests = split_input(lines)
    registry: dict[str, str | None] = {}                 # normalized name -> registrant account
    for name in registered:
        key = normalize(name)
        if key:
            registry.setdefault(key, None)               # block names have no registrant
    out: list[str] = []
    for req in requests:
        if req.upper().startswith("RECLAIM,"):
            if reclaim:
                _, account, name = req.split(",", 2)     # the name may contain commas
                key = normalize(name)
                # only the original registrant may reclaim; unknown names / block names ignored
                if key in registry and registry[key] == account.strip():
                    del registry[key]
            continue
        account, _, name = req.partition("|")
        account = account.strip()
        key = normalize(name)
        if key and key not in registry:                  # empty normalized name is never available
            out.append(f"{account}|{AVAILABLE}")
            if persist:
                registry[key] = account                  # taken from now on, even for this account
        else:
            out.append(f"{account}|{NOT_AVAILABLE}")
    return out


def part1(lines: list[str], persist: bool = False) -> list[str]:
    return run(lines, persist=persist, reclaim=False)


def part2(lines: list[str]) -> list[str]:
    return run(lines, persist=True, reclaim=False)


def part3(lines: list[str]) -> list[str]:
    return run(lines, persist=True, reclaim=True)


def main(stdin=sys.stdin, stdout=sys.stdout) -> None:
    lines = [ln.strip() for ln in stdin.read().splitlines() if ln.strip()]
    part = 3
    if lines and lines[0].upper().startswith("PART"):
        part = int(lines[0].split()[1])
        lines = lines[1:]
    out = {1: part1, 2: part2, 3: part3}[part](lines)
    stdout.write("\n".join(out) + ("\n" if out else ""))


if __name__ == "__main__":
    main()
