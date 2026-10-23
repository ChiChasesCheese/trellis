---
id: hl-j07-concat-vs-formatted
node: java21.j07-text-blocks
type: qa
step: 12
---
## Q
字符串拼接什么时候被折叠成一条 `ldc`，什么时候变成运行时拼接？文本块里要嵌入变量，开销如何？

## A
- 全是字面量的 `"a" + "b" + "c"` 会被**常量折叠**成一条 `ldc`；
- 一旦掺入变量就变运行时拼接：`StringBuilder`，Java 9 起是 `invokedynamic makeConcatWithConstants`。

文本块里**不能**直接嵌变量，用 `.formatted()` 是**运行时**调用（一次 `String.format`），开销与手写 `String.format` 相同。
