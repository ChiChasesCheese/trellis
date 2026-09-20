---
nodes: [problems.search.search-engine, storage.search]
tags: [problem]
---
# Drill: Design a search engine / post search for a social network

Design a search feature over a corpus of 500M-DAU social posts (or, as a variant, a
web-scale search engine): users type keywords, get back matching posts/pages, and can sort
results by relevance, recency, or like count. New posts must become searchable quickly, and
the corpus keeps changing under the index (new posts, changing like counts, deletions).

**Constraints to state and honor**
- 500M DAU, ~32.5M posts/day, ~1,157 average search QPS (peak ~5,787).
- ~12.81TB of postings over a 5-year searchable window, implying ~32 index shards.
- Query latency P99 < 300ms; new content searchable P99 < 10s.
- The index is a derived view of the system of record, never written to directly.

**Grading points**
- Explains why a search cluster is a derived, rebuildable view and never the system of
  record, using CDC-style sync from the database ([[storage-search-sync]],
  [[storage-search-not-sot]], [[problems-search-engine-derived-index-not-writable-directly]]).
- Chooses document-partitioning over term-partitioning and quantifies why Zipfian term
  skew makes term-partitioning's narrower fan-out not worth its hot-shard risk
  ([[problems-search-engine-doc-vs-term-partitioning-zipf-skew]]).
- Connects the shard count derived from storage capacity to query fan-out width and
  explains why that count matters more than the raw storage size
  ([[problems-search-engine-5yr-shard-count-drives-fanout]]).
- Mitigates fan-out tail latency with hedged requests and can compute the resulting drop
  in miss probability ([[problems-search-engine-hedged-requests-tail-latency]]).
- Explains the NRT refresh mechanism (segments become visible only after a refresh,
  durability via translog is separate) ([[storage-search-nrt-refresh]],
  [[storage-search-segments]]).
- Designs ranking as a narrowing multi-pass funnel instead of scoring every AND-candidate
  with an expensive model ([[problems-search-engine-multipass-candidate-funnel]]).
- Handles sort-by-like-count on a fast-changing corpus with milestone batching plus an
  over-fetch-and-rerank step against live counts
  ([[problems-search-engine-like-milestone-batching]]).
- States a concrete degradation path for an unavailable shard (partial results, not a
  failed query) ([[problems-search-engine-partial-results-on-shard-failure]]).
- Reasons about how shard count and fan-out width grow at 10x scale, and how that compares
  to a web-scale corpus ([[problems-search-engine-10x-shard-growth-vs-web-scale]]).

**Solution**: [[solution-search-engine]] — attempt first, then read.

**Attempt log**
- [ ] Attempt 1 (date, 40 min, self-graded notes):
