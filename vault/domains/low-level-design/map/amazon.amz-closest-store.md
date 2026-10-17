%% trellis:begin %%
# 增删查最近值（Add / Remove / Closest）
*Amazon 专项（Amazon OOD）*

电面 OOD：维护一组数，支持插入、删除、查询离 target 最近的数；从排序列表到值域分桶。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/low-level-design/map/python.data-model|数据模型与特殊方法（Data Model）]], [[domains/low-level-design/map/oop.interfaces|接口与抽象基类]]

## Readings
- [[solution-amz-closest-store|设计题解：增删查最近值（Add / Remove / Closest）]]
- [[src-python-bisect-amz-closest-store|bisect — Array bisection algorithm（Python 标准库文档）]]

## Drills
- [[design-amz-closest-store|Drill：增删查最近值（Add / Remove / Closest）]]

## Cards (9)
1. [[amz-closest-store-how-asked-and-three-questions]]
2. [[amz-closest-store-objects-and-their-jobs]]
3. [[amz-closest-store-stage1-closest-with-bisect]]
4. [[amz-closest-store-data-structure-sorted-list-vs-fenwick]]
5. [[amz-closest-store-seam-only-where-two-implementations]]
6. [[amz-closest-store-followup-range-constraint-fenwick]]
7. [[amz-closest-store-failure-path-remove-missing]]
8. [[amz-closest-store-concurrency-one-lock-two-reads]]
9. [[amz-closest-store-common-mistake-one-candidate]]
%% trellis:end %%

## Notes
