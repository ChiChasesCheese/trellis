---
nodes: [problems.search.typeahead, caching.strategies]
tags: [problem]
---
# Drill: Design a typeahead / autocomplete suggestion service

Design the suggestion box for a search bar with 300M DAU: every keystroke can trigger a
request for a ranked list of completions for the current prefix, and the whole
keystroke-to-render experience must feel instant.

**Constraints to state and honor**
- 300M DAU, ~900M submitted searches/day, ~62,500 average suggestion QPS (peak ~312,500)
  — about 6x the submitted-search QPS.
- The precomputed prefix structure must fit comfortably in memory (~12GB realistic, ~60GB
  worst case for this design's assumptions).
- End-to-end latency (keystroke to rendered suggestions) P99 < 100ms, including the client.
- A newly-trending query should reach suggestions within about an hour, not a full batch
  cycle.

**Grading points**
- Explains why per-request computation (querying logs or running a model on the request
  path) is infeasible at this QPS/latency combination, and precomputes instead
  ([[problems-typeahead-6x-suggest-ratio-drives-precompute]]).
- Chooses a trie with a precomputed top-K cached at each node over computing top-K via
  on-the-fly subtree traversal ([[problems-typeahead-precomputed-topk-vs-onthefly-dfs]]).
- Weighs a mutable trie-with-cache against a more memory-efficient but rebuild-only FST,
  and picks correctly given the freshness requirement
  ([[problems-typeahead-trie-cache-vs-fst-tradeoff]]).
- Recognizes that uniform sampling of query logs at larger scale silently drops long-tail
  queries, and applies sampling asymmetrically
  ([[problems-typeahead-uniform-sampling-loses-long-tail]]).
- Adds a streaming trending-booster patch layer on top of a daily batch baseline instead of
  waiting for the next full batch run ([[problems-typeahead-trending-booster-patch-layer]]).
- Implements personalization as a lightweight per-request rerank against a small per-user
  history, not a duplicated per-user structure
  ([[problems-typeahead-personalization-overlay-not-duplicated-structure]]).
- Handles a single hot/viral prefix with replicated read replicas routed by request
  identity, not by adding more shards ([[problems-typeahead-hot-prefix-replication]]).
- Explains why the prefix cache is a cache-aside style read-optimized structure rebuilt
  from a pipeline, not a source of truth, and how it would be warmed after a flush
  ([[caching-aside-vs-read-through]], [[caching-cache-warming]]).

**Solution**: [[solution-typeahead]] — attempt first, then read.

**Attempt log**
- [ ] Attempt 1 (date, 40 min, self-graded notes):
