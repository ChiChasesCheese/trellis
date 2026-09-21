---
id: debug-mode-slow-callback-100ms
node: asyncio.debugging
type: qa
source: cpython-internals
---
## Q
调试模式下，一个回调（callback）执行超过多久会被记录为「慢回调」？这个阈值能改吗？

## A
默认阈值是 100 毫秒：调试模式下执行时间超过 100ms 的回调会被日志记录下来，帮助定位拖慢事件循环的代码。这个阈值可以通过 `loop.slow_callback_duration` 属性调整为其它秒数。
