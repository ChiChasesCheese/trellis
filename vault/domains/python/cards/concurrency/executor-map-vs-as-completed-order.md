---
id: executor-map-vs-as-completed-order
node: concurrency.executors
type: qa
source: python-docs
---
## Q
`executor.map(fn, urls)` 和 `concurrent.futures.as_completed(futures)` 在“结果出现的顺序”上有什么区别？

## A
`map()` 保序：结果按传入 `iterable` 的原始顺序产出，不管任务实际完成的先后。`as_completed(futures)` 不保序：它是一个生成器，谁先完成就先把谁的 `Future` yield 出来，因此更适合“先到先处理”的场景（比如先展示已经下载完的网页），而需要按输入顺序对应结果时应该用 `map()` 或手动维护 `{future: 对应输入}` 的映射。
