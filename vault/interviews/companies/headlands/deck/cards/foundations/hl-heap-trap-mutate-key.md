---
id: hl-heap-trap-mutate-key
node: foundations.heap-priority-queue
type: qa
step: 26
---
## Q
入队后修改元素里决定顺序的字段会怎样？`PriorityQueue` 怎么更新优先级？

## A
`PriorityQueue` 没有 decrease-key 方法，堆内部数组不会重排。实测 5, 6, 7, 8 入堆后把 8 改成 1，`peek()` 仍返回 5（应该是 1）。

三种修法：
1. **先 remove 再 add**：`pq.remove(x); x.key = newKey; pq.add(x);`，`remove(Object)` 是 O(n)；
2. **懒删除（lazy deletion）**：不删旧条目，插入带新优先级的新条目；`poll` 出来时检查是否过期（和 map 里最新版本对不上），过期就丢弃再 `poll`。Dijkstra、事件调度的标准技巧，每个操作保持 O(log n)；
3. **索引堆**（indexed priority queue）：自己实现，额外维护 `位置[id]`，支持 O(log n) 的 decrease-key。

最好的预防：让元素不可变（`record`）。
