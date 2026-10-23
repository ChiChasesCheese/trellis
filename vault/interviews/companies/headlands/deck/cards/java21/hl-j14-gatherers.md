---
id: hl-j14-gatherers
node: java21.j14-stream-api
type: qa
step: 20
---
## Q
Stream Gatherers 是什么？Java 21 里有吗？面试被问到怎么答？

## A
流水线的中间操作（`filter`、`map`、`sorted`……）是固定的一组。**Stream Gatherers**（JDK 22 预览，**JDK 24 转正**）让你自定义中间操作：`Stream::gather(Gatherer)`，内置 `fold`、`mapConcurrent`、`scan`、`windowFixed`、`windowSliding`。

「滑动窗口平均」在 JDK 21 要写自己的 `Spliterator` 或绕路，24 起一行 `stream.gather(Gatherers.windowSliding(3))`。

面试说法：「21 里没有；24 起有 Gatherers，我知道有这件事。」
