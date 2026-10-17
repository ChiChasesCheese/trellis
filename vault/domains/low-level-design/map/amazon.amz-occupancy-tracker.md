%% trellis:begin %%
# 办公室人数追踪（Occupancy Tracker）（low priority）
*Amazon 专项（Amazon OOD）*

刷卡进出事件，查询任意时刻楼里有多少人：事件溯源、前缀和加二分、同一模型的 SQL 写法。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/low-level-design/map/structure.storage|内存持久化（In-Memory Persistence）]]

## Readings
- [[solution-amz-occupancy-tracker|设计题解：办公室人数追踪（Occupancy Tracker）（low priority）]]

## Drills
- [[design-amz-occupancy-tracker|Drill：办公室人数追踪（Occupancy Tracker）]]

## Cards (9)
1. [[amz-occupancy-tracker-how-asked-and-three-questions]]
2. [[amz-occupancy-tracker-objects-and-their-jobs]]
3. [[amz-occupancy-tracker-stage1-enter-leave-in-code]]
4. [[amz-occupancy-tracker-count-at-prefix-sum-and-bisect]]
5. [[amz-occupancy-tracker-decision-range-max-start-count-and-segment-tree]]
6. [[amz-occupancy-tracker-followup-zones-peaks-do-not-add]]
7. [[amz-occupancy-tracker-failure-path-duplicate-and-late-events]]
8. [[amz-occupancy-tracker-sql-version-and-scale]]
9. [[amz-occupancy-tracker-concurrency-validate-and-append-under-one-lock]]
%% trellis:end %%

## Notes
