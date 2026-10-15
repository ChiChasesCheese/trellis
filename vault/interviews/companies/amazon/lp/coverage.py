#!/usr/bin/env python3
"""LP x story coverage. Edit MATRIX below, then run: python3 lp/coverage.py

P = primary fit (story can lead the answer), S = secondary (usable as support / re-angle).
Output is Markdown, pasted into story_matrix.md.
"""
from collections import defaultdict

LPS = [  # (code, number, official name)
    ("CO", 1, "Customer Obsession"), ("OWN", 2, "Ownership"), ("IS", 3, "Invent and Simplify"),
    ("ARAL", 4, "Are Right, A Lot"), ("LBC", 5, "Learn and Be Curious"), ("HD", 6, "Hire and Develop the Best"),
    ("IHS", 7, "Insist on the Highest Standards"), ("TB", 8, "Think Big"), ("BFA", 9, "Bias for Action"),
    ("FRU", 10, "Frugality"), ("ET", 11, "Earn Trust"), ("DD", 12, "Dive Deep"),
    ("HB", 13, "Have Backbone; Disagree and Commit"), ("DR", 14, "Deliver Results"),
    ("BE", 15, "Strive to be Earth's Best Employer"), ("SSBR", 16, "Success and Scale Bring Broad Responsibility"),
]

STORIES = {  # id: (short title, source)
    "S1": ("Amex settlement pipeline", "core/stories S1"),
    "S2": ("Quality-check framework + ADR", "S2"),
    "S3": ("ACH fee NULL incident RCA", "S3"),
    "S4": ("AU Amex refund fee (data ends thread)", "S4"),
    "S5": ("Net Settlement / interchange source switch", "S5"),
    "S6": ("Anomaly detector go/no-go", "S6"),
    "S7": ("Schema pool (zero-copy clones)", "S7"),
    "S8": ("Terraform 7-minute RCA", "S8"),
    "S9": ("Amex payout-delay incident", "S9"),
    "S10": ("Refund-fee billing-terms retraction", "S10"),
    "S11": ("Intern: Kafka/Spring/Spark", "S11"),
    "R1": ("Quant-Stroller (personal project)", "resume"),
    "R2": ("AI-native Ruby/Kotlin to Snowflake/Java migration", "resume"),
    "R3": ("Aiki / AikiCard (consumer apps)", "resume"),
    "M1": ("Onboarding doc + new-engineer mentoring", "Answers Q13/Q16"),
}

MATRIX = {
    "S1":  {"OWN": "P", "DR": "P", "DD": "S", "IHS": "S", "IS": "S", "FRU": "S"},
    "S2":  {"IS": "P", "IHS": "P", "ET": "P", "FRU": "P", "ARAL": "S", "HB": "S", "TB": "S", "HD": "S"},
    "S3":  {"DD": "P", "OWN": "P", "IHS": "P", "HB": "P", "CO": "S", "BFA": "S", "ET": "S", "DR": "S"},
    "S4":  {"CO": "P", "DD": "P", "ET": "P", "ARAL": "S", "HB": "S", "OWN": "S"},
    "S5":  {"OWN": "P", "DR": "P", "ARAL": "P", "DD": "S", "IHS": "S", "IS": "S", "BFA": "S", "CO": "S", "TB": "S", "FRU": "S"},
    "S6":  {"ARAL": "P", "DD": "P", "HB": "P", "OWN": "P", "FRU": "S", "IS": "S", "BFA": "S", "DR": "S", "IHS": "S"},
    "S7":  {"IS": "P", "BFA": "P", "OWN": "P", "LBC": "S", "FRU": "S", "TB": "S"},
    "S8":  {"BFA": "P", "DD": "P", "OWN": "S", "IHS": "S", "ET": "S", "DR": "S"},
    "S9":  {"CO": "P", "DD": "S", "HB": "S", "ET": "S", "DR": "S", "OWN": "S", "IHS": "S"},
    "S10": {"ET": "P", "DD": "P", "ARAL": "P", "IHS": "S", "CO": "S", "OWN": "S"},
    "S11": {"LBC": "S", "DD": "S", "IHS": "S", "DR": "S"},
    "R1":  {"TB": "P", "IS": "P", "LBC": "P", "ARAL": "P", "IHS": "P", "DD": "S", "OWN": "S", "DR": "S"},
    "R2":  {"BFA": "P", "LBC": "P", "DR": "S", "IHS": "S", "IS": "S"},
    "R3":  {"CO": "P", "OWN": "S", "LBC": "S", "IS": "S", "DR": "S"},
    "M1":  {"HD": "P", "ET": "S", "IHS": "S", "BE": "S", "OWN": "S"},
}


def main():
    codes = [c for c, _, _ in LPS]
    for sid, row in MATRIX.items():
        assert sid in STORIES, sid
        for c in row:
            assert c in codes, (sid, c)
            assert row[c] in ("P", "S"), (sid, c)
    assert set(MATRIX) == set(STORIES)

    print("| Story | " + " | ".join(f"{n} {c}" for c, n, _ in LPS) + " | P | S |")
    print("|---|" + "---|" * (len(LPS) + 2))
    for sid in STORIES:
        row = MATRIX[sid]
        cells = [row.get(c, "") for c in codes]
        p = sum(1 for v in row.values() if v == "P")
        s = sum(1 for v in row.values() if v == "S")
        print(f"| **{sid}** {STORIES[sid][0]} | " + " | ".join(cells) + f" | {p} | {s} |")
    pc = {c: sum(1 for r in MATRIX.values() if r.get(c) == "P") for c in codes}
    sc = {c: sum(1 for r in MATRIX.values() if r.get(c) == "S") for c in codes}
    print("| **Primary count** | " + " | ".join(str(pc[c]) for c in codes) + " | | |")
    print("| **Secondary count** | " + " | ".join(str(sc[c]) for c in codes) + " | | |")

    # "work stories" = employer stories only (exclude R*/M1 personal/thin) -> real coverage
    work = [s for s in STORIES if s.startswith("S") and s != "S11"]
    print("\n### Per-LP coverage (P = primary, S = secondary; `solid P` = primary from S1-S10 employer work only)\n")
    print("| # | LP | P | S | solid P (S1-S10) | best stories (P first) | status |")
    print("|---|---|---|---|---|---|---|")
    gaps = []
    for c, n, name in LPS:
        ps = [s for s in STORIES if MATRIX[s].get(c) == "P"]
        ss = [s for s in STORIES if MATRIX[s].get(c) == "S"]
        solid = [s for s in ps if s in work]
        if not ps and not ss:
            status = "GAP (no story)"
        elif not ps:
            status = "GAP (secondary only)"
        elif len(solid) == 0:
            status = "THIN (primary only from personal/resume)"
        elif len(solid) == 1:
            status = "THIN (one solid primary)"
        else:
            status = "ok"
        if status != "ok":
            gaps.append((n, name, status))
        print(f"| {n} | {name} | {len(ps)} | {len(ss)} | {len(solid)} | {', '.join(ps)}{' / ' if ps and ss else ''}{', '.join(ss)} | {status} |")

    print("\n### Gaps / thin LPs\n")
    for n, name, status in gaps:
        print(f"- LP{n} {name}: {status}")

    print("\n### Story load (how many LPs each story is primary for; >4 means over-reliance)\n")
    load = {s: sum(1 for v in MATRIX[s].values() if v == "P") for s in STORIES}
    for s in sorted(load, key=lambda x: -load[x]):
        print(f"- {s} {STORIES[s][0]}: P={load[s]}, S={sum(1 for v in MATRIX[s].values() if v == 'S')}")

    print("\n### Sole-primary risk (LP answerable by exactly one primary story)\n")
    inv = defaultdict(list)
    for c, n, name in LPS:
        ps = [s for s in STORIES if MATRIX[s].get(c) == "P"]
        if len(ps) == 1:
            inv[ps[0]].append(f"LP{n} {name}")
    for s, l in inv.items():
        print(f"- {s}: sole primary for {', '.join(l)}")

    total = len(LPS)
    covered = sum(1 for c, _, _ in LPS if any(MATRIX[s].get(c) == "P" for s in work))
    print(f"\nTotals: {len(STORIES)} stories x {total} LPs; LPs with a solid employer-work primary: {covered}/{total}; "
          f"LPs with any P: {sum(1 for c in codes if pc[c])}/{total}; LPs with zero story: "
          f"{sum(1 for c in codes if not pc[c] and not sc[c])}")


if __name__ == "__main__":
    main()
