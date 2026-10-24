---
id: pl-foundations-lineage-principle
node: foundations.lineage
type: qa
step: 1
---
## Q
什么是编程语言的谱系（lineage）？为什么看谱系就能理解一个语言特性「为什么长这样」？

## A
谱系是一门语言的思想来源图：它从哪些前辈那里继承了什么、借用了什么、反对了什么。新语言几乎从不凭空设计，因为设计者本人是用旧语言长大的，旧语言的优点会被保留，痛点会被针对。

特性沿三条路径传播：

1. 继承（inherit）：直接沿用语法和语义。Java 的花括号、`for` 循环、`int` 类型来自 C 和 C++（C++ 本身就是把 C 整个继承下来，再叠加 Simula 的类）。
2. 借用（borrow）：把另一个家族里被证明有效的思想搬过来。Rust 的 `enum` 加 `match` 来自 ML 家族，`trait` 来自 Haskell 的类型类（type class）。
3. 反动（react）：针对前辈的痛点做相反的选择。Go 针对 C++ 的复杂和慢编译做减法；Java 针对 C++ 的内存错误引入垃圾回收；Rust 针对 C++ 的不安全引入借用检查。

意义：看到一个陌生特性，问「它的祖先是谁」，等于把五门语言的几十个特性归并到寥寥几个思想上。学过一次代数数据类型（algebraic data type），遇到 Rust `enum`、Java `sealed` 就是同一件事的不同写法；学过一次 CSP 的通道（channel），遇到 Go 的 `chan` 就不陌生。
