---
id: hl-j04-trade-format
node: java21.j04-record-patterns
type: qa
step: 19
---
## Q
订单事件格式化里，`case Trade(var taker, var maker, Side side, var px, var qty) when side == Side.BUY` 把 `side` 写成显式类型，和写 `var side` 有区别吗？怎么匹配具体的买方向？

## A
**两者等价**：`Side side` 是显式类型，`var side` 由编译器推导为组件的声明类型 `Side`。

要匹配具体的 `Side.BUY`，不能写常量子模式，用 `when side == Side.BUY`：

```java
case Trade(var taker, var maker, Side side, var px, var qty) when side == Side.BUY ->
        "BOUGHT %d@%d (taker %d <- maker %d)".formatted(qty, px, taker, maker);
case Trade(var taker, var maker, var side, var px, var qty) -> "SOLD ...";
```
