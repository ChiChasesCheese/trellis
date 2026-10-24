---
id: pl-memory-value-reference-semantics-history
node: memory.value-reference-semantics
type: qa
step: 11
---
## Q
值语义与引用语义的取舍，在近二十年的语言演进里朝哪个方向移动？

## A
早期的主流是「对象全是引用」：Smalltalk、Java、Python 的统一对象模型简单，但别名和堆分配的代价随着多核和大数据变得突出。演进有三条线：

1. **回到值**：C#（`struct`）、Go（结构体按值）、Swift（值类型是一等公民，数组和字典是写时复制的值类型）、Rust（默认移动）。趋势是让数据结构默认是值，需要共享才显式引用。
2. **让引用变成不可变**：Java 的 `record`（Java 16 正式）、Python 的 `frozen` dataclass、函数式语言的持久数据结构。共享仍在，但「修改」消失了，别名不再危险。
3. **让编译器管别名**：Rust 的借用规则；Swift 的独占访问规则（exclusivity enforcement）；C++ 社区的相关提案。

Java 的 Valhalla 项目则从另一侧逼近：想让某些类没有对象身份，像值一样内联存储。

综合来看，演进的方向是同一个：**别名加可变是 bug 的主要来源**，所以新语言要么消除别名，要么消除可变性，要么让编译器证明二者不冲突。
