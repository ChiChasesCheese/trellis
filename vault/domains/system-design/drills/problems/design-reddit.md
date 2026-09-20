---
nodes: [problems.social.reddit, caching.strategies]
tags: [problem]
---
# Drill: Design a forum with voting and nested comments, like Reddit

Design the core of a Reddit-style forum with 100M daily active users posting into about
150,000 communities (subreddits). Users upvote/downvote posts and comments, reply to form
arbitrarily deep nested comment trees, and browse each community's "hot" listing, which
must re-rank quickly as new votes arrive.

**Constraints to state and honor**
- 100M DAU, ~2M posts/day, ~60M comments/day, ~1.2B votes/day (peak vote QPS ≈ 83,333).
- Hot-listing reads must stay P99 < 200ms; a vote's effect on ranking must be visible
  P99 < 5s; a submitted comment must be visible to other readers P99 < 2s.
- A single viral post can absorb a large share of site-wide vote traffic on one target.
- Comment threads can reach tens of thousands of comments on a single post and must
  support "load more" pagination rather than loading the whole tree at once.

**Grading points**
- Sizes the hot-listing cache per community rather than per user, and explains why it
  barely grows with DAU compared to a per-follower feed's inbox cache
  ([[problems-reddit-per-community-vs-per-user-cache]]).
- Chooses an adjacency list with a `(parentId, score)` index for the comment tree over a
  closure table, and quantifies the write amplification the closure table would add
  ([[problems-reddit-adjacency-list-vs-closure-table]]).
- Designs the hot-ranking score as a pure function of a post's own vote count and creation
  time, so a vote only triggers recomputing and reinserting that one post, not a periodic
  full-site rescan ([[problems-reddit-hot-score-pure-function]]).
- Ranks comments by a confidence lower bound rather than a raw upvote ratio, and can show a
  concrete case where the raw ratio gets the order wrong ([[problems-reddit-wilson-score-vs-average]]).
- Makes votes idempotent through the natural key `(userId, targetId, targetType)` rather
  than a client-supplied token ([[problems-reddit-vote-idempotency-natural-key]]).
- Separates the displayed vote count from the value the ranking function actually uses,
  and explains why that separation doesn't affect ranking correctness
  ([[problems-reddit-vote-fuzzing-display-vs-ranking]]).
- States a concrete mitigation for a single viral post's vote-counter write hot key
  (sharding into sub-counters) rather than assuming more shards alone dilutes it
  ([[problems-reddit-viral-post-write-hotkey-sharding]]).
- Explains what does and doesn't change at 10x DAU given a cache sized by community count,
  not user count ([[problems-reddit-10x-cache-decoupled-from-dau]]).

**Solution**: [[solution-reddit]] — attempt first, then read.

**Attempt log**
- [ ] Attempt 1 (date, 40 min, self-graded notes):
