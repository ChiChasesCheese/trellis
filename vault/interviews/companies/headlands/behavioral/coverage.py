#!/usr/bin/env python3
"""Story x value coverage for the Headlands background questions.

Edit MATRIX / CAVEATS below, then run:  python3 behavioral/coverage.py
Output is Markdown, pasted into value_matrix.md.

P = primary fit (the story can lead the answer), S = secondary (support / re-angle).
CAVEATS marks a cell whose evidence is weaker than the letter suggests; a value whose
solid primaries are all caveated is reported as THIN even though it has a "P".
"""
from collections import defaultdict

# (code, number, short name, note)
VALUES = [
    ("LOWEGO", 1, "Low ego, collaborative", "JD Q4; videos 09, 13"),
    ("CURIOUS", 2, "Genuine curiosity", "JD Q3; video 12"),
    ("AUTON", 3, "Autonomy, independent ideas", "JD Q4 'autonomously'; video 07"),
    ("AUTOTEST", 4, "Fully automated, extensively tested", "JD Q5"),
    ("PERF", 5, "Performance limits", "JD D3"),
    ("DSTORE", 6, "Distributed storage / compute farm", "JD D2, D4"),
    ("LINUXNET", 7, "Linux, networking, single machine", "JD Q7, Q9, D7"),
    ("BREADTH", 8, "Good at everything, many layers", "JD Q6; video 03"),
    ("FASTITER", 9, "Fast iteration (weeks)", "video 16"),
    ("MONITOR", 10, "Monitoring, proactive detection", "JD D5"),
    ("DATAANAL", 11, "Data analysis for decisions", "JD D6"),
    ("DEBUG", 12, "Debugging, root cause", "JD Q8 'debug'; Q7"),
    ("XTEAM", 13, "Cross-team communication", "JD D8"),
    ("REVIEW", 14, "Code review, mentoring", "JD D9"),
    ("LANG", 15, "Java / C++ language depth", "JD Q8, Plus; recruiter mail"),
]

STORIES = {  # id: (short title, source kind)
    "S1": ("Amex settlement pipeline", "employer"),
    "S2": ("Quality-check framework + ADR", "employer"),
    "S3": ("ACH fee NULL incident RCA", "employer"),
    "S4": ("AU Amex refund fee (data ends thread)", "employer"),
    "S5": ("Interchange source cutover", "employer"),
    "S6": ("Anomaly detector go/no-go", "employer"),
    "S7": ("Schema pool (zero-copy clones)", "employer"),
    "S8": ("Terraform 7-minute RCA + repo scan", "employer"),
    "S9": ("Amex payout-delay incident", "employer"),
    "S10": ("Refund-fee retraction", "employer"),
    "S11": ("Intern: Kafka / Spring / Spark", "intern"),
    "R1": ("Quant-Stroller (personal project)", "resume-only"),
    "R2": ("AI-native Ruby/Kotlin to Snowflake/Java", "resume-only"),
    "R3": ("Aiki / AikiCard (consumer apps)", "resume-only"),
    "M1": ("Onboarding doc + mentoring", "answers-only"),
}

MATRIX = {
    "S1":  {"AUTON": "P", "AUTOTEST": "S", "DEBUG": "S", "MONITOR": "P", "DSTORE": "S", "BREADTH": "S",
            "DATAANAL": "S"},
    "S2":  {"AUTOTEST": "P", "LOWEGO": "P", "PERF": "S", "DATAANAL": "S", "XTEAM": "S", "MONITOR": "S",
            "AUTON": "S"},
    "S3":  {"DEBUG": "P", "AUTOTEST": "P", "MONITOR": "P", "BREADTH": "P", "DATAANAL": "S", "AUTON": "S",
            "FASTITER": "S"},
    "S4":  {"XTEAM": "P", "DATAANAL": "P", "DEBUG": "S", "LOWEGO": "S", "AUTON": "S"},
    "S5":  {"AUTOTEST": "P", "FASTITER": "P", "PERF": "S", "DATAANAL": "S", "DSTORE": "S", "AUTON": "S",
            "XTEAM": "S", "BREADTH": "S"},
    "S6":  {"PERF": "P", "DATAANAL": "P", "AUTON": "P", "LOWEGO": "S", "BREADTH": "S", "DSTORE": "S"},
    "S7":  {"AUTON": "P", "CURIOUS": "P", "FASTITER": "P", "BREADTH": "P", "DSTORE": "S", "AUTOTEST": "S",
            "PERF": "S"},
    "S8":  {"DEBUG": "P", "CURIOUS": "P", "LOWEGO": "P", "FASTITER": "S", "XTEAM": "S"},
    "S9":  {"XTEAM": "P", "LOWEGO": "S", "DEBUG": "S", "FASTITER": "S"},
    "S10": {"LOWEGO": "P", "DATAANAL": "P", "DEBUG": "S", "AUTOTEST": "S", "CURIOUS": "S"},
    "S11": {"DSTORE": "P", "LANG": "S", "BREADTH": "S", "CURIOUS": "S", "PERF": "S"},
    "R1":  {"CURIOUS": "P", "AUTOTEST": "P", "AUTON": "P", "BREADTH": "S", "PERF": "S", "DATAANAL": "S",
            "LINUXNET": "S"},
    "R2":  {"AUTOTEST": "P", "LANG": "S", "FASTITER": "S", "AUTON": "S"},
    "R3":  {"CURIOUS": "S", "AUTON": "S", "FASTITER": "S"},
    "M1":  {"REVIEW": "P", "LOWEGO": "S", "XTEAM": "S"},
}

# Cells whose evidence is weaker than the letter says.  Shown in a separate table.
CAVEATS = {
    ("S6", "PERF"): "capacity reasoning before anything shipped, not profiling a running system",
    ("S11", "DSTORE"): "consumer / sink side only; never operated the cluster",
    ("M1", "REVIEW"): "no code-review trail; contract and architecture review only",
    ("R1", "LINUXNET"): "one resume line (self-hosted CI, 8-GPU server); no detail written down",
    ("S7", "BREADTH"): "personal repository, not the team toolchain",
    ("S7", "AUTON"): "personal repository, not the team toolchain",
}

# Stories whose P counts as "solid" (employer work, S1-S10).
WORK = [s for s in STORIES if s.startswith("S") and s != "S11"]


def main():
    codes = [c for c, *_ in VALUES]
    for sid, row in MATRIX.items():
        assert sid in STORIES, sid
        for c, v in row.items():
            assert c in codes, (sid, c)
            assert v in ("P", "S"), (sid, c)
    assert set(MATRIX) == set(STORIES)
    for (sid, c) in CAVEATS:
        assert c in MATRIX[sid], ("caveat on empty cell", sid, c)

    def cell(sid, c):
        v = MATRIX[sid].get(c, "")
        return v + "*" if v and (sid, c) in CAVEATS else v

    print("| Story | " + " | ".join(f"{n} {c}" for c, n, *_ in VALUES) + " | P | S |")
    print("|---|" + "---|" * (len(VALUES) + 2))
    for sid in STORIES:
        row = MATRIX[sid]
        p = sum(1 for v in row.values() if v == "P")
        s = sum(1 for v in row.values() if v == "S")
        print(f"| **{sid}** {STORIES[sid][0]} | " + " | ".join(cell(sid, c) for c in codes) + f" | {p} | {s} |")
    pc = {c: sum(1 for r in MATRIX.values() if r.get(c) == "P") for c in codes}
    sc = {c: sum(1 for r in MATRIX.values() if r.get(c) == "S") for c in codes}
    print("| **Primary count** | " + " | ".join(str(pc[c]) for c in codes) + " | | |")
    print("| **Secondary count** | " + " | ".join(str(sc[c]) for c in codes) + " | | |")
    print("\n`*` = caveat (see the caveat table).")

    print("\n### Per-value coverage (`solid P` = primary from employer work S1-S10 only)\n")
    print("| # | Value | P | S | solid P | best stories (P first) | status |")
    print("|---|---|---|---|---|---|---|")
    gaps = []
    for c, n, name, src in VALUES:
        ps = [s for s in STORIES if MATRIX[s].get(c) == "P"]
        ss = [s for s in STORIES if MATRIX[s].get(c) == "S"]
        solid = [s for s in ps if s in WORK]
        clean = [s for s in solid if (s, c) not in CAVEATS]
        if not ps and not ss:
            status = "GAP (no story)"
        elif not ps:
            status = "GAP (secondary only)"
        elif not solid:
            status = "THIN (primary only from intern / personal / resume)"
        elif not clean:
            status = "THIN (every solid primary is caveated)"
        elif len(clean) == 1:
            status = "THIN (one clean primary)"
        else:
            status = "ok"
        if status != "ok":
            gaps.append((n, name, status))
        best = ", ".join(ps) + (" / " if ps and ss else "") + ", ".join(ss)
        print(f"| {n} | {name} | {len(ps)} | {len(ss)} | {len(solid)} | {best} | {status} |")

    print("\n### Gaps / thin values\n")
    for n, name, status in gaps:
        print(f"- V{n} {name}: {status}")

    print("\n### Caveat table\n")
    print("| Story | Value | Caveat |")
    print("|---|---|---|")
    for (sid, c), why in CAVEATS.items():
        n = next(n for cc, n, *_ in VALUES if cc == c)
        print(f"| {sid} | V{n} {c} | {why} |")

    print("\n### Story load (values each story is primary for; >4 means over-reliance)\n")
    load = {s: sum(1 for v in MATRIX[s].values() if v == "P") for s in STORIES}
    for s in sorted(load, key=lambda x: -load[x]):
        print(f"- {s} {STORIES[s][0]}: P={load[s]}, S={sum(1 for v in MATRIX[s].values() if v == 'S')}")

    print("\n### Sole-primary risk (value answerable by exactly one primary story)\n")
    inv = defaultdict(list)
    for c, n, name, _ in VALUES:
        ps = [s for s in STORIES if MATRIX[s].get(c) == "P"]
        if len(ps) == 1:
            inv[ps[0]].append(f"V{n} {name}")
    for s, l in inv.items():
        print(f"- {s}: sole primary for {', '.join(l)}")

    total = len(VALUES)
    clean_cov = sum(1 for c in codes
                    if any(MATRIX[s].get(c) == "P" and (s, c) not in CAVEATS for s in WORK))
    print(f"\nTotals: {len(STORIES)} stories x {total} values; values with a clean employer-work primary: "
          f"{clean_cov}/{total}; values with any P: {sum(1 for c in codes if pc[c])}/{total}; "
          f"values with zero story: {sum(1 for c in codes if not pc[c] and not sc[c])}")


if __name__ == "__main__":
    main()
