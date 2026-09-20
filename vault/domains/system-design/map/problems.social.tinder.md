%% trellis:begin %%
# Dating & Matching (Tinder)
*Design Problems / Social, Feeds & Messaging*

Geo-filtered candidate feeds, swipes at high write rates, and exactly-once match detection.

**Requires:** [[domains/system-design/map/distributed.consistency|Consistency Models]]

## Readings
- [[solution-tinder|设计题解：约会与匹配（Dating & Matching，Tinder）]]
- [[src-elastic-tinder|Elasticsearch: Terms query]]
- [[src-tindereng-elasticache-tinder|Taming ElastiCache with Auto-discovery at Scale]]
- [[src-tindereng-geosharding1-tinder|Geosharded Recommendations Part 1: Sharding Approach]]
- [[src-tindereng-geosharding2-tinder|Geosharded Recommendations Part 2: Architecture]]
- [[src-tindereng-geosharding3-tinder|Geosharded Recommendations Part 3: Consistency]]

## Drills
- [[design-tinder|Drill: Design a dating app's candidate feed and matching engine like Tinder]]

## Cards (8)
1. [[problems-tinder-swipe-write-forces-wide-column]]
2. [[problems-tinder-match-gate-safety-margin]]
3. [[problems-tinder-bidirectional-preference-filter]]
4. [[problems-tinder-bloom-filter-storage-reduction]]
5. [[problems-tinder-index-side-filter-terms-cap]]
6. [[problems-tinder-match-detection-canonical-pair-key]]
7. [[problems-tinder-geoshard-timezone-imbalance]]
8. [[problems-tinder-10x-match-gate-sharding]]
%% trellis:end %%

## Notes
