---
id: hl-j06-equals-oneliner
node: java21.j06-instanceof-pattern
type: qa
step: 14
---
## Q
补全代码：用 `instanceof` 模式写 `Instrument.equals(Object o)`，比较 `ticker` 和 `exchange`。为什么不需要单独的 `o == null` 检查？

## A
```java
@Override public boolean equals(Object o) {
    return o instanceof Instrument other
            && ticker.equals(other.ticker)
            && exchange.equals(other.exchange);
}
```
`instanceof` 同时完成"判空、判类型、转型、命名"；`null instanceof Instrument` 为 `false`，所以对 `null` 安全，不需要单独的 `o == null` 检查。
