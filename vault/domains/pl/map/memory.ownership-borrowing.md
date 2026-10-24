%% trellis:begin %%
# 所有权与借用（Rust）
*内存管理*

每个值一个所有者、移动、不可变借用与可变借用互斥、借用检查器；它在编译期消除了哪几类 bug。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/pl/map/memory.manual-raii|手动管理与 RAII]], [[domains/pl/map/memory.value-reference-semantics|值语义与引用语义]]

**Unlocks:** [[domains/pl/map/memory.lifetimes|生命周期（Rust）]], [[domains/pl/map/memory.memory-safety|内存安全]], [[domains/pl/map/concurrency.data-race-freedom|数据竞争的预防]], [[domains/pl/map/engineering.api-design|地道的 API 设计]], [[domains/pl/map/signatures.rust|Rust 的独到之处]]

## Drills
- [[abstraction-mutable-key-lookup|练习：缓存明明有这个键，却总是未命中]]

## Cards (9)
1. [[pl-memory-ownership-borrowing-principle]]
2. [[pl-memory-ownership-borrowing-foundation-ownership]]
3. [[pl-memory-ownership-borrowing-foundation-borrows]]
4. [[pl-memory-ownership-borrowing-mechanism]]
5. [[pl-memory-ownership-borrowing-table]]
6. [[pl-memory-ownership-borrowing-data-race]]
7. [[pl-memory-ownership-borrowing-best-practice]]
8. [[pl-memory-ownership-borrowing-pitfall-checker]]
9. [[pl-memory-ownership-borrowing-history]]
%% trellis:end %%

## Notes
