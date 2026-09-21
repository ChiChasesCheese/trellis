---
id: event-loop-debug-mode-100ms-threshold
node: asyncio.event-loop
type: qa
source: python-docs
---
## Q
`asyncio.run(main(), debug=True)` 开启调试模式后，事件循环会对哪种协程发出告警，触发阈值是多少？

## A
调试模式（debug mode）会记录并告警那些连续占用执行权（不让出控制权给事件循环）达到 100ms 或更久的协程，帮助定位没有正确 `await` 从而拖慢/卡住整个循环的代码。
