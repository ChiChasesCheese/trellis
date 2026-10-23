---
id: hl-hc08-put-delete-code
node: problems.hc08-order-sequence-api
type: qa
step: 7
---
## Q
`put` 和 `delete` 的检查顺序为什么重要？写出核心代码并说出它保证了什么。

## A
```java
public void put(long id, long qty) {
    if (qty <= 0) throw new IllegalArgumentException(INVALID_QTY);
    if (indexOf.containsKey(id)) throw new IllegalArgumentException(DUPLICATE_ID);
    long newTotal = Math.addExact(totalQty, qty);   // 溢出 → ArithmeticException，此时还没改任何东西
    if (nextIndex > capacity) compact();             // 下标空间写满：先压缩
    int i = nextIndex++;
    idByIdx[i] = id; qtyByIdx[i] = qty;
    addCnt(i, 1); addSum(i, qty); indexOf.put(id, i);
    totalQty = newTotal;
}
public long delete(long id, long qty) {
    Integer i = indexOf.get(id);
    if (i == null) throw new NoSuchElementException("unknown id");
    if (qty <= 0) throw new IllegalArgumentException(INVALID_QTY);
    long have = qtyByIdx[i];
    if (qty > have) throw new IllegalArgumentException("quantity exceeds remaining");
    long left = have - qty;
    qtyByIdx[i] = left; addSum(i, -qty); totalQty -= qty;
    if (left == 0) { addCnt(i, -1); indexOf.remove(id); }
    return left;
}
```
- **所有可能抛异常的检查都在任何修改之前**，失败时对象保持原样（状态不变）。
- 只要**全局总和** `totalQty` 不溢出，任何前缀和都不会溢出，所以只检查它一个数。
- 压缩放在领下标之前，且在溢出检查之后（失败的 `put` 不应触发压缩）；压缩完成后 `nextIndex = m + 1`，保证有空位。
- `delete` 下标从不改变；返回剩余量。

常见 bug：`indexOf.get(id)` 对未知 id 返回 null，拆箱 NPE（应抛 `NoSuchElementException`）；没检查 `qty ≤ 0`（负数会加量）；没检查 `qty >` 剩余（数量变负，洞与活跃订单混淆）；没更新 `totalQty`；查询已删除的 id 返回 0 而不是抛异常（0 让调用方分不清「没有订单」和「前面没有订单」）；先改树后检查溢出。
