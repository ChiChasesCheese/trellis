---
id: hl-j04-exhaustive-product
node: java21.j04-record-patterns
type: qa
step: 11
---
## Q
record 的多个组件都是 `sealed` 类型时，`switch` 的穷尽性怎么算？用 `Pair(Bit a, Bit b)`（`Bit` 有 `Zero`、`One`）说明。

## A
所有**组合**都要覆盖，数量**相乘**：2 × 2 = 4 种。

```java
return switch (p) {
    case Pair(Zero a, Zero b) -> "0";
    case Pair(Zero a, One b)  -> "1";
    case Pair(One a, Zero b)  -> "1";
    case Pair(One a, One b)   -> "0";    // 缺一个就编译错误
};
```
去掉最后一行报 `does not cover all possible input values`。"买卖方向 × 订单类型"这类场景，漏组合就是编译错误。用无条件子模式 `Pair(Bit a, Bit b)` 可以一次覆盖。
