%% trellis:begin %%
# 数据竞争的预防
*并发与并行*

Rust 用 Send/Sync 在编译期禁止数据竞争、Go 的 race detector、Java 靠纪律与工具、Python GIL 带来的错觉。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/pl/map/concurrency.atomics-memory-models|原子操作与内存模型]], [[domains/pl/map/memory.ownership-borrowing|所有权与借用（Rust）]]

**Unlocks:** [[domains/pl/map/signatures.rust|Rust 的独到之处]]

## Cards (10)
1. [[pl-conc-datarace-principle]]
2. [[pl-conc-datarace-found-send-sync]]
3. [[pl-conc-datarace-found-race-detector]]
4. [[pl-conc-datarace-mechanism]]
5. [[pl-conc-datarace-table]]
6. [[pl-conc-datarace-unique-gil-illusion]]
7. [[pl-conc-datarace-unique-failfast]]
8. [[pl-conc-datarace-best-practice]]
9. [[pl-conc-datarace-pitfall-check-then-act]]
10. [[pl-conc-datarace-history]]
%% trellis:end %%

## Notes
