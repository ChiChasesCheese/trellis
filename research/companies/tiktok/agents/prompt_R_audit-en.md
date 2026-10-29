# Task — refresh TikTok / ByteDance coding-interview sightings (AUDIT-EN half), 2026-10-28

Repo `/Users/chiserver/sessions/trellis`, branch `main`. Never commit, never spawn agents, never edit any file except
your output file `research/companies/tiktok/catalog/refresh-2026-10-28-audit-en.json`. Scratch work in `/tmp/rf_audit-en/`.
The repo is public: record source ids and URLs, short English paraphrases of the problem only; no names, no handles,
no contact details, no copied post bodies.

## Context

On 2026-10-24 a full collection (window 2025-10-01 .. 2026-10-24) produced `research/companies/tiktok/catalog/CATALOG.md`
§1 (186 coding problem families, 464 de-duplicated sightings; each row lists its sources) from the raw notes in
`research/companies/tiktok/catalog/raw/`. Read CATALOG.md §0 (counting rules) and §1, and the raw files of your half
for the **access paths that worked** (they are written at the top of each raw file). Your job is the delta: coding
an **audit re-sweep of 2026-07-17 .. 2026-10-28**: go through every platform below again for that window, and record every coding sighting that is **not already** in CATALOG.md §1 or in `catalog/refresh-2026-10-28-*.json` (check source ids and same-event duplicates). Also add, to `skipped`, per platform: how many reports in the window you looked at, how many named a problem, and how many of those were already recorded — this measures how complete the first collection was.

## Your sources (English: US / SG). Window 2026-07-17 .. 2026-10-28

1. 1point3acres: forum tag `bytedance` pages (`https://www.1point3acres.com/bbs/tag-4142-<page>.html`) back to threads of
   2026-07-17 (about pages 1-15), each thread's experience-summary page `https://www.1point3acres.com/interview/thread/<tid>`
   and visible fragments; the bank page with its 30-day / 90-day filters. Gated content: glance at what is visible (title,
   summary, fragments). Do not call the in-page tRPC fetch (refused by the permission system before) or work around any
   refusal, login or paywall.
2. TrueInterview: GitHub mirror `kevin-2023-code/Tech-Interview-Questions` via `gh api` (`data/questions.jsonl`), and the
   site's ByteDance / TikTok lists for titles.
3. Blind search pages (`sources.md` §Blind; queries: TikTok interview, ByteDance interview, TikTok coding, TikTok phone
   screen, TikTok onsite, TikTok leetcode, TikTok senior, TikTok USDS).
4. Reddit via Arctic Shift (`raw/forums_en.md`), LeetCode Discuss (`raw/forums_en.md` §LC Discuss), PracHub company pages
   (all pages back to 2026-07-17), Hello Interview TikTok questions, Glassdoor via WebSearch snippets.
The Playwright browser is yours alone during this task; close tabs you open.

## Output

A JSON object:

```json
{"collected": "2026-10-28", "half": "audit-en", "window": ["2026-07-17", "2026-10-28"],
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
