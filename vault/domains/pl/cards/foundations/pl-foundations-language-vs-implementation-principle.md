---
id: pl-foundations-language-vs-implementation-principle
node: foundations.language-vs-implementation
type: qa
step: 1
---
## Q
「编程语言」和「语言实现」（language implementation）是两个东西吗？为什么要区分？

## A
语言是一份规定：哪些程序合法（语法），合法程序的含义是什么（语义）。实现是一个真正的软件：编译器、解释器或虚拟机，负责让程序跑起来。语言像「合同」，实现像「履行合同的人」。

为什么要区分：同一份规定可以有速度、体积、平台都不同的多个实现。你写的代码如果只依赖规定，换实现就能照常工作；如果依赖了某个实现的行为，换实现就会坏。

定义语言的三种常见方式：

1. 书面规范加多个实现。Java 有语言规范（JLS）和虚拟机规范（JVMS），Go 有语言规范，C/C++ 有 ISO 标准。
2. 参考实现即规范。CPython 长期是 Python 的事实标准，`rustc` 是 Rust 的事实标准，实现的行为就是答案。
3. 一致性测试套件。Java 的 TCK（Technology Compatibility Kit）规定：通过全部测试，才能叫兼容的 Java 实现。

常见误解：「Python 慢」「Java 要装 JVM」描述的多是实现，不是语言。换成 PyPy，同样的 Python 代码常常快几倍；换成 GraalVM 原生镜像，Java 程序可以不带 JVM 启动。
