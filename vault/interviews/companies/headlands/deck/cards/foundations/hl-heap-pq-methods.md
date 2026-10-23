---
id: hl-heap-pq-methods
node: foundations.heap-priority-queue
type: qa
step: 22
---
## Q
`PriorityQueue` 的 `offer`、`add`、`peek`、`element`、`poll`、`remove()`、`remove(Object)`、`contains` 各自复杂度是多少，空队列时行为是什么？

## A
- `offer(e)` / `add(e)`：O(log n)，无界不会满，二者没区别；
- `peek()`：O(1)，空队列返回 `null`；`element()`：O(1)，空则抛 `NoSuchElementException`；
- `poll()`：O(log n)，空返回 `null`；`remove()`：O(log n)，空抛 `NoSuchElementException`；
- `remove(Object o)`：**O(n)**，删除 `equals` 相等的第一个，没有返回 false；
- `contains(Object o)`：**O(n)**；`size()` / `isEmpty()`：O(1)；`clear()`：O(n)。

`null` 元素不允许（`NullPointerException`），因为 `poll` 用 `null` 表示「空」。元素必须可比较（`Comparable` 或 `Comparator`），否则 `ClassCastException`。
