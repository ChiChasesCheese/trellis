---
id: hl-j04-no-constants
node: java21.j04-record-patterns
type: qa
step: 12
---
## Q
`case Order(var id, Side.BUY, var px, var q) ->` 为什么编译不过？要匹配具体的 `Side.BUY` 怎么写？

## A
Java 21 的子模式只能是**模式**（类型模式、`var`、嵌套 record 模式），**不能是常量**（`enum` 常量、字符串、数字字面量都不行），报 `<identifier> expected`。

正确写法：先绑定再用 `when`：
```java
case Order(var id, Side side, var px, var q) when side == Side.BUY -> ...
```
注意：`case Level.LOW` 是**顶层**标签接受限定名 `enum` 常量，不是 record 模式的子模式，两回事。
