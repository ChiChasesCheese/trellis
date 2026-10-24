---
id: pl-foundations-lineage-mechanism
node: foundations.lineage
type: qa
step: 2
---
## Q
一个特性是怎样跨越几十年从研究语言进入 Go、Java、Rust 的？以「代数数据类型加模式匹配」和「通道」为例写出传播路径。

## A
特性的典型传播路径：学术或小众语言先验证想法，十几年后被主流语言吸收，再过十年进入更多语言。

代数数据类型（algebraic data type）加模式匹配（pattern matching）：

1. 1970 年代：ML 语言引入「几种形态之一」的数据类型和按形态分支的 `match`。
2. 1990 年：Haskell 继承并加入类型类。
3. 2015 年：Rust 1.0 把它们变成 `enum` 与 `match`，`Option` 和 `Result` 靠它实现。
4. 2021 到 2023 年：Java 16 的 `record`、Java 17 的 `sealed` 类，以及 Java 21 的 switch 模式匹配和 record 模式，把同一思想补进 Java。

通道（channel）：

1. 1978 年：Tony Hoare 发表 CSP（通信顺序进程），主张进程之间通过消息通信而不是共享内存。
2. 1980 年代到 90 年代：Rob Pike 在 Newsqueak、Limbo 等语言里把通道做成语法。
3. 2009 年：Go 公开，用 `go` 关键字启动 goroutine，用 `ch <- v` 和 `<-ch` 收发。

规律：从提出到进入主流，往往要 20 到 40 年。所以今天主流语言在追的特性（比如不可变数据、值类型、效应系统），多半能在研究语言里找到源头。
