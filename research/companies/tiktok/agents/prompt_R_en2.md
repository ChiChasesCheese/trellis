# Task — refresh TikTok / ByteDance coding-interview sightings (EN-2 half), 2026-10-28

Repo `/Users/chiserver/sessions/trellis`, branch `main`. Never commit, never spawn agents, never edit any file except
your output file `research/companies/tiktok/catalog/refresh-2026-10-28-en2.json`. Scratch work in `/tmp/rf_en2/`.
The repo is public: record source ids and URLs, short English paraphrases of the problem only; no names, no handles,
no contact details, no copied post bodies.

## Context

On 2026-10-24 a full collection (window 2025-10-01 .. 2026-10-24) produced `research/companies/tiktok/catalog/CATALOG.md`
§1 (186 coding problem families, 464 de-duplicated sightings; each row lists its sources) from the raw notes in
`research/companies/tiktok/catalog/raw/`. Read CATALOG.md §0 (counting rules) and §1, and the raw files of your half
for the **access paths that worked** (they are written at the top of each raw file). Your job is the delta: coding
sightings dated **2026-10-17 or later** (overlap on purpose: mirrors publish late) that are **not already** in CATALOG.md.

## Your sources (English half, second pass: fill the gaps of the first pass)

The first pass (`catalog/refresh-2026-10-28-en.json`, read its `sightings` and `skipped`) covered 1P3A tag pages 1-2,
the rendered 1P3A bank page, the TrueInterview GitHub mirror, Reddit, LeetCode Discuss, PracHub and Hello Interview.
Do NOT repeat those; do these, glancing at whatever is visible when content is gated (a title, a summary line, a
visible fragment is enough to identify a problem):

1. **1point3acres bank, per record**: on the rendered bank page `https://www.1point3acres.com/interview/problems/company/ByteDance`,
   open each coding record's own page (click through in the Playwright browser) and note its last-asked date and the
   threads it lists; compare with `raw/1p3a.md` §1 → `bank_changes`, and any thread dated ≥ 2026-10-17 not yet in a
   sighting becomes a row. Use only the rendered pages: the in-page tRPC fetch was refused by the permission system in the
   first pass, so do not call it or work around that refusal.
2. **1point3acres threads the first pass could not name**: 1194630 (TT Infra, "graph problems"), 1193633, 1193634, and
   any other ByteDance / TikTok thread on tag pages 1-3 dated ≥ 2026-10-17: open `https://www.1point3acres.com/interview/thread/<tid>`
   (the experience-summary page, which named LC 311 for 1194680) and the thread page; record any problem now visible.
3. **Blind**: `https://www.teamblind.com/search/<query>` for "TikTok interview", "ByteDance interview", "TikTok coding",
   "TikTok phone screen", "TikTok onsite", "TikTok leetcode" (browser User-Agent; see `sources.md` §Blind): posts dated
   ≥ 2026-10-17 that name a coding problem.
4. **Glassdoor** (direct fetch is 403): WebSearch `site:glassdoor.com TikTok software engineer interview questions` and
   ByteDance variants; record only snippets dated ≥ 2026-10-17 that name a problem (conf low).
5. **TrueInterview site** `https://www.trueinterview.io` ByteDance / TikTok question list: titles and dates newer than the
   mirror's newest (2026-10-05); titles are visible even when the body is gated.
The Playwright browser is yours alone during this task; close tabs you open.

## Output

A JSON object:

```json
{"collected": "2026-10-28", "half": "en2",
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
