---
id: hl-javaq-e-q23-options
node: java-questions.e-jit-gc
type: qa
step: 21
---
## Q
低延迟 Java 服务的 GC 与堆参数应该怎么设？ZGC 和 G1 各自的取舍是什么？

## A
- **分代 ZGC**：目标暂停 <1 ms，与堆大小无关；吞吐略低，需要 CPU 余量（并发线程）和**堆余量**。21 里分代需显式 `-XX:+ZGenerational`（后续版本才逐步默认，别在 21 里假设）。
- **G1**：`-XX:MaxGCPauseMillis`（软目标）；停顿随存活数据量 / 晋升量波动。
- `-Xms == -Xmx`：避免动态扩缩。
- `-XX:+AlwaysPreTouch`：启动时触碰所有页，避免运行时页错误；代价是启动更慢、RSS 一次性占满。
- 大页（THP / HugePages）有利有弊，需测；容器里确认 JVM 看到的核数（决定 GC 线程数）。
- 不要靠 `System.gc()`；`-XX:+DisableExplicitGC` 视情况。
