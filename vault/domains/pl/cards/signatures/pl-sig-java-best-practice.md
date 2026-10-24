---
id: pl-sig-java-best-practice
node: signatures.java
type: qa
step: 8
---
## Q
写现代 Java 服务有哪些核心实践？资深工程师在语言特性、JVM 参数、并发和可观测性上遵守什么规则？

## A
**规则与理由**：
1. **使用较新的 LTS（21 或 25）**：新特性（`record`、`sealed`、模式匹配、虚拟线程）显著减少样板，旧版本只会累积迁移债务。
2. **用 `record` 和 `sealed` 建模数据**：不可变、`equals`/`hashCode`/`toString` 自带；`switch` 表达式不写 `default`，让编译器检查穷尽性。
3. **默认不可变**：`final` 字段、不可变集合（`List.of`、`Map.of`），共享时不需要防御性拷贝。
4. **用组合和接口，少用继承**；框架（Spring）的魔法集中在配置和边界，业务代码保持朴素 Java。
5. **并发**：I/O 密集用虚拟线程；CPU 密集用固定大小线程池或 `ForkJoinPool`；不要手写锁，优先用 `java.util.concurrent` 的结构；避免 `synchronized` 内阻塞 I/O。
6. **JVM 参数少而精**：容器里设置 `-XX:MaxRAMPercentage`，让堆随容器内存调整；默认 G1，延迟敏感才评估 ZGC；先测量再调优，不要复制来路不明的参数清单。
7. **可观测性**：开启 GC 日志（`-Xlog:gc`），在生产使用 JFR 持续录制，监控堆、GC 暂停、线程数、类加载。
8. **预热与压测**：服务上线前用接近真实的流量预热；基准测试用 JMH。
9. **依赖管理**：BOM 统一版本，`mvn dependency:tree` 查冲突，enforcer 阻止依赖漂移。
10. **空值**：不返回 `null` 集合；返回值可能缺失用 `Optional`，字段与参数不用 `Optional`；用注解（JSpecify）声明可空性。

**何时破例**：延迟极度敏感的路径，可以用堆外内存、对象池、原始类型数组；与旧系统集成时遵守其约定，不强推新风格。

**一个判断标准**：新入职的工程师能不能在不理解 Spring 内部机制的情况下，读懂并修改业务代码？框架越透明，维护越容易。
