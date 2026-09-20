---
id: problems-tinder-index-side-filter-terms-cap
node: problems.social.tinder
type: qa
step: 5
tags: [grown]
---
## Q
A design that filters out already-swiped candidates by adding a `must_not terms` clause (listing every swiped user id) directly to the candidate search query hits a real limit: Elasticsearch defaults `index.max_terms_count` to 65,536 terms per query. If a heavy user with 3 years of daily use at 150 swipes/day has swiped 164,250 people, what happens to this index-side filtering approach, and what does it argue for instead?

## A
164,250 exceeds the default 65,536-term cap by about 2.5x, so the query fails or requires repeatedly raising the limit at the cost of worse query performance — the approach breaks down exactly for the heavy-user population this design must support. This argues for filtering with a compact per-user Bloom filter checked after (or alongside) the geo/preference index query, rather than folding the entire seen-set into the index query's term list, since a Bloom filter's size doesn't run into a hard per-query term-count ceiling.

## Q zh
一种设计通过把每一个划过的用户 id 列成 `must_not terms` 子句直接加进候选人搜索查询里来排除已划过的候选人，这会撞上一个真实限制：Elasticsearch 默认把 `index.max_terms_count` 设为每次查询 65,536 个词项。如果一个用了 3 年、平均每天滑动 150 次的重度用户已经划过 164,250 人，这种索引侧过滤方案会怎样？这说明应该改用什么方案？

## A zh
164,250 超出默认的 65,536 词项上限约 2.5 倍，查询会直接失败，或者需要不断调高上限、以更差的查询性能为代价——这个方案恰好在这道题必须覆盖的重度用户群体规模上失效。这说明应该改用紧凑的每用户 Bloom filter，在地理/偏好索引查询之后（或旁边）做过滤，而不是把整个 seen set 塞进索引查询的词项列表里，因为 Bloom filter 的大小不会撞上单次查询的词项数硬上限。
