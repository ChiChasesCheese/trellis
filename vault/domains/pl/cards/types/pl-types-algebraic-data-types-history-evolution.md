---
id: pl-types-algebraic-data-types-history-evolution
node: types.algebraic-data-types
type: qa
step: 11
---
## Q
和类型是怎样从函数式语言进入主流语言的？为什么 2020 年代的语言几乎都在补这个特性？

## A
源头在 1970 年代的 ML 语言：它把「几种形态之一的数据类型」和「按形态分支的模式匹配」作为核心，后来 Haskell、OCaml 沿用。很长时间里，这对搭档被看作函数式语言的专利，主流的面向对象语言用类继承加访问者模式（visitor）模拟，代码冗长。

进入主流的路径：

- Scala（2004）的 `case class` 和 `sealed`，让 JVM 上有了和类型。
- Rust（2015）把 `enum` 加 `match` 作为系统语言的一等特性，`Option`、`Result` 全部建立在它上面。
- C++17（2017）用标准库补上 `std::variant`（带标签联合体），没有新语法，也没有 `match`；到 C++23 为止标准里仍没有模式匹配，只能靠 `std::visit`（按 `variant` 当前变体分派的函数）。
- Swift（2014）和 Kotlin（`sealed class`，2016）把它带给移动开发。
- TypeScript 的可辨识联合（discriminated union）。
- Java 在 16 到 21 之间补齐三件事：`record`（积类型）、`sealed`（封闭变体集）、`switch` 的模式匹配（穷尽分支）。
- Python 3.10（2021）加入 `match` 语句，配合 `dataclass` 和联合类型。
- Go 目前不支持，社区曾多次提出和类型的提案，但与它的接口设计和简单性目标存在冲突。

趋势的原因是：软件越来越多地是在处理「几种消息、几种状态之一」（协议、状态机、事件流、错误结果）。用类型表达这些，编译器能替你检查完整性；用继承加访问者，代码量大数倍。收益明显，各语言便依次补上。
