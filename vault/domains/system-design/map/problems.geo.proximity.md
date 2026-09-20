%% trellis:begin %%
# Proximity & Nearby Search (Yelp)
*Design Problems / Location & Mobility*

Geohash vs quadtree vs S2, read-heavy place search, and nearby friends on moving data.

**Core** — part of the first pass through this subject.

**Requires:** [[domains/system-design/map/storage.relational.indexing|Indexing]]

## Readings
- [[solution-proximity|设计题解：邻近搜索（Proximity & Nearby Search，Yelp）]]
- [[src-bytebytego-proximity|Proximity Service]]
- [[src-google-s2|S2 Geometry Library]]
- [[src-hellointerview-yelp|Yelp]]
- [[src-redis-geoadd|GEOADD]]
- [[src-uber-blog-h3|H3: Uber's Hexagonal Hierarchical Spatial Index]]
- [[src-wikipedia-geohash|Geohash]]

## Drills
- [[design-proximity|Drill: Design a proximity search service like Yelp]]

## Cards (8)
1. [[problems-proximity-index-fits-in-memory]]
2. [[problems-proximity-geohash-vs-quadtree-density]]
3. [[problems-proximity-s2-hilbert-vs-geohash-zorder]]
4. [[problems-proximity-h3-uniform-neighbor-distance]]
5. [[problems-proximity-two-stage-ranking-composite-cursor]]
6. [[problems-proximity-nearby-friends-pull-vs-push]]
7. [[problems-proximity-double-buffer-index-outage]]
8. [[problems-proximity-10x-geo-sharding-boundary]]
%% trellis:end %%

## Notes
