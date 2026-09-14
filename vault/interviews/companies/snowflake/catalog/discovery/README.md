# Snowflake interview-kit harvest — discovery/ (agent C, harvester)

Run date: 2026-09-13. Scope: Reddit, Hacker News, and a 1point3acres Telegram mirror, for
Snowflake backend-SWE interview signal (OA / phone screen / onsite / offer / rejection posts).
This directory is self-contained; nothing outside `catalog/discovery/` was touched and no git
commands were run.

## What was harvested

### 1. Reddit
- Subs: `leetcode`, `cscareerquestions`, `csMajors`, `ExperiencedDevs`, `snowflake`, `dataengineering`.
- Queries (per sub, via `r/<sub>/search.rss?restrict_sr=1`): "snowflake interview", "snowflake oa",
  "snowflake online assessment", "snowflake onsite", "snowflake phone screen", "snowflake
  hackerrank", "snowflake codesignal", "snowflake new grad", "snowflake intern", "snowflake system
  design", "snowflake offer", "snowflake rejected", "snowflake ic1", "snowflake ic2", "snowflake
  backend interview", "snowflake chakra", "snowflake ai interview" — 17 queries x 6 subs = 102
  search calls, run sequentially with the tool's built-in 429 backoff plus an added 3.5s floor
  between calls (never in parallel, per the harvester's hard rule on Reddit's RSS endpoint).
- Full text + comments fetched (`reddit-post <id> --sub <sub>`, `.rss` single-post endpoint) for
  every unique post whose **title** mentions "snowflake" AND an interview-context word
  (interview/oa/onsite/screen/offer/assessment/hackerrank/codesignal/chakra), most-recent-first,
  capped at 60.
- Exact commands actually run (via driver scripts that import `harvest.py`'s functions directly
  instead of shelling out per call, so pacing/dedup/checkpointing could be controlled across the
  100+-call matrix in one process — the logic is line-for-line what
  `python3 tools/harvest.py reddit --sub <sub> --q "<query>"` and
  `python3 tools/harvest.py reddit-post <id> --sub <sub>` do; the shared `tools/harvest.py` itself
  was **not** modified):
  - `catalog/discovery/_run_harvest.py` — ran all 102 search calls (6 subs x 17 queries, one
    JSON per sub) to completion, then began the reddit-post full-text pass. Reddit's per-IP rate
    limit hardened partway through the post-fetch pass (100% `HTTP 429` even after the tool's
    internal 4-try exponential backoff) — after ~17 minutes of that going nowhere the process was
    killed (only 4/60 candidates fetched).
  - `catalog/discovery/_resume_posts.py` — recomputed the same 60 candidates from the on-disk
    per-sub search JSON, skipped the 4 already-saved ids, retried the remaining 56 with a longer
    external delay (6s, on top of the tool's own backoff). Recovered to ~40% success (18/56 ok;
    the rest still 429'd).
  - `catalog/discovery/_retry_failed.py` — one more pass over the ids that failed in the previous
    step (34 remaining), delay raised to 9s. Recovered another 13/34.
  - Net result: **35 of the 60 candidate posts got full text + comments**; the other 25 kept
    hitting 429 through three passes and were left as search-index metadata only (title, author,
    published date, permalink — still in the per-sub JSON, just no body/comments).
- Raw output: `harvest/reddit_<sub>_2026-09-13.json` (search-result index per sub, deduped by post
  id) and `harvest/reddit_posts_2026-09-13.json` (full body + comments for the 35 successfully
  fetched posts).

### 2. Hacker News
- `catalog/discovery/_run_hn.py`, equivalent to `harvest.py hn --q "<query>"` for each query with
  both `tags=comment` and `tags=story` (Algolia API, open/no auth, no rate-limit issues), 4
  queries: "snowflake interview", "snowflake onsite", "snowflake hiring engineer", "snowflake
  interview process". 414 unique rows.
- HN's full-text search is **very noisy for "snowflake"**: the idiom "special snowflake" and the
  SQL-warehouse-product sense of the word dominate. A word-proximity filter
  (`_filter_hn3.py`, "snowflake" within ~180 chars of an interview-context word) cut 414 → 72
  candidates; manual read-through of those found only **6** that are actually first-hand Snowflake
  (the employer) interview accounts with a concrete fact — see Triage table. The rest are hiring
  threads (Snowflake job postings inside monthly "Who is hiring" threads — real but not interview
  accounts) or false positives on the idiom.
- Raw output: `harvest/hn_2026-09-13.json` (414 raw), `harvest/hn_2026-09-13_relevant.json`
  (72 proximity-filtered, pre-manual-review).

### 3. 1point3acres mirror (Telegram)
- `curl -A <desktop UA> "https://t.me/s/usinterview?q=snowflake"`, then paged backwards with
  `&before=<lowest message id>` from each page's minimum `data-post` id.
  - `page_1.html`: HTTP 200, 20 hits, ids 28723-29627 (2026-06-06 to 2026-09-04).
  - `page_2.html`: HTTP 200, 2 hits, ids 28631-28661 (2026-05-30 to 2026-06-01).
  - `page_3.html` (`before=28631`): HTTP 200 but **0 matching messages** — query exhausted after
    3 pages (well inside the 8-page budget; not stopped by the 2024-06 age cutoff, since this
    channel's entire `#snowflake`-tagged backlog turned out to be only ~4 months old, 2026-05
    through 2026-09).
  - Parsed all 22 raw hits into `mirror_1p3a_snowflake/_parsed.json`, dropped 1 off-topic hit
    (an Agoda DA thread that only mentions "Snowflake" as the SQL warehouse product, not the
    company) → 21 rows in `mirror_1p3a_snowflake/index.md`.
  - Also tried the Stripe-catalog's `__NEXT_DATA__` bypass (curl with a browser UA straight to a
    `1point3acres.com` Next.js page, reading the SSR JSON blob without needing to render the
    login-walled client): `https://www.1point3acres.com/interview/company/snowflake`,
    `https://www.1point3acres.com/interview/problems/company/snowflake`, and
    `https://www.1point3acres.com/interview/thread/1188432` (a thread id sourced from the Telegram
    mirror above). **All three returned HTTP 403** with a Cloudflare "Just a moment..." challenge
    page (`raw_1p3a_nextdata/*.html`) — the bypass that worked for Stripe's researcher on
    2026-09-01 no longer works as of 2026-09-13; Cloudflare bot-challenge appears to have been
    added site-wide (or at least to these paths) in the interim. Recorded and moved on per
    instructions; no further attempts (no proxy/JS-rendering tools used).

## Counts per source

| Source | Search calls | Raw hits (deduped per sub) | Full-text fetched | Blocked / notes |
|---|---|---|---|---|
| Reddit | 102 (17 queries x 6 subs) | leetcode 73, cscareerquestions 77, csMajors 86, ExperiencedDevs 43, snowflake 90, dataengineering 47 → **416 raw hits** | 35 of 60 candidate posts (title matched "snowflake" + interview-context word); other 25 stayed metadata-only | Sustained 429 wall during post-fetch phase (see above); every search call eventually succeeded via the tool's own backoff, some sub x query combos legitimately returned 0 hits (see `_run_harvest.log`) |
| Hacker News | 8 (4 queries x 2 tag types) | 414 raw, algolia API | full text always included (Algolia returns full comment/story text); 6 rows judged genuinely on-topic after manual review | none blocked (open API); signal-to-noise is the problem, not access |
| 1p3a Telegram mirror | 3 pages | 22 raw / 21 after dropping 1 off-topic (Agoda) | full thread bodies NOT available (login wall); only Telegram caption + site link-preview snippet, both already source-truncated upstream | query exhausted at page 3 (`before=28631` → 0 hits) |
| 1p3a direct (`__NEXT_DATA__`) | 3 URLs | 0 | — | **all 3 HTTP 403** (Cloudflare "Just a moment..." challenge) — the bypass that worked for the Stripe researcher on 2026-09-01 is dead as of 2026-09-13 |

## Triage table

46 rows — every harvested item that states a concrete interview question or a concrete round
fact: 22 from Reddit, 18 from the 1point3acres Telegram mirror, 6 from Hacker News. First-hand =
poster describing their own interview. Second-hand = someone relaying another's report, a
recruiter statement relayed by the candidate, a compiled/aggregated list, or an SEO-style page.

See **`TRIAGE.md`** in this directory for the full table with links.

## Files in this directory

- `README.md` (this file), `TRIAGE.md` — the two deliverable write-ups.
- `harvest/` — raw JSON: `reddit_<sub>_2026-09-13.json` (6 files), `reddit_posts_2026-09-13.json`,
  `hn_2026-09-13.json`, `hn_2026-09-13_relevant.json`.
- `mirror_1p3a_snowflake/` — `page_1.html`..`page_3.html` (raw Telegram HTML), `_parsed.json`,
  `index.md` (the requested table).
- `raw_1p3a_nextdata/` — the three failed `__NEXT_DATA__`-bypass attempts (403 Cloudflare
  challenge pages), kept as evidence the method is currently dead.
- `_run_harvest.py`, `_resume_posts.py`, `_retry_failed.py`, `_run_hn.py`, `_parse_tg.py`,
  `_build_mirror_index.py`, `_filter_hn3.py` — scratch driver/parser scripts (not shared tools;
  `tools/harvest.py` itself was never modified), kept for reproducibility/audit. `*.log` files
  next to them are the run logs referenced above.
