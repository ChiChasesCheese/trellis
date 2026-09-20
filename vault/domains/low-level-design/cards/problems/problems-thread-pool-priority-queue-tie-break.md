---
id: problems-thread-pool-priority-queue-tie-break
node: problems.components.thread-pool
type: qa
step: 6
tags: [grown]
---
## Q
线程池要支持按优先级出队。把排队中的每一条记录做成 `@dataclass(order=True)` 塞进 `queue.PriorityQueue`，要注意什么才能避免运行时抛 `TypeError`？

## A
必须显式把任务体、参数、`Future` 这些字段标成 `field(compare=False)`，只让『优先级 + 一个单调递增的序号』这两个字段参与排序。原因是 `PriorityQueue` 内部靠元素之间的 `<` 比较决定谁先出队，`dataclass(order=True)` 默认会按字段声明顺序依次比较**全部**字段；如果两个任务的优先级和序号都相同（正常情况下序号单调递增、天然唯一，但一旦比较逻辑因为某次改动退化到需要比较后面的字段），Python 就会尝试比较两个函数对象或两个 `Future`，两者都没有定义 `<`，直接抛 `TypeError: '<' not supported`。这是 `heapq`／`PriorityQueue` 包着非纯数据对象时最常见的坑：排序键必须只覆盖那些真正可比较、真正决定顺序的字段，其余一律显式排除在比较之外，而不是依赖『反正不会发生』的假设。
