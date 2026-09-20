%% trellis:begin %%
# 线程、GIL 与内存模型
*并发（Concurrency）*

并发与并行、GIL 保护了什么又没保护什么、为什么 `x += 1` 仍然不是原子的、线程/进程/协程的选择。

**Core** — part of the first pass through this subject.

**Unlocks:** [[domains/low-level-design/map/concurrency.primitives|同步原语（threading）]], [[domains/low-level-design/map/concurrency.asyncio|asyncio 与协程]]

## Readings
- [[java-concurrency-in-practice|Java Concurrency in Practice (Goetz et al.)]]
- [[jenkov-java-memory-model|Java Memory Model (Jakob Jenkov)]]

## Cards (6)
1. [[concurrency-gil-definition]]
2. [[concurrency-augmented-assignment-not-atomic]]
3. [[concurrency-check-then-act]]
4. [[concurrency-gil-myth-invariants]]
5. [[concurrency-cpu-vs-io-bound-choice]]
6. [[concurrency-free-threading-pep703]]
%% trellis:end %%

## Notes
