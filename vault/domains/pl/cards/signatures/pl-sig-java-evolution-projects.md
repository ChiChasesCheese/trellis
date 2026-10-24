---
id: pl-sig-java-evolution-projects
node: signatures.java
type: qa
step: 10
---
## Q
Java 的长期演进由哪几个“项目”（Loom、Valhalla、Panama、Leyden 等）驱动？它们分别在补什么缺口？

## A
Java 的重大演进以 OpenJDK 的项目组织，每个项目针对一个**结构性缺口**，历时多年，分阶段发布：

- **Project Loom（并发）**：虚拟线程（Java 21 定稿）、结构化并发（预览中）、作用域值。目标：不改变同步编程模型，让百万级并发成为可能。
- **Project Valhalla（数据布局）**：值类和值对象，让小而不可变的数据放弃对象身份、被扁平存放，减少指针追逐；最终让泛型支持原始类型特化。本机 Java 25 的编译器仍不接受 `value class`，说明尚未落地。
- **Project Panama（原生互操作）**：外部函数与内存 API（Foreign Function & Memory），取代 JNI，安全高效地调用 C 库与访问堆外内存。
- **Project Leyden（启动与足迹）**：把更多工作提前到构建期，缩短启动与预热时间，类似提前编译、缓存已解析的类与剖析数据。
- **Project Amber（语言生产力）**：`var`、`record`、`sealed`、模式匹配、文本块、`switch` 表达式等小而精的语言特性。
- **Project Lilliput（对象头压缩）**：缩小对象头以降低内存占用。

**规律**：
1. 每一项都对应前文提到的 Java 弱点——启动、足迹、数据布局、冗长、原生互操作、并发。
2. 都**不破坏兼容**，通过新增 API、预览特性、运行时选项推出。
3. 节奏慢但方向稳：从提案到稳定常需三到八年。

**对比**：Go 的演进主要在标准库和工具；Rust 的演进是语言层加 edition；Python 的演进是语言加解释器（JIT、自由线程）。Java 的演进主要是**平台层**。

**对使用者的建议**：关注 LTS 版本发布说明；预览特性只在非关键代码里试用；Valhalla 稳定之前不要为它重写数据结构；今天就能受益的是虚拟线程、记录、模式匹配、新的 GC 与启动优化。
