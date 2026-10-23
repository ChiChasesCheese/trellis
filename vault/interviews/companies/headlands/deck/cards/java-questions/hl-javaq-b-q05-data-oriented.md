---
id: hl-javaq-b-q05-data-oriented
node: java-questions.b-versions
type: qa
step: 3
---
## Q
Java 17/21 的"数据导向编程"（data-oriented programming）主线是什么？相比 Java 8 的 visitor / `instanceof` 链好在哪里？

## A
主线是一条链：**`record`（数据）→ `sealed`（封闭的种类集合）→ `switch` 模式匹配（按种类分派，编译器检查穷尽）→ record 模式（直接拆开字段）**。

对比 Java 8 的 visitor 或 `instanceof` 链：新增一种事件时，老写法编译器不会提醒你漏改；**sealed + switch 会编译失败**，逼你补上处理分支。也不需要 visitor 的 `accept` 样板代码。

同一个文件里可以同时用：`List.of`（9）、`stream().toList()`（16）、文本块（15）、`instanceof` 模式（16）、带 `when` 守卫的 sealed `switch`（17/21）、`reversed()/getFirst()`（21）、`Collectors.teeing`（12）、虚拟线程执行器（21）。
