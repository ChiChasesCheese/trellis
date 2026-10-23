---
id: hl-omap-design-timer
node: foundations.ordered-maps-trees
type: qa
step: 42
---
## Q
设计一个本地定时器：加入（到期时间, 任务）、取消某任务、取出所有已到期任务。选 `PriorityQueue` 还是 `TreeMap`？

## A
关键是**取消**：`PriorityQueue.remove(Object)` 是 O(n)。

- 用 `TreeMap<Long, List<Task>>` 或 `TreeSet<(到期时间, 序号)>` 加 `HashMap<taskId, key>`，取消 O(log n)；取到期任务用 `headMap(now, true)`；
- 取消很少时，`PriorityQueue` + **懒删除**（标记取消，`poll` 到时丢弃）更快。
