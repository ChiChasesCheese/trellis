---
id: hl-heap-trap-iteration
node: foundations.heap-priority-queue
type: qa
step: 24
---
## Q
打印或遍历 `PriorityQueue` 得到的是排序顺序吗？怎么得到有序输出？

## A
不是。`toString`、`iterator`、`toArray` 走的是**内部数组下标顺序**。例：由 `[9,4,7,1,8,2,6]` 建的队列，`toString` 是 `[1, 4, 2, 9, 8, 7, 6]`，而反复 `poll` 才是 `1 2 4 6 7 8 9`。Javadoc 明确不保证迭代按任何特定顺序。

正确做法：要有序输出就反复 `poll`，代价 O(n log n)；或拷贝再排序：
```java
var sorted = new ArrayList<>(pq);
Collections.sort(sorted);
```
原因：堆只保证父不大于子，兄弟之间无序。
