---
id: hl-heap-qa-update-priority
node: foundations.heap-priority-queue
type: qa
step: 34
---
## Q
追问：我要支持「修改某个任务的优先级」，怎么做？

## A
推荐答法：「`PriorityQueue` 不支持 decrease-key。修改很少就 `remove` 再 `add`（O(n)）；通用做法是**懒删除**：保留旧条目，插入新版本，`poll` 出来时核对版本号丢弃过期的；必须严格 O(log n) 且旧条目不能留，就实现带位置表的**索引堆**。」
