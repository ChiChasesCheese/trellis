# Hello Interview community questions — TikTok / ByteDance

Collected 2026-10-24 with the Playwright browser (page loads, no login). Window 2025-10 to 2026-10-24.

## Access

- `https://www.hellointerview.com/community/questions?company=TikTok`: page header says "13,941 total reports" for the site; the TikTok list has 13 questions, only 5 are visible without Premium ("Unlock all 13 TikTok questions"). The other 8 are placeholder Lorem-ipsum cards with user counts (34 / 19 / 11 users), types System Design (Mid-Senior), Coding (Senior-Staff), Behavioral (Mid-level); real titles hidden.
- `?company=ByteDance`: "No questions submitted for this set of filters yet" (0).
- Each visible question has a detail page `/community/questions/<slug>/<id>?company=TikTok` with "Asked at" companies, a timeline (month, level), community solutions and comments.
- Dates are month granularity ("Late September, 2026").

## Visible reports (5 of 13)

| # | Type | Level | Last asked | Users | Title / description | Detail URL |
|---|---|---|---|---|---|---|
| 1 | System Design | Senior | Late September 2026 | 1 | **Design a Metrics Aggregator**: collect count-based metrics (user signups, system errors, ad clicks) from services through a client library and show histogram data on a dashboard; query aggregated metrics for a time range. Also asked at DoorDash, OpenAI, Rippling, LinkedIn (+10). Site digest: StatsD / Datadog-style; high-volume ingest, time buckets, windowed counters, hot-key contention, time-series storage, consistency vs availability, real-time vs batch rollups, cardinality control. 19 community solutions. | https://www.hellointerview.com/community/questions/metrics-aggregator/cm78h7tyk02kgl7b16admv2nz?company=TikTok |
| 2 | System Design | Senior | Early September 2026 | 1 | **Design a TikTok Live Coin Tracking System**: virtual gifting in real time on a live-streaming platform, per-session creator earnings, reliable weekly financial settlement. Timeline note: "globally distributed, highly accurate coin tracking and settlement system; real-time virtual gifting from users worldwide with guaranteed idempotency, precise per-session earnings for creators, reliable weekly settlements". No community solutions yet. TikTok-only question. | https://www.hellointerview.com/community/questions/tiktok-live-coin-tracking/cmtz76hxj2sxb08ad22bhtk6a?company=TikTok |
| 3 | Coding | Senior | Mid August 2026 | 1 | **LeetCode 101 Symmetric Tree** (recursive mirror compare or queue). Also asked at LinkedIn, Apple. | https://www.hellointerview.com/community/questions/symmetric-tree/cm5eh7nrh04pt838o9tb1q1l8?company=TikTok |
| 4 | Coding | Senior | Late July 2026 | 1 | **LeetCode 721 Accounts Merge** (union-find or graph; merge by shared email only, names do not imply identity; return name + sorted unique emails). Also Meta, Airbnb, Bloomberg. | https://www.hellointerview.com/community/questions/accounts-merge/cm5eguhac02kf838ox3fg55a5?company=TikTok |
| 5 | System Design | Senior, Manager | Mid April 2026 | 4 | **Design a Video Moderation System**: global platform like TikTok, millions of video uploads per day, ML risk scoring plus rule-based moderation in near real time, automatic handling of policy violations, audit trails. | https://www.hellointerview.com/community/questions/video-moderation-system/cm7jsn3bt0082fh44ia25k8tf?company=TikTok |

Confidence: medium for all five (site digest of a user submission; one user each except #5 with 4). The remaining 8 reports are not recoverable without Premium.

## Notes

- Matches 1P3A bank records: `top-songs-by-country-leaderboard`, `content-moderation-system-design` (n=5, 2026-01-14 .. 2026-08-12), `payment-platform-design` (idempotency, transactions) and the live-gifting prompt above point to the same area as the Nowcoder "TikTok live room like-count / comment system" prompts.
- Accounts Merge and Symmetric Tree do not appear in the Chinese reports; Accounts Merge appears once in the PDF compilation (TT-068, 2025-12-13).
