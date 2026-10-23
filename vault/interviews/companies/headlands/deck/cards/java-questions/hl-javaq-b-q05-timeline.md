---
id: hl-javaq-b-q05-timeline
node: java-questions.b-versions
type: qa
step: 2
---
## Q
按版本列出 Java 8 到 21 的关键特性：8、9、10、11、14–16、17、21 各引入了什么？

## A
- **8（2014）**：lambda、方法引用、Stream、Optional、`java.time`、接口 `default` 方法、`CompletableFuture`。
- **9（2017）**：模块系统（JPMS）、`List.of / Set.of / Map.of`、**G1 成为默认 GC**、紧凑字符串（JEP 254）、字符串拼接走 `invokedynamic`（JEP 280）。
- **10**：`var`（局部变量类型推断）。
- **11（LTS）**：`String.isBlank / lines / strip / repeat`、HttpClient、单文件运行 `java Foo.java`、JFR 开源。
- **14–16**：`switch` 表达式（14）、文本块（15）、record（16）、`instanceof` 模式（16）、`Stream.toList`（16）。
- **17（LTS）**：sealed 类、强封装 JDK 内部。
- **21（LTS）**：虚拟线程（JEP 444）、`switch` 模式匹配（441）、record 模式（440）、Sequenced Collections（431）、分代 ZGC（439）。
- 21 里的**预览**特性：结构化并发、`ScopedValue`、未命名变量、FFM API。
