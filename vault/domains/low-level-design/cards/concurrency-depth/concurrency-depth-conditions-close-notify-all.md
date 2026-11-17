---
id: concurrency-depth-conditions-close-notify-all
node: concurrency-depth.conditions
type: qa
step: 3
---
## Q
一个任务队列有 3 个消费线程都阻塞在 `get()`。服务关闭时调用 `close()`，用 `notify()` 实现，结果只有一个线程退出，进程挂住。什么时候用 `notify()`，什么时候必须用 `notify_all()`？

## A
**一次变化只够一个等待者用，才用 `notify()`**

- **放进一个元素**：只有一个消费者能拿到它，叫醒一个就够，叫醒全部是白白惊动；
- **关闭、取消、状态整体翻转**：对所有等待者都有意义，必须 `notify_all()`，否则其余线程永远睡着；
- **释放 n 个资源**：`notify(n)` 叫醒 n 个；
- **拿不准就用 `notify_all()`**：等待方都是 `while` 或 `wait_for` 检查谓词，多醒几个只会多检查一次，不会出错；少醒一个则可能死锁；
- **关闭要写进谓词**：`wait_for` 的条件是“有元素，或者已关闭”，否则被叫醒的线程发现队列空，又睡回去。

```python
import threading
class Box:
    def __init__(self):
        self.c, self.items, self.closed = threading.Condition(), [], False
    def get(self):
        with self.c:
            self.c.wait_for(lambda: self.items or self.closed)
            return self.items.pop(0) if self.items else None   # None：已关闭且取空
    def close(self):
        with self.c:
            self.closed = True; self.c.notify_all()            # notify() 只醒一个
box = Box()
ts = [threading.Thread(target=box.get) for _ in range(3)]
[t.start() for t in ts]; box.close(); [t.join(1) for t in ts]
print([t.is_alive() for t in ts])                              # [False, False, False]
```

<details class="pt"><summary>延伸</summary>

关闭之后还在 `put` 的生产者应该立刻收到错误，不要悄悄丢数据。取空之后返回 `None` 还是抛异常，是接口契约，要和调用方约好。

</details>

**知识点：**条件变量（Condition Variables）
