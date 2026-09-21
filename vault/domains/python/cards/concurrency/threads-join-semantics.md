---
id: threads-join-semantics
node: concurrency.threads
type: qa
source: python-docs
---
## Q
`thread.join(timeout=...)` 超时后返回值是什么？如何判断是否真的等到了超时？

## A
`join()` 无论是否超时都返回 `None`，不会告诉调用者结果。必须在 `join()` 之后再调用 `thread.is_alive()`：如果线程仍存活，说明是超时返回而不是线程终止返回。另外，`join()` 一个尚未 `start()` 的线程，或者线程 `join` 自身（会造成死锁），都会抛出 `RuntimeError`。
