---
id: concurrency-queue-vs-deque
node: concurrency.primitives
type: qa
step: 5
---
## Q
`queue.Queue` 和 `collections.deque` 都能在多线程间传递数据，二者的线程安全边界分别是什么？

## A
`queue.Queue` 是标准库里为多生产者-多消费者场景设计的线程安全队列：内部持锁，`put()`/`get()` 本身就是同步点，还提供 `maxsize` 做背压、`task_done()`/`join()` 做完成追踪，`get()` 在队列为空时会阻塞（而不是抛异常）。

`deque` 本身不是"线程安全队列"，但它的**单次** `append()`/`appendleft()`/`pop()`/`popleft()` 因为是单条字节码操作，天然是原子的、不需要额外加锁，可以安全地被多个线程调用；它没有阻塞语义（空的时候 `pop()` 直接抛 `IndexError`），也没有内置的容量上限背压。常见误用：把"单次操作原子"错误地推广成"整个使用模式都安全"——比如"先检查 `len(dq)` 再决定要不要 `pop`"仍然是一次 check-then-act 复合操作，`deque` 不会替你保护它。
