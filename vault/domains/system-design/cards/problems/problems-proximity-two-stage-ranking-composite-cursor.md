---
id: problems-proximity-two-stage-ranking-composite-cursor
node: problems.geo.proximity
type: qa
step: 5
tags: [grown]
---
## Q
In a proximity search that ranks results by a blend of distance and rating rather than pure distance, why must candidate generation and ranking be split into two stages, and why does plain offset-based pagination (`OFFSET n LIMIT m`) break for the ranked result list?

## A
A blended distance+rating score is not monotonic in distance alone, so a spatial index that returns results ordered purely by distance cannot directly produce the final ranked order — the design must first use the spatial index to generate a widened candidate set (e.g. 1.5x the requested radius), then re-rank that candidate set by the blended score in a second stage. Offset-based pagination breaks because the candidate set can shift between page requests as businesses are added or removed, so the record at a given OFFSET drifts, causing duplicates or skipped results; a composite cursor of (blended_score, business_id) is stable because the next page starts strictly after that exact score/id pair regardless of how the rest of the candidate set changes.

## Q zh
在一个按'距离 + 评分'综合分而不是纯距离排序的邻近搜索中，为什么候选集生成和排序必须拆成两个阶段？为什么纯偏移量分页（`OFFSET n LIMIT m`）对这种排序结果会失效？

## A zh
距离和评分的综合分并不是距离的单调函数，所以一个只按纯距离排序返回结果的空间索引无法直接产出最终的排序结果——设计必须先用空间索引生成一个放宽的候选集（例如请求半径的 1.5 倍），再在第二阶段对这个候选集按综合分重排。偏移量分页会失效，是因为候选集可能在两次翻页请求之间因商户增删而变化，某个 OFFSET 对应的记录会漂移，导致翻页时看到重复或缺失的商户；而 `(综合分, business_id)` 的组合游标是稳定的，因为下一页总是严格从这个精确的分数/id 组合之后开始，不受候选集其余部分变化的影响。
