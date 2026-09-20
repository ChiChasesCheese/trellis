---
nodes: [problems.social.news-feed, caching.strategies, async.queues]
tags: [problem]
---
# Drill: Design a news feed / timeline like Twitter or Facebook

Design the home timeline for a social network with 200M daily active users: users follow
each other, post text updates, and see a ranked feed of their followees' posts. Follower
counts are heavily skewed — most accounts have a few hundred followers, but a tiny fraction
have millions.

**Constraints to state and honor**
- 200M DAU, ~4M posts/day, ~4.8B feed reads/day (a read:write ratio around 1,200:1).
- Each user's precomputed home timeline (inbox) caps at 800 entries.
- Feed reads must stay P99 < 200ms; new posts from ordinary accounts should reach
  followers' timelines P99 < 5s.
- The feed is ranked, not purely reverse-chronological, and must paginate correctly while
  new posts keep arriving.

**Grading points**
- Chooses fan-out on write for ordinary accounts (precomputing each follower's inbox) and
  explains why the read:write ratio makes read-time aggregation unaffordable at this scale
  ([[problems-news-feed-read-write-ratio-drives-precompute]]).
- Identifies that a small fraction of high-follower accounts dominates write amplification
  under naive full fan-out, and excludes them from push in favor of read-time merging,
  quantifying the resulting reduction ([[problems-news-feed-hybrid-fanout-threshold]]).
- Handles a viral post's read-side hot key with a redundant/replicated cache rather than
  just adding more shards ([[problems-news-feed-redundant-cache-hot-key]]).
- Designs ranking as a narrowing multi-pass funnel instead of running an expensive model on
  every candidate ([[problems-news-feed-multipass-ranking-funnel]]).
- Caps the precomputed inbox at a fixed size and explains why an unbounded inbox degrades
  over time, not just at launch ([[problems-news-feed-capped-inbox-vs-unbounded]]).
- Uses a composite (score, postId) pagination cursor for the ranked feed rather than a
  plain timestamp, and explains why timestamp-only pagination breaks
  ([[problems-news-feed-composite-pagination-cursor]]).
- States a concrete degradation path when the inbox cache is unavailable — real-time
  fan-out on read reconstruction, not an outright feed outage
  ([[problems-news-feed-inbox-cache-outage-degradation]]).
- Describes how the inbox cache scales at 10x DAU by physical sharding rather than growing
  one cluster indefinitely ([[problems-news-feed-10x-physical-shard-inbox]]).

**Solution**: [[solution-news-feed]] — attempt first, then read.

**Attempt log**
- [ ] Attempt 1 (date, 40 min, self-graded notes):
