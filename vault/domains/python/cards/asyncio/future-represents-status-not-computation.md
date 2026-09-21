---
id: future-represents-status-not-computation
node: asyncio.futures
type: qa
source: python-docs
---
## Q
`asyncio.Future` 和协程（coroutine）都可以被 `await`，它们本质上代表的东西一样吗？

## A
不一样。协程代表一段「还没跑的计算逻辑」本身；Future 不是计算逻辑，而是一个计算结果的占位符/状态灯，只有「pending（进行中）」、「cancelled（已取消）」、「done（已完成）」三种状态。Future 可以被多次 `await`，每次都拿到同一个结果，因为它只是在等一个别处已经产生（或将产生）的值。
