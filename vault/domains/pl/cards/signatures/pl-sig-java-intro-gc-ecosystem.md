---
id: pl-sig-java-intro-gc-ecosystem
node: signatures.java
type: qa
step: 3
---
## Q
Java 的可选垃圾回收器（G1、ZGC 等）和它的生态（Maven Central、Spring、企业框架）为什么是同等重要的“独到之处”？

## A
**垃圾回收器的选择**：JVM 允许在启动时选择收集算法，不同算法对应不同目标：
- **G1**（JDK 9 起默认）：分区的、以暂停时间为目标的收集器，在吞吐与延迟间折中。本机观察：默认选择 `UseG1GC = true`，一次年轻代暂停约 0.3 ms。
- **ZGC / 分代 ZGC**：并发整理的低延迟收集器，暂停通常在 1 ms 以内，堆可达 TB 级，适合延迟敏感的在线服务。
- **Parallel GC**：吞吐优先，适合批处理。
- **Serial GC**：单线程，适合小堆、容器里的小进程。

选择不需要改代码，只改启动参数（如 `-XX:+UseZGC`）。配合 JFR、GC 日志可以看到每次暂停和分配速率，调优有数据可依。

**生态**：
- **构建与依赖**：Maven Central 上有海量库，所有主流企业软件都提供 Java SDK。
- **框架**：Spring（依赖注入、Web、数据访问）几乎成为企业 Java 的事实标准，Hibernate/JPA、JUnit、Mockito 等。
- **大数据与基础设施**：Hadoop、Spark、Kafka、Cassandra、Elasticsearch、Flink 用 Java 或 JVM 语言写成，Java 的运行时特性直接影响它们的表现。
- **JVM 语言**：Kotlin、Scala、Clojure 运行在同一个平台上，共享库和工具。
- **工具**：IDE（IntelliJ）、调试器、性能分析器（JFR、async-profiler）、字节码工具成熟度领先。

**为什么二者同等重要**：企业选择 Java，是在选“十年后仍然有人懂、有库、有工具、有性能调优手段”。生态降低了建设成本，可选的 GC 与可观测性降低了运维风险；单有语言特性，不足以撑起这样的决定。

**代价**：配置项和选择过多，团队需要有人懂 GC 和 JVM 调优；框架（Spring）带来大量“魔法”，增加了理解门槛。

**要记住的一点**：Java 的竞争力在平台和生态，语言本身在三十年里并不是最先进的，却是最“经得起时间”的之一。
