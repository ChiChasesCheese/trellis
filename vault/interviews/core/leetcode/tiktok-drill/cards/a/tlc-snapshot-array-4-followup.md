---
id: tlc-snapshot-array-4-followup
node: a.snapshot-array
type: qa
step: 4
---
## Q
**LC 1146 快照数组**｜追问

面试官接着问：（1）加 `rollback(snap_id)` 回到某个快照？（2）下标范围是 `10^9` 的稀疏数组？（3）同样的技术怎么做「时间版 KV 存储」（LC 981）？

## A
1. **回滚**：把每个下标的历史里快照号 `> snap_id` 的记录截掉，并把当前 `snap_id` 设成目标值加一。为避免遍历所有下标，用一个集合记录「自某次快照以来被写过的下标」，只处理这些下标；也可以把历史改成按快照号栈式管理，回滚就是弹栈。
2. **稀疏数组**：`history` 用 `dict[int, list[tuple[int, int]]]`（`defaultdict(list)` 亦可），只为被写过的下标建记录；`get` 时下标不在字典里直接返回 `0`；有记录时二分，且第一条记录的快照号可能 `> snap_id`，此时也返回 `0`，不要再依赖 `(0, 0)` 哨兵。
3. **LC 981**：键是字符串，快照号换成时间戳，`set(key, value, timestamp)` 追加，`get(key, timestamp)` 用 `bisect_right` 找最后一个时间戳 `<= timestamp` 的值；题目保证时间戳递增，所以也不必排序，结构与此处完全一样。

**Python 提醒**：`bisect` 的 `key` 参数（3.10+）只用于被搜索的元素，传入的查找值要写成**已经映射过的值**（这里是 `snap_id`，不是元组）；这和 `sorted(key=...)` 不同，容易写错成 `bisect_right(hist, (snap_id, 0), key=...)`。
