%% trellis:begin %%
# 内存布局与对象开销
*内存管理*

对象头、指针间接、字段内联：Java 对象头与装箱、Python 对象开销、Go/Rust 结构体按值内联；缓存友好性与 Valhalla 值类型。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/pl/map/memory.value-reference-semantics|值语义与引用语义]]

**Unlocks:** [[domains/pl/map/runtime.performance-model|性能模型：慢在哪里]], [[domains/pl/map/trends.value-types|值类型与数据导向]]

## Cards (9)
1. [[pl-memory-memory-layout-principle]]
2. [[pl-memory-memory-layout-foundation-padding]]
3. [[pl-memory-memory-layout-foundation-headers-boxing]]
4. [[pl-memory-memory-layout-foundation-cache-locality]]
5. [[pl-memory-memory-layout-table]]
6. [[pl-memory-memory-layout-rust-control]]
7. [[pl-memory-memory-layout-best-practice]]
8. [[pl-memory-memory-layout-pitfall-pointers]]
9. [[pl-memory-memory-layout-history]]
%% trellis:end %%

## Notes
