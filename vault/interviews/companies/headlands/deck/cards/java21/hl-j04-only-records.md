---
id: hl-j04-only-records
node: java21.j04-record-patterns
type: qa
step: 21
---
## Q
Java 21 的 record 模式能不能用来解构普通类？不是 record 的类怎么办？

## A
**不能**：record 模式只能用在 **record 类型**上，Java 21 对普通类没有解构方式。

办法：
- 把它改成 `record`；
- 或用类型模式 + 手动调 getter。
