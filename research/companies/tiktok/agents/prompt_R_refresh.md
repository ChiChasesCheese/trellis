# Task — refresh TikTok / ByteDance coding-interview sightings ({HALF} half), 2026-10-28

Repo `/Users/chiserver/sessions/trellis`, branch `main`. Never commit, never spawn agents, never edit any file except
your output file `research/companies/tiktok/catalog/refresh-2026-10-28-{half}.json`. Scratch work in `/tmp/rf_{half}/`.
The repo is public: record source ids and URLs, short English paraphrases of the problem only; no names, no handles,
no contact details, no copied post bodies.

## Context

On 2026-10-24 a full collection (window 2025-10-01 .. 2026-10-24) produced `research/companies/tiktok/catalog/CATALOG.md`
§1 (186 coding problem families, 464 de-duplicated sightings; each row lists its sources) from the raw notes in
`research/companies/tiktok/catalog/raw/`. Read CATALOG.md §0 (counting rules) and §1, and the raw files of your half
for the **access paths that worked** (they are written at the top of each raw file). Your job is the delta: coding
sightings dated **2026-10-17 or later** (overlap on purpose: mirrors publish late) that are **not already** in CATALOG.md.

{SOURCES}

## Output

A JSON object:

```json
{"collected": "2026-10-28", "half": "{half}",
 "sightings": [
   {"date": "2026-10-21", "region": "US|SG|CN", "source": "NC 2931234 | 1P3A 1194001 | TI 2026-10-22 | reddit 1xyzabc | ...",
    "url": "...", "role": "backend intern / SWE 2-1 / ...", "round": "OA|P|O|HM|?",
    "family": "exact family name from CATALOG.md §1 (bold text without **) or null",
    "lc": [146], "custom": "one-line English description when no LeetCode number fits, else null",
    "note": "how TikTok changed it, if stated", "conf": "high|medium|low"}
 ],
 "bank_changes": [ {"slug": "...", "n_before": 9, "n_now": 10, "last_before": "2026-10-07", "last_now": "2026-10-25"} ],
 "skipped": "one paragraph: which sources failed or returned nothing, and why"}
```

Rules: one row per problem per interview report (a post naming two problems = two rows). Count a report once even if it
appears on several sites (same problem family, dates within 7 days, different sites = one event; keep the first-hand
source). Drop sightings that name no identifiable problem ("a medium DP"). Map to an LC number whenever the problem is a
LeetCode problem or a close variant; use `custom` only for genuinely non-LeetCode problems. A sighting already listed
in CATALOG.md (same source id) is not a new row.

## Reply (≤ 10 lines)

Number of new sightings, how many map to an existing family vs new families, the new families with LC numbers, the date
range covered, what failed.
