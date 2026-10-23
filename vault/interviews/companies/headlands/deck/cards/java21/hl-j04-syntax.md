---
id: hl-j04-syntax
node: java21.j04-record-patterns
type: qa
step: 3
---
## Q
record 模式（record pattern）的写法是什么？它能用在哪两处？写出 `Point(long x, long y)` 的两个例子。

## A
record 模式 = **record 类型名 + 括号 + 与组件一一对应的子模式**。读法：若 `o` 是 `Point`，把第一个组件绑定到 `x`，第二个绑定到 `y`；`x`、`y` 是新局部变量，仅在匹配成功的范围内可用。

两处可用：
```java
if (o instanceof Point(var x, var y) && x < y) { ... }       // instanceof，可接 &&
case Point(var x, var y) when x == 0 && y == 0 -> "origin"   // switch 的 case
```
