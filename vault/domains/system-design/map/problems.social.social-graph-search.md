%% trellis:begin %%
# Social Graph & Friend Search
*Design Problems / Social, Feeds & Messaging*

Storing a graph of billions of edges and answering degree-of-separation and mutual-friend queries.

**Requires:** [[domains/system-design/map/distributed.partitioning.schemes|Hash vs Range]]

## Readings
- [[solution-social-graph-search|设计题解：社交关系图谱与好友检索（Social Graph & Friend Search）]]
- [[src-donnemartin-social-graph-search|system-design-primer — Design Facebook's Friend Search]]
- [[src-fbresearch-social-graph-search|Three and a Half Degrees of Separation]]
- [[src-flockdb-social-graph-search|Twitter — FlockDB]]
- [[src-usenix-tao-social-graph-search|TAO: Facebook's Distributed Data Store for the Social Graph]]
- [[src-vldb-unicorn-social-graph-search|Unicorn: A System for Searching the Social Graph]]

## Drills
- [[design-social-graph-search|Drill: Design a social graph store with friend search, like Facebook's friend graph]]

## Cards (8)
1. [[problems-social-graph-search-graph-partitioning-decay]]
2. [[problems-social-graph-search-mutual-friends-two-shard-cost]]
3. [[problems-social-graph-search-typed-edge-inverted-index]]
4. [[problems-social-graph-search-raw-edge-cache-vs-feed-inbox]]
5. [[problems-social-graph-search-bidirectional-bfs-exponent-halving]]
6. [[problems-social-graph-search-why-not-precompute-all-pairs-shortest-path]]
7. [[problems-social-graph-search-strong-consistency-tradeoff-by-write-volume]]
8. [[problems-social-graph-search-high-degree-node-hotspot]]
%% trellis:end %%

## Notes
