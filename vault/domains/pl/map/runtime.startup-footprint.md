%% trellis:begin %%
# 启动时间与内存占用
*编译、运行时与性能*

Go/Rust 静态二进制毫秒启动、JVM 启动与预热、GraalVM 原生镜像与 CDS、Python 导入开销；对 CLI、Serverless、容器的影响。

**Requires:** [[domains/pl/map/runtime.jit|JIT 编译]]

**Unlocks:** [[domains/pl/map/runtime.deployment|构建产物与部署]]

## Drills
- [[runtime-first-call-and-debug-build|练习：刚发布的 Java 实例前几个请求特别慢，而 Rust 版本比 Java 还慢]]

## Cards (10)
1. [[pl-rt-startup-principle]]
2. [[pl-rt-startup-found-jvm]]
3. [[pl-rt-startup-found-python]]
4. [[pl-rt-startup-found-native]]
5. [[pl-rt-startup-mechanism-footprint]]
6. [[pl-rt-startup-table]]
7. [[pl-rt-startup-philosophy]]
8. [[pl-rt-startup-best-practice]]
9. [[pl-rt-startup-pitfall-container-heap]]
10. [[pl-rt-startup-evolution]]
%% trellis:end %%

## Notes
