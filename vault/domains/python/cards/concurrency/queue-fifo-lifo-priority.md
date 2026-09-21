---
id: queue-fifo-lifo-priority
node: concurrency.queues
type: qa
source: python-docs
---
## Q
`queue` 模块里 `Queue`、`LifoQueue`、`PriorityQueue` 的取出顺序分别是什么？

## A
`Queue` 是 FIFO（先进先出）：最先放入的最先取出。`LifoQueue` 是 LIFO（后进先出），行为像一个栈。`PriorityQueue` 内部用 `heapq` 维护有序，每次取出的是当前最小值的条目，典型写法是放入 `(priority_number, data)` 元组；如果 `data` 之间不可比较，需要用一个只比较优先级字段的包装类（如 `@dataclass(order=True)` 且 `data` 字段 `compare=False`）避免比较报错。三者都通过 `maxsize` 限制容量，达到上限后 `put()` 阻塞直到有空位。
