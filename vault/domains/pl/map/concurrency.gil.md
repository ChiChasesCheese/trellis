%% trellis:begin %%
# Python GIL 与自由线程
*并发与并行*

全局解释器锁为什么存在（引用计数）、对 CPU 密集代码的影响、multiprocessing 绕开它、3.13 起的实验性 free-threaded 构建。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/pl/map/concurrency.os-threads|操作系统线程（1:1 模型）]], [[domains/pl/map/memory.reference-counting|引用计数]]

## Drills
- [[concurrency-health-check-stalls|练习：每次生成月度报表，健康检查的 p99 就跳到 250 毫秒]]

## Cards (11)
1. [[pl-conc-gil-principle]]
2. [[pl-conc-gil-found-refcount]]
3. [[pl-conc-gil-found-behavior]]
4. [[pl-conc-gil-found-escape-routes]]
5. [[pl-conc-gil-mechanism]]
6. [[pl-conc-gil-table]]
7. [[pl-conc-gil-unique-measure]]
8. [[pl-conc-gil-best-practice]]
9. [[pl-conc-gil-pitfall-nogil-races]]
10. [[pl-conc-gil-pitfall-multiprocessing]]
11. [[pl-conc-gil-evolution]]
%% trellis:end %%

## Notes
