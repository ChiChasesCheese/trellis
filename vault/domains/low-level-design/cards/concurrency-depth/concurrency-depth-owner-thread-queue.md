---
id: concurrency-depth-owner-thread-queue
node: concurrency-depth.confinement
type: qa
step: 3
---
## Q
一个计数表会被很多线程更新，又不想到处加锁。“让一个线程独占这张表，其他线程通过 `queue.Queue` 发消息”是怎么做的？和直接加锁比，取舍是什么？

## A
**状态只属于一个 owner 线程，别人发消息**

- **做法**：owner 线程循环 `get()` 取消息、改自己的字典、把结果放进消息里带的回复队列；字典从不被第二个线程碰，所以没有锁；
- **命令天然串行化**：队列保证先进先出，复合操作（读、改、返回）在 owner 线程里是一个整体；
- **关闭**：放一个哨兵（`None`）让循环退出，再 `join()`；
- **代价**：每次调用多一次线程往返，吞吐被单个 owner 线程限住；示例的队列无界，积压会吃掉内存，要限长就用 `Queue(maxsize=…)`；
- **什么时候选它**：状态大或操作长，加锁会让所有调用方互相阻塞；状态小、操作短就直接加锁，更简单；
- **异常**：示例没有处理；owner 线程里的异常要自己捕获并通过回复队列传回去，否则 owner 死了，后面的调用方永远等。

```python
import queue, threading
class HitCounter:
    def __init__(self):
        self._q, self._n = queue.Queue(), {}      # _n 只有 owner 线程碰
        self._t = threading.Thread(target=self._loop); self._t.start()
    def _loop(self):
        while (msg := self._q.get()) is not None:
            key, reply = msg
            self._n[key] = self._n.get(key, 0) + 1
            reply.put(self._n[key])
    def hit(self, key):
        reply = queue.Queue(1); self._q.put((key, reply)); return reply.get()
    def close(self): self._q.put(None); self._t.join()
c = HitCounter(); print(c.hit("a"), c.hit("a"), c.hit("b")); c.close()   # 1 2 1
```

**知识点：**不靠锁的线程安全（Immutability & Confinement）
