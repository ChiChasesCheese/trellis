---
id: executor-exception-on-result
node: concurrency.executors
type: qa
source: python-docs
---
## Q
如果提交给 `Executor` 的可调用对象在执行时抛出了异常，这个异常什么时候、在哪里被重新抛出？

## A
异常不会立刻传播，而是被 `Future` 捕获保存起来；只有调用方调用 `future.result()`（或者迭代 `executor.map()` 返回的迭代器取到对应位置）时，这个异常才会在调用方所在的线程里被重新抛出。这意味着如果代码只 `submit()` 而从不调用 `.result()`，异常会被静默吞掉，是常见的 bug 来源。
