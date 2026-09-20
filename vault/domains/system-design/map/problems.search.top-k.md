%% trellis:begin %%
# Top-K & Trending (Heavy Hitters)
*Design Problems / Search, Crawling & Data Pipelines*

Most-viewed over sliding windows: exact vs approximate counting, count-min sketch, stream aggregation.

**Requires:** [[domains/system-design/map/async.streaming.processing|Stream Processing]]

## Readings
- [[solution-top-k|设计题解：实时热门榜与 Top-K 统计（Top-K & Trending / Heavy Hitters）]]
- [[src-cormode-muthukrishnan-top-k|An Improved Data Stream Summary: The Count-Min Sketch and its Applications]]
- [[src-donnemartin-top-k|Design Amazon's sales rank by category feature]]
- [[src-hellointerview-top-k|Top K Problem Breakdown]]
- [[src-metwally-space-saving-top-k|Efficient Computation of Frequent and Top-k Elements in Data Streams]]

## Drills
- [[design-top-k|Drill: Design a real-time Top-K / trending leaderboard]]

## Cards (8)
1. [[problems-top-k-cms-error-bound]]
2. [[problems-top-k-partition-by-item-id-exact-merge]]
3. [[problems-top-k-cms-vs-space-saving-tradeoff]]
4. [[problems-top-k-space-saving-guarantee]]
5. [[problems-top-k-hierarchical-window-rollup]]
6. [[problems-top-k-dimension-sharding-merge-correctness]]
7. [[problems-top-k-hot-item-salting]]
8. [[problems-top-k-10x-tree-merge]]
%% trellis:end %%

## Notes
