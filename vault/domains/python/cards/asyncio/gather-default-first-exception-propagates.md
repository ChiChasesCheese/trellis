---
id: gather-default-first-exception-propagates
node: asyncio.gather-wait-timeout
type: qa
source: python-docs
---
## Q
`await asyncio.gather(coro_a(), coro_b(), coro_c())` 中如果 `coro_b()` 先抛出异常，默认情况下会发生什么？`coro_a()`、`coro_c()` 会不会被取消？

## A
默认（`return_exceptions=False`）下，第一个抛出的异常会立即向等待 `gather()` 的调用方传播；但 `aws` 序列里其它还在运行的可等待对象（如 `coro_a()`、`coro_c()`）**不会**被自动取消，仍会继续跑下去——这是 `gather` 和更安全的 `TaskGroup` 的关键差异之一。
