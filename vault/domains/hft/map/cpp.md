%% trellis:begin %%
# 低延迟 C++

HFT 交易热路径的主力语言，以及让 C++ 代码稳定跑在纳秒级的惯用法：不分配、静态分派、缓存友好容器、原子操作与无锁队列。

## Topics
- [[domains/hft/map/cpp.why-cpp|为什么交易热路径用 C++]]
- [[domains/hft/map/cpp.no-alloc|热路径不分配内存：对象池与 arena]]
- [[domains/hft/map/cpp.static-dispatch|静态分派：模板、CRTP 与虚函数的代价]]
- [[domains/hft/map/cpp.compile-time|编译期计算：constexpr 与查表]]
- [[domains/hft/map/cpp.containers|容器选择：vector、扁平哈希表]]
- [[domains/hft/map/cpp.compiler|让编译器帮你：内联、likely 提示、PGO 与看汇编]]
- [[domains/hft/map/cpp.atomics|std::atomic 与 memory_order]]
- [[domains/hft/map/cpp.spsc-seqlock|SPSC 环形队列与 seqlock]]
- [[domains/hft/map/cpp.warm-cache|缓存预热：让热路径保持热]]
- [[domains/hft/map/cpp.errors-logging|异常、错误处理与日志离开热路径]]
%% trellis:end %%

## Notes
