---
id: hl-hc08-hidden-pitfalls
node: problems.hc08-order-sequence-api
type: qa
step: 11
---
## Q
订单序列题的隐藏测试和常见误区有哪些？

## A
1. Fenwick 下标从 0 开始（`i & -i` 在 0 上死循环）；
2. 删除后把后面的订单往前挪，下标全乱，`indexOf` 失效（正确：留洞）；
3. `cnt` 和 `sum` 共用一棵树，或部分删除时也 `addCnt(i, -1)`；
4. 压缩后忘了更新 `indexOf`；压缩容量取 `m+1`，导致每次 put 都压缩；压缩后 `next_index_` 没更新，新订单写进旧位置；
5. 先改树后检查总量溢出，抛异常时状态已被改；
6. 查询已删除的 id 返回 0 而不是抛 `NoSuchElementException`；
7. 容量不是 2 的幂时直接套二分下降；
8. id 取 0 / 负数 / `Long.MIN_VALUE`（不能用 0 当「空」标记）；
9. 重复 id 当作更新（同一 id 同时只能有一张活跃订单；删光后可再 put，排到最后）。

**边界清单**：空序列上的所有查询；重复 id；`qty ≤ 0`；删除超过剩余；已删除的 id 再查询；总量到 `Long.MAX_VALUE`；Fenwick 的边界（大小不是 2 的幂、只剩头 / 只剩尾）；洞全堆在序列前面（永远删最老的）；容量 1 / 4 这种极小空间下的压缩。

**变体**：4 个 API 是 `put / delete / count(id) / quantity(id)` 没有 `idAt`；前缀改成后缀 / 价格区间。「memory management」可指删除后内存回收（Part 3），也可指订单对象池（订单簿 Part 4 的思路）。
