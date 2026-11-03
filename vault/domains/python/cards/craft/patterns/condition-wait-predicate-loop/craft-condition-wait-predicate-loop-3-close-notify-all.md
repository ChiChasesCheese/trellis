---
id: craft-condition-wait-predicate-loop-3-close-notify-all
node: craft.patterns.condition-wait-predicate-loop
type: qa
step: 3
---
## Q
**条件变量等待循环 · close() 为什么要 notify_all，漏掉会怎样**｜模式

队列有 `close()`：关闭后不再接收新元素，已有的取完，等待的消费者应该醒来返回。如果 `close()` 只把 `closed` 设成 True，没有通知，一个正在等空队列的消费者会怎样？

## A
**要点。** 它会永远睡下去：谓词里虽然包含了 `closed`，但没人叫醒它去重新检查。关闭是「所有等待者的谓词同时变化」，要广播（`notify_all`），并且对每个 Condition 都要广播（生产者等的 `not_full` 和消费者等的 `not_empty`）。

```python
def get(self):
    with self.not_empty:
        while not self.items and not self.closed:    # 谓词里要包含 closed
            self.not_empty.wait()
        return self.items.pop(0) if self.items else None

def close(self):
    with self.not_empty:
        self.closed = True
        self.not_empty.notify_all()                  # 叫醒所有等待者，让它们看到 closed
```

一个消费者在空队列上等，随后 `close()`：

```
close() 里 notify_all: False -> 消费者线程还卡着吗: True
close() 里 notify_all: True -> 消费者线程还卡着吗: False
```

**为什么。** 状态变化与通知要成对：每个会让某个谓词变化的地方（放入、取出、关闭、退订）都要想一遍「谁在等这个谓词」。

**易错。** 症状是程序退出时挂起、关闭测试偶发超时，不是异常。漏掉其中一个 Condition 只会让一半的线程卡住，更难发现。
