# Task — refresh TikTok / ByteDance coding-interview sightings (AUDIT-CN half), 2026-10-28

Repo `/Users/chiserver/sessions/trellis`, branch `main`. Never commit, never spawn agents, never edit any file except
your output file `research/companies/tiktok/catalog/refresh-2026-10-28-audit-cn.json`. Scratch work in `/tmp/rf_audit-cn/`.
The repo is public: record source ids and URLs, short English paraphrases of the problem only; no names, no handles,
no contact details, no copied post bodies.

## Context

On 2026-10-24 a full collection (window 2025-10-01 .. 2026-10-24) produced `research/companies/tiktok/catalog/CATALOG.md`
§1 (186 coding problem families, 464 de-duplicated sightings; each row lists its sources) from the raw notes in
`research/companies/tiktok/catalog/raw/`. Read CATALOG.md §0 (counting rules) and §1, and the raw files of your half
for the **access paths that worked** (they are written at the top of each raw file). Your job is the delta: coding
an **audit re-sweep of 2026-07-17 .. 2026-10-28**: go through every platform below again for that window, and record every coding sighting that is **not already** in CATALOG.md §1 or in `catalog/refresh-2026-10-28-*.json` (check source ids and same-event duplicates). Also add, to `skipped`, per platform: how many reports in the window you looked at, how many named a problem, and how many of those were already recorded — this measures how complete the first collection was.

## Your sources (Chinese: CN). Window 2026-07-17 .. 2026-10-28

1. Nowcoder search API (`raw/forums_cn.md` §0 for the method; use all its queries plus 字节 手撕, 字节 算法题, 抖音 面经,
   TikTok 面经, 飞书 后端, 字节 社招, 字节 秋招 后端), all pages back to 2026-07-17; bodies from the detail pages.
2. GitHub mirror `wearzdk/interview-experience` (all ByteDance / TikTok / 抖音 / 飞书 files dated in the window),
   `atomeocean/job-compass`, `emmazhang-ai-sde/shuyangzhang-leetcode-notes`.
3. A glance at 小红书 / 知乎 / CSDN / 掘金 through WebSearch (they failed before; record what search shows).
Do not use the browser (another agent owns it); curl / gh / WebFetch only.

## Output

A JSON object:

```json
{"collected": "2026-10-28", "half": "audit-cn", "window": ["2026-07-17", "2026-10-28"],
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
