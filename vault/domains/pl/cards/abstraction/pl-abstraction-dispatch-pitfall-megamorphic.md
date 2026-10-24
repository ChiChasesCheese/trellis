---
id: pl-abstraction-dispatch-pitfall-megamorphic
node: abstraction.dispatch
type: qa
step: 9
---
## Q
Java 里一个接口调用点从「见到一种类型」变成「见到三种类型」，性能会怎样变化？

## A
在一个循环里对一个 `Shape[]`（1024 个元素，实现类为三个只做加法的 `record`）反复调用 `area()` 并求和。实测（Java 25，Apple Silicon，预热后，一次测量，仅为量级参考）：

```text
1 impl: 0.23 ns/call
3 impl: 1.31 ns/call
```

代码完全相同，只是数组里的元素类型从 1 种变成 3 种，每次调用平均慢了约 5 倍。原因：1 种类型时调用点是单态的，JIT 把 `area()` 直接内联进循环，循环还被向量化；3 种类型超过 HotSpot 内联缓存的容量（两种），调用点变成多态，只能走接口表间接调用，内联和向量化一并丢失。

生产里的症状：服务在压测（只有少数请求类型）下很快，上线后类型变杂就慢下来；或者引入一个新的实现类，其他毫不相关的热点路径也变慢，因为它们共用同一个调用点（例如统一的 `handler.process()`）。

排查与修法：用性能剖析（JFR、async-profiler）看热点是否停在 `itable stub` / `vtable stub`；热循环里按类型分桶，每个桶内调用点保持单态；或者把「封闭的小集合」改成 `sealed` + `switch`，让分支可预测。注意：不要为了一次这样的测量就全面消灭多态，仅处理已确认的热点。
