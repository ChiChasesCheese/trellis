---
id: paginated-fetch-semaphore-plus-retry-pattern
node: asyncio.streams-protocols
type: qa
source: python-docs
---
## Q
用 asyncio 并发拉取一个分页（paginated）API 的所有页面时，常见的组合模式是怎样把「限流」和「重试」结合起来的？

## A
典型写法是：用 `asyncio.Semaphore(N)` 限制同时在途的请求数（防止把对方服务器打垮或触发限流），每个页面的抓取协程内部再包一层重试逻辑（捕获网络异常后按次数或退避策略重试），最后用 `asyncio.gather()` 或 `TaskGroup` 并发收集所有页面协程的结果——限流管住并发度，重试管住单个请求的可靠性，两者是互相独立、可以叠加的两层控制。
