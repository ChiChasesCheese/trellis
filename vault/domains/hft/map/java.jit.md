%% trellis:begin %%
# JIT、分层编译、预热与去优化
*低延迟 Java*

解释执行 → C1 → C2 的分层编译（tiered compilation）、基于运行统计的激进优化、预热（warm-up）为什么必要、去优化（deoptimization）何时发生。

**Core** — part of the first pass through this subject.

**Unlocks:** [[domains/hft/map/java.safepoints|safepoint 与 GC 之外的 JVM 停顿]], [[domains/hft/map/measurement.benchmarking|微基准测试的陷阱：JMH 与 Google Benchmark]], [[domains/hft/map/java-at-hft.why-java|为什么选 Java：生产力、安全与生态]]

## Readings
- [[openjdk-jmh|JMH（Java Microbenchmark Harness）]]
- [[shipilev-jvm-anatomy|JVM Anatomy Quarks]]
- [[wiki-jit|即时编译（JIT compilation）]]

## Cards (5)
1. [[hft-java-jit-tiered]]
2. [[hft-java-jit-warmup]]
3. [[hft-java-jit-deopt]]
4. [[hft-java-jit-inlining]]
5. [[hft-java-jit-escape-analysis]]
%% trellis:end %%

## Notes
