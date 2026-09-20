%% trellis:begin %%
# 带过期时间的缓存（TTL Cache）
*设计题（Design Problems） / 基础组件*

惰性过期与主动清理、可注入时钟、与淘汰策略组合。

**Requires:** [[domains/low-level-design/map/structure.api|进程内 API 设计]]

## Readings
- [[solution-ttl-cache|设计题解：带过期时间的缓存（TTL Cache）]]
- [[src-anomaly2104-ttl-cache|anomaly2104/cache-low-level-system-design — Cache low level design]]
- [[src-interviewready-ttl-cache|InterviewReady/Low-Level-Design — distributed-cache]]
- [[src-pythondocs-ttl-cache|heapq — Heap queue algorithm（Priority Queue Implementation Notes）]]

## Drills
- [[design-ttl-cache|Drill：带过期时间的缓存（TTL Cache）]]

## Cards (8)
1. [[problems-ttl-cache-three-ways-to-expire]]
2. [[problems-ttl-cache-absolute-deadline-not-remaining]]
3. [[problems-ttl-cache-tombstones-must-be-compacted]]
4. [[problems-ttl-cache-heap-tuple-needs-a-counter]]
5. [[problems-ttl-cache-expired-is-invisible]]
6. [[problems-ttl-cache-evict-by-policy-or-deadline]]
7. [[problems-ttl-cache-single-flight]]
8. [[problems-ttl-cache-stats-and-callback-refuse-patterns]]
%% trellis:end %%

## Notes
