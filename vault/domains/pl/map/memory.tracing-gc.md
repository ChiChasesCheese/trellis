%% trellis:begin %%
# 追踪式垃圾回收
*内存管理*

可达性、标记-清除、复制与整理、分代假设、并发与增量回收、写屏障；Java（G1/ZGC）与 Go（并发三色、非分代、非移动）的不同选择。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/pl/map/memory.manual-raii|手动管理与 RAII]]

**Unlocks:** [[domains/pl/map/memory.escape-analysis|逃逸分析]], [[domains/pl/map/memory.memory-safety|内存安全]], [[domains/pl/map/engineering.memory-analysis|内存与分配分析]], [[domains/pl/map/signatures.java|Java 的独到之处]]

## Cards (11)
1. [[pl-memory-tracing-gc-principle]]
2. [[pl-memory-tracing-gc-foundation-mark-sweep]]
3. [[pl-memory-tracing-gc-foundation-generational]]
4. [[pl-memory-tracing-gc-foundation-concurrent-barrier]]
5. [[pl-memory-tracing-gc-foundation-java-collectors]]
6. [[pl-memory-tracing-gc-foundation-go-collector]]
7. [[pl-memory-tracing-gc-table]]
8. [[pl-memory-tracing-gc-go-vs-java]]
9. [[pl-memory-tracing-gc-best-practice]]
10. [[pl-memory-tracing-gc-pitfall-leak]]
11. [[pl-memory-tracing-gc-history]]
%% trellis:end %%

## Notes
