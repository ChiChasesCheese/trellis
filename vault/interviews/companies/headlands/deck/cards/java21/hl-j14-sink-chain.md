---
id: hl-j14-sink-chain
node: java21.j14-stream-api
type: qa
step: 15
---
## Q
Stream 流水线在 `java.util.stream` 内部是怎么执行的？`findFirst` 如何短路？`sorted` 和 `distinct` 为什么是屏障？

## A
流水线是一串 `Sink` 对象，每个中间操作包一层。终止操作开始后，库从来源**一个一个**取元素，调 `sink.accept(x)` 往下推。

例：`filter(偶数) → map(×10) → findFirst`，来源 1..6：元素 1 在 `filter` 被拒，不走 `map`；元素 2 通过并被 `findFirst` 拿到结果 20，然后通知上游「别再给了」（**短路**），元素 3–6 根本没被读。

`sorted()`、`distinct()` 是**有状态的屏障**：必须看完全部输入才能往下推，如先出现全部 `before sort 3,1,2`，才有 `after sort 1,2,3`。
