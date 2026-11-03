---
id: craft-backpressure-overflow-policy-3-block-releases-lock
node: craft.patterns.backpressure-overflow-policy
type: qa
step: 3
---
## Q
**反压与溢出策略 · 日志处理器：阻塞的 put 为什么不能放在锁里**｜写法

异步日志处理器：业务线程把日志记录放进有界队列，后台线程慢慢写盘。队列满了，可以选择丢弃并计数，或者阻塞业务线程。这两种策略在加锁上有什么不同？为什么日志不应该把业务线程卡住？

## A
**要点。** `put_nowait` 不会阻塞，放在锁里没问题（丢弃分支）。阻塞版的 `put` 可能等很久，**绝不能持有锁去等**：别的线程要用同一把锁来关闭处理器、统计丢弃数，被一个正在等队列的线程挡住，整个系统卡死。做法：在锁内登记「我要放一条」（`_inflight += 1`），出锁后再做阻塞的 `put`，最后在锁内注销；`close()` 先置关闭标志，再等 `_inflight` 归零才放入结束哨兵，于是每条被接受的记录都排在哨兵之前。

```python
import queue, threading, time

class AsyncHandler:
    """把记录放进有界队列，后台线程慢慢写。drop_when_full=True 时满了就丢并计数。"""
    def __init__(self, cap, drop_when_full):
        self.q = queue.Queue(maxsize=cap)
        self.drop, self.dropped, self.lock = drop_when_full, 0, threading.Lock()

    def handle(self, rec) -> bool:
        if self.drop:
            try: self.q.put_nowait(rec); return True       # 非阻塞，业务线程永远不被日志拖慢
            except queue.Full:
                with self.lock: self.dropped += 1          # 丢了，但留下数字
                return False
        self.q.put(rec); return True                       # 阻塞：一条不丢，代价是业务线程可能卡住

h = AsyncHandler(cap=3, drop_when_full=True)                # 后台线程卡住了（没人消费）
t0 = time.perf_counter()
results = [h.handle(i) for i in range(10)]
print("10 条记录:", results.count(True), "条入队，", h.dropped, "条丢弃；业务线程总耗时 <0.1s:", time.perf_counter() - t0 < 0.1)

blocker = AsyncHandler(cap=3, drop_when_full=False)
th = threading.Thread(target=lambda: [blocker.handle(i) for i in range(10)], daemon=True)
th.start(); th.join(timeout=0.3)
print("阻塞版：业务线程 0.3 秒后还卡在 put 上:", th.is_alive(), "，队列里:", blocker.q.qsize())
```

后台线程卡住（没人消费），队列容量 3，写 10 条：

```
10 条记录: 3 条入队， 7 条丢弃；业务线程总耗时 <0.1s: True
阻塞版：业务线程 0.3 秒后还卡在 put 上: True ，队列里: 3
```

**为什么。** 日志是旁路：业务逻辑成不成功不该取决于磁盘写得快不快。所以日志处理器的默认应当是不阻塞，满了丢弃并计数（`dropped`）。真正不能丢的审计日志才选阻塞，并且要承担「磁盘慢 = 业务慢」的后果。

**易错。** 后台线程里的异常不能杀掉消费循环：`except Exception: errors += 1` 加 `finally: task_done()`，否则一条写失败的记录会让 `flush()` 永远等不到队列清空。

**见 external-call-outside-the-lock。** 阻塞调用不持锁，是这叶的并发版本。
