---
id: hi-lld-intro-4-blocking-queue
node: qb.lld.kv-store-eviction.pre-lld-concurrency-intro
type: qa
step: 4
---
## Q
**阻塞队列与生产者消费者**｜低层设计 · 并发

线程之间交接工作用什么？阻塞队列（blocking queue）怎么工作，为什么优先用它而不是自己写条件变量？

## A
**要点。** 阻塞队列是队列加条件变量，提供线程安全的生产者、消费者交接：生产者用 `put()` 放入，队列满则阻塞；消费者用 `take()` 或 `get()` 取出，队列空则阻塞。所有同步都在队列内部完成。

```python
import queue

q: "queue.Queue[str]" = queue.Queue(maxsize=100)   # 有界队列，满了生产者会被拖慢

def produce(task: str) -> None:
    q.put(task)        # 队列满时阻塞，形成背压

def consume() -> str:
    return q.get()     # 队列空时阻塞，不空转烧 CPU
```

**为什么。** 空队列时消费者要高效等待而不是空转；满队列时生产者要放慢。有界队列天然带来背压。

**使用时机。** 异步请求处理、突发流量缓冲，以及资源池化。它是线程间交接工作的首选工具。
