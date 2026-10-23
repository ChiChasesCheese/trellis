---
id: hl-hc08-what-asked
node: problems.hc08-order-sequence-api
type: qa
step: 1
---
## Q
订单序列 API（Order Sequence API）要实现哪几个操作？语义规则和三个 Part 是什么？

## A
一排按到达顺序排队的订单，每张有 `unique_id`（任意 `long`，同时只能有一张同 id 的活跃订单）和正整数 `quantity`，新订单排队尾。
- `put(id, qty)`：放到末尾。`qty ≤ 0` → `IllegalArgumentException("invalid quantity")`；id 已活跃 → `IAE("duplicate id")`；全体活跃订单数量之和会超过 `Long.MAX_VALUE` → `ArithmeticException("overflow")`，**状态不变**。
- `delete(id, qty)`：删掉 `qty` 个单位，返回**剩余数量**；剩余为 0 时订单从序列移除；**位置不变**。`qty ≤ 0` → IAE；未知 id → `NoSuchElementException("unknown id")`；`qty >` 剩余 → `IAE("quantity exceeds remaining")`，状态不变。
- `countUpTo(id)`：队头到该订单（含）的活跃订单数；`qtyUpTo(id)`：同范围剩余数量之和；未知 id → `NoSuchElementException`。
- `idAt(k)`：第 k 张（1 起）活跃订单的 id；越界 → `IndexOutOfBoundsException("index out of range")`。
- `size()`、`totalQty()`、`entries()`。同一 id 删光后可再 `put`，它排到**最后**。

Part 1：语义做对，允许朴素 `ArrayList` 线性扫描，另有文本接口 `PUT/DELETE/COUNT/QTY/AT`；Part 2：**亚线性**查询（O(log n)），50 万张订单 + 50 万次操作 < 2 s；Part 3：部分删除 + 压缩（下标空间写满时重新编号；200 万次 put/delete 循环、活跃 ≤ 1000，容量必须 ≤ 4096）。

手算：`put(10,5) put(20,3) put(30,7)`：`countUpTo(30)=3`，`qtyUpTo(20)=8`；`delete(20,3)` 后 `qtyUpTo(30)=12`，`idAt(2)=30`。

考点：看到「前缀和 + 在线修改」想到树状数组；Part 3 是工程问题：**内存应该跟活跃量走，而不是跟历史总量走**。
