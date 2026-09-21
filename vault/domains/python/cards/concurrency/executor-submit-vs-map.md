---
id: executor-submit-vs-map
node: concurrency.executors
type: qa
source: python-docs
---
## Q
`Executor.submit(fn, *args)` 和 `Executor.map(fn, *iterables)` 的返回值形式有什么不同？

## A
`submit()` 一次提交一个调用，立即返回一个 `Future` 对象，代表这次调用的异步执行，需要 `.result()` 取值。`map()` 一次提交一批调用（对 iterable 里每个元素各调一次 `fn`），返回一个迭代器（不是列表），按*输入顺序*逐个产出结果——即使某个较早提交的任务比后面的任务先完成，迭代器也要等到它对应的结果被取出后才会往下走；这一点和标准库 `as_completed()` 按完成顺序返回正好相反。
