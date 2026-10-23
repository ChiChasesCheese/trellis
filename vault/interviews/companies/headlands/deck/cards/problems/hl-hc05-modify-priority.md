---
id: hl-hc05-modify-priority
node: problems.hc05-market-order-book
type: qa
step: 7
---
## Q
订单簿的 `modify` 为什么「减量保持优先级、增量丢失优先级」？怎么实现，要注意什么顺序？

## A
- **减量**：不动位置——让别人没有额外损失的修改不丢优先级。
- **增量**：移到该价位的队尾——否则可以先挂 1 个占队头，再改成 1000 个，白占便宜。
- 等量什么都不变。

实现：增量时 `fifo.putLast(id, node)`（对已有 key，`LinkedHashMap` 把它移到末尾）；C++ 用 `list::splice` 移到队尾，比「删除再插入」好：O(1)、不分配、迭代器和 `Locator` 保持不变。

顺序（异常安全）：
```java
long newTotal = Math.addExact(level.total, newQty - n.qty);   // 先算，可能抛
n.qty = newQty; level.total = newTotal;                       // 再改
if (newQty > oldQty) level.fifo.putLast(id, n);               // 增量移队尾
```
所有会抛异常的检查（`addExact`）放在任何修改之前，抛出时簿还没变。反例：先 `put` 再加总量，抛异常时队列已多一个订单而 `total` 没更新，簿就坏了。

`newQty <= 0` 检查在「找 id」之前，所以 `modify(未知 id, 0)` 先报参数错。内部 `Node` 可变（`qty` 被成交减少），对外的 `Order` 是不可变 record（`find` 返回新快照）。

`total` 缓存的代价：**每一处**修改都必须同步更新，否则与真实队列不一致（不变量）。
