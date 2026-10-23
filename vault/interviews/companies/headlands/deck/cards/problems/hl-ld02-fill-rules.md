---
id: hl-ld02-fill-rules
node: problems.ld02-trading-ood
type: qa
step: 4
---
## Q
`Fill` 的处理规则和检查顺序是什么？为什么去重在状态检查之前，超量成交的 `execId` 为什么不能记为已见？

## A
回报是 **at-least-once** 投递：同一笔成交可能到两次。每笔成交有全局唯一 `execId`，记在 `Set`，见过的直接返回 `false`。

`Fill` 检查顺序（全部通过后才修改）：
1. **去重**（`execId` 已见过 ⟹ 返回 `false`，无任何效果——即使订单已 `FILLED`）；
2. 状态是否允许（`WORKING` 或 `PARTIALLY_FILLED`）；
3. `qty > leaves` ⟹ `IllegalTransitionException`（超量成交）；
4. 成交价不得越过限价：买单 `px > 限价` 非法，卖单 `px < 限价` 非法；等于限价、价格改善合法；
5. 计算新累计成交额 `Math.addExact(cumNotional, Math.multiplyExact(qty, px))`，溢出抛 `ArithmeticException` 且订单状态不变；
6. **全部通过之后**才记 `execId`、改 `cumQty`、改聚合量、改状态：`cumQty == order.qty` ⟹ `FILLED`（`openCount--`），否则 `PARTIALLY_FILLED`。

```java
case ExecEvent.Fill f -> {
    if (seenExecIds.contains(f.execId())) yield false;
    require(s.status == WORKING || s.status == PARTIALLY_FILLED, s, "Fill");
    if (f.qty() > s.leaves()) throw new IllegalTransitionException("overfill on order " + s.order.id());
    boolean outside = s.order.side() == Side.BUY ? f.px() > s.order.px() : f.px() < s.order.px();
    if (outside) throw new IllegalTransitionException(...);
    long newCumNotional = Math.addExact(s.cumNotional, Math.multiplyExact(f.qty(), f.px()));
    seenExecIds.add(f.execId());
    s.cumQty += f.qty(); s.cumNotional = newCumNotional;
    reduceOpen(s, f.qty());
    ...
    yield true;
}
```
**为什么去重在状态检查之前**：订单已 `FILLED` 后旧回报过来，先检查状态会被当「终态后又来 Fill」的非法转移抛异常，但它只是重复消息，应安静忽略；更糟的实现把它当新成交，仓位翻倍。

**为什么超量被拒的 `execId` 不能记为已见**：否则之后用合法数量重发会被当重复吞掉。

「边验证边修改」是常见错误：超量成交先加 `cumQty` 再报错，抛异常时状态已破坏。前五步只读不写，任何一步失败状态都没动——这是之后 `replay` 成立的前提。

`Cancel`：`reduceOpen(s, s.leaves())`，`CANCELED`，`openCount--`；`Reject`：只在 `PENDING`，存 `rejectReason`；未知订单抛 `NoSuchElementException`，在任何修改之前。
