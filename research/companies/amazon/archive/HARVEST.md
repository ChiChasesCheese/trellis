# Amazon OA harvest log

Method copied from stripeoa `tools/harvest.py` (2026-09-03 实测路径). 429 is normal; backoff is built in.

## Reddit (2026-09-09)

- Browser UA required. HTML is a JS shell. `.json` 403. **`.rss` works**.
- `r/leetcode/search.rss?q=amazon+oa&restrict_sr=1` → **25 posts**. Index: `harvest/reddit_leetcode_amazon_oa.txt`.
- `r/leetcode` `amazon online assessment` → **0 条**, then HTTP 429 on retry.
- `reddit-post 1w4kghq`: first session returned L5 SDE OA, 100 min, problem 1 LeetCode-style, problem 2 repo + AI assistant; Germany new-grad comment said the AI section bombed and they still advanced. Re-fetch the same day: **HTTP 429**, file left as a miss note.

## Hacker News (2026-09-09)

- `hn --q "amazon oa"` → 300 comments, almost all false positives (Kindle Oasis, Amazon the retailer). **未找到** useful OA write-ups with this query. Do not treat HN as an Amazon OA source unless the query is tighter than two common tokens.

## Official (clip, do not paraphrase as problem text)

- https://www.amazon.jobs/content/en/how-we-hire/assessments
- https://www.aboutamazon.com/about-us/leadership-principles

Problem packages are **reconstructions of reported shapes** (fulfillment / hops / windows / logs / two-sum / prefix remainder). They are not LeetCode statements. Confidence: medium on wording, high on the algorithm family.
