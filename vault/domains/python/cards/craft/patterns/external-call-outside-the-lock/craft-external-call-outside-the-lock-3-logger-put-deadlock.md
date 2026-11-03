---
id: craft-external-call-outside-the-lock-3-logger-put-deadlock
node: craft.patterns.external-call-outside-the-lock
type: qa
step: 3
---
## Q
**外部调用不持锁 · 异步日志里持锁 put 为什么会互相等死**｜写法

异步日志用一条有界队列加一个工作线程：业务线程把记录 `put` 进队列，工作线程取出来写磁盘。业务线程在持有状态锁时调用会阻塞的 `put`，工作线程写失败后要拿同一把状态锁记错误次数。队列满了之后会发生什么？

## A
**要点。** 死锁。生产者握着锁卡在满队列的 `put` 上，等工作线程取走记录；工作线程卡在拿锁记账上，没法再取。两边各等对方。`put` 在有界队列满时会阻塞，所以它属于「外部调用」，一样不能放在锁里。

```python
def handle(self, n):
    if self.hold:
        with self.lock:
            self.q.put(n)        # 队列满时阻塞，还握着锁
    else:
        self.q.put(n)            # 阻塞的 put 不持锁

def _run(self):
    while True:
        self.q.get()
        try:
            raise OSError("磁盘写失败")
        except OSError:
            with self.lock:      # 工作线程拿同一把锁记账
                self.errors += 1
```

队列容量 1，写 10 条记录，1 秒后看生产者是否结束：

```
put 时持锁=True: 生产者 1 秒内结束了吗 -> False
put 时持锁=False: 生产者 1 秒内结束了吗 -> True
```

**为什么。** 参考解的做法：锁内只登记「我被接纳了」（`_inflight += 1`），出锁再 `put`，`finally` 里注销；关闭时 `close()` 等 `_inflight` 归零才放哨兵。

**易错。** 不抛异常时一切正常，这个死锁只在内层 handler 出错且队列满时出现，测试很难撞上。
