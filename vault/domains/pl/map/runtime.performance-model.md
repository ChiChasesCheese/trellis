%% trellis:begin %%
# 性能模型：慢在哪里
*编译、运行时与性能*

同一段代码在四门语言里的典型速度量级，以及差距来自哪里：解释开销、装箱与指针追逐、GC、边界检查、动态分派。

**Requires:** [[domains/pl/map/runtime.jit|JIT 编译]], [[domains/pl/map/runtime.cpython-internals|CPython 解释器]], [[domains/pl/map/memory.memory-layout|内存布局与对象开销]]

**Unlocks:** [[domains/pl/map/engineering.profiling|性能剖析]]

## Drills
- [[runtime-first-call-and-debug-build|练习：刚发布的 Java 实例前几个请求特别慢，而 Rust 版本比 Java 还慢]]

## Cards (10)
1. [[pl-rt-perf-principle]]
2. [[pl-rt-perf-found-cache]]
3. [[pl-rt-perf-found-boxing]]
4. [[pl-rt-perf-found-alloc]]
5. [[pl-rt-perf-mechanism-ladder]]
6. [[pl-rt-perf-table]]
7. [[pl-rt-perf-philosophy]]
8. [[pl-rt-perf-best-practice]]
9. [[pl-rt-perf-pitfall-pointer-chasing]]
10. [[pl-rt-perf-evolution]]
%% trellis:end %%

## Notes
