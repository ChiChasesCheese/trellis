%% trellis:begin %%
# 逃逸分析
*内存管理*

编译器判断对象是否会离开函数，决定栈分配还是堆分配：Go 编译期逃逸分析、Java JIT 的标量替换。

**Core** — part of the first pass through this subject.

**Requires:** [[domains/pl/map/memory.stack-heap|栈与堆]], [[domains/pl/map/memory.tracing-gc|追踪式垃圾回收]]

## Cards (9)
1. [[pl-memory-escape-analysis-principle]]
2. [[pl-memory-escape-analysis-foundation-go]]
3. [[pl-memory-escape-analysis-foundation-java-jit]]
4. [[pl-memory-escape-analysis-mechanism]]
5. [[pl-memory-escape-analysis-table]]
6. [[pl-memory-escape-analysis-go-visible]]
7. [[pl-memory-escape-analysis-best-practice]]
8. [[pl-memory-escape-analysis-pitfall-assumptions]]
9. [[pl-memory-escape-analysis-history]]
%% trellis:end %%

## Notes
