---
nodes: [problems.search.news-aggregator, async.queues]
tags: [problem]
---
# Drill: Design a news aggregator (Google News)

Design a system that ingests articles from about 300,000 publishers, detects when multiple
publishers are reporting the same event, and serves a fresh, ranked feed of stories per
region/language edition. Assume feed fan-out and per-user personalization are not required
— this is a shared, editorially-ranked feed, not a social timeline.

**Constraints to state and honor**
- ~2.4M articles/day, ~28 writes/sec average; publisher update frequency is power-law
  distributed (a small high-frequency tier vs. a large long-tail tier), so a single fixed
  polling interval is measurably wasteful compared to adapting per-feed.
- Near-duplicate detection must scale to ~7.2M actively-clustered articles (a 72h window)
  without pairwise comparison, and must run as articles arrive continuously, not in batches.
- A version's ranking must balance freshness against corroboration — neither raw
  chronological order nor raw source count alone is acceptable.
- Reads run at roughly 208x the write rate, but the underlying ranking score keeps drifting
  from time decay even without new writes, so a write-triggered cache alone is not correct.
- Near-duplicate clustering cannot cross languages by construction (the fingerprint is
  computed from language-specific tokens), yet a globally significant story should still be
  visible in editions with fewer native-language publishers.

**Grading points**
- Combines adaptive-interval polling, WebSub push, and a crawling fallback rather than
  relying on a single ingestion mechanism, and can state the reduction adaptive polling
  gives over a uniform interval ([[problems-news-aggregator-adaptive-polling-reduction]]).
- Chooses a single SimHash fingerprint over a multi-value MinHash signature for the
  resident near-duplicate index and can justify it by memory footprint at this design's
  scale ([[problems-news-aggregator-simhash-vs-minhash-memory]]).
- Can compute how LSH banding parameters (bands × rows) shape the candidate-pair
  probability curve as a function of true similarity
  ([[problems-news-aggregator-lsh-banding-collision-curve]]).
- Can size a multi-table Hamming-distance index (number of tables, expected candidates per
  probe) for this design's own active-corpus size rather than quoting another system's
  parameters ([[problems-news-aggregator-hamming-multitable-scale]]).
- Assigns new articles to story clusters incrementally as they arrive, rather than batch
  reclustering, and can state the consistency trade-off this accepts
  ([[problems-news-aggregator-incremental-cluster-assignment]]).
- Ranks stories with a formula that combines time decay and a log-dampened corroboration
  count, and can work through a concrete example where an older, well-corroborated story
  competes with a newer, thinly-sourced one
  ([[problems-news-aggregator-freshness-corroboration-score]]).
- Serves reads from a periodically-refreshed per-edition cache rather than a write-triggered
  one, and can explain why write-triggered invalidation alone is insufficient here
  ([[problems-news-aggregator-edition-cache-decouples-read-cost]]).
- Keeps clustering strictly per-language while adding a lightweight cross-lingual linking
  step for already-corroborated stories
  ([[problems-news-aggregator-per-language-clustering-cross-link]]).
- Explains why a message queue (not a direct call) sits between ingestion and processing
  given the irregular arrival pattern of polling, push, and crawl results
  ([[async-broker-selection]], [[async-queue-backpressure]]).

**Solution**: [[solution-news-aggregator]] — attempt first, then read. For the shared
ground on crawling politeness and frontier scheduling, see the Web Crawler solution; for
feed fan-out under a heavy read:write ratio, see the News Feed & Timeline solution.

**Attempt log**
- [ ] Attempt 1 (date, 40 min, self-graded notes):
