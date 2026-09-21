---
id: mp-pool-map-vs-apply-async
node: concurrency.multiprocessing
type: qa
source: python-docs
---
## Q
`Pool.map(f, iterable)` 和 `Pool.apply_async(f, args)` 在阻塞行为和返回结果上有什么区别？

## A
`pool.map()` 会阻塞调用者，直到所有任务都完成，返回结果按输入顺序排列的列表——它是“批量、同步等待、保序”的接口。`pool.apply_async(f, args)` 立即返回一个 `AsyncResult` 对象，不阻塞；实际结果通过之后调用 `.get(timeout=...)` 获取，`.get()` 在结果未就绪时才阻塞，超时未完成会抛出 `TimeoutError`。需要提交多个独立任务、又想在等待期间做别的事情时用 `apply_async`；只需要“批量跑完拿到全部结果”时 `map` 更简单。
