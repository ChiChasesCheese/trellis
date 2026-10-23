---
id: hl-j15-exception-safe
node: java21.j15-math-string-utils
type: qa
step: 21
---
## Q
订单簿为什么要「先 `addExact` 算出 `newTotal`，再修改状态」，而不是边改边算？

## A
这是**异常安全（强保证）**：

```java
// 先算后改：addExact 抛异常时下面还没有任何修改，簿保持原样
long newTotal = Math.addExact(level == null ? 0L : level.total, qty);
```
`addExact` 抛异常时状态还没改，订单簿保持原样；若边改边算，抛异常时可能已改了一半（如已扣队列但价位总量没更新），簿内部不一致。

同理，价格×数量累加成交额用 `Math.addExact(notional, Math.multiplyExact(price, qty))`；多个 ticker map 的累加器 `values[i] = Math.addExact(values[i], delta)`，溢出要报错。
