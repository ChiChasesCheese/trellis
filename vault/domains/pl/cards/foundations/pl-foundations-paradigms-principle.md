---
id: pl-foundations-paradigms-principle
node: foundations.paradigms
type: qa
step: 1
---
## Q
编程范式（programming paradigm）是什么？命令式、面向对象、函数式、声明式这四种范式各把程序看成什么？

## A
范式是组织程序的思维方式，回答两个问题：程序由什么构成，状态怎样变化。它要解决的问题是：程序一大，「一条接一条执行的语句」就会失控，需要一个组织原则来限制谁能改什么、先做什么。

常见的四种回答：

- 命令式（imperative）：程序是一串改变内存状态的指令，关心「怎么做」。赋值、循环、分支是基本零件。
- 面向对象（object-oriented）：把数据和操作它的函数捆成对象，状态藏在对象里，只通过方法访问。
- 函数式（functional）：程序是表达式求值，函数本身是值，尽量不修改已有数据，而是产生新值。
- 声明式（declarative）：只描述想要的结果，由引擎决定怎么算。SQL 和正则表达式是典型。

四者不互斥。Go、Java、Rust、Python 都是多范式（multi-paradigm）语言，内核都是命令式，区别只在默认鼓励哪一种：Java 默认推你写类，Rust 和 Python 容易写出函数式风格，Go 刻意保持朴素的过程式加方法。
