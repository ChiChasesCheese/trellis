%% trellis:begin %%
# Typeahead & Autocomplete
*Design Problems / Search, Crawling & Data Pipelines*

Prefix suggestions under 100 ms: tries vs precomputed top-k, sampling query logs, personalisation.

**Requires:** [[domains/system-design/map/caching.strategies|Write & Read Strategies]]

## Readings
- [[solution-typeahead|设计题解：输入联想与自动补全（Typeahead & Autocomplete）]]
- [[src-elastic-typeahead|Near real-time search]]
- [[src-linkedin-typeahead|Cleo: the open source technology behind LinkedIn's typeahead search]]
- [[src-mccandless-typeahead|Using Finite State Transducers in Lucene]]

## Drills
- [[design-typeahead|Drill: Design a typeahead / autocomplete suggestion service]]

## Cards (8)
1. [[problems-typeahead-6x-suggest-ratio-drives-precompute]]
2. [[problems-typeahead-precomputed-topk-vs-onthefly-dfs]]
3. [[problems-typeahead-trie-cache-vs-fst-tradeoff]]
4. [[problems-typeahead-uniform-sampling-loses-long-tail]]
5. [[problems-typeahead-trending-booster-patch-layer]]
6. [[problems-typeahead-personalization-overlay-not-duplicated-structure]]
7. [[problems-typeahead-hot-prefix-replication]]
8. [[problems-typeahead-10x-hot-cold-split-fst]]
%% trellis:end %%

## Notes
