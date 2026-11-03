---
id: craft-condition-wait-predicate-loop-2-two-conditions
node: craft.patterns.condition-wait-predicate-loop
type: qa
step: 2
---
## Q
**条件变量等待循环 · 一把锁配两个 Condition，省掉了什么**｜写法

有界阻塞队列要让生产者在「满」时等、消费者在「空」时等。只用一个 Condition 加 `notify_all` 可以正确，为什么参考解还是用两个共用同一把锁的 Condition？

## A
**要点。** 正确性两者都有（谓词循环保证），差别在唤醒的数量。一个 Condition 时，放入一个元素要叫醒所有等待者，包括同样在等「空位」的生产者，它们醒来发现条件不成立又睡回去（惊群，thundering herd）。两个 Condition 各管一种谓词，`put` 后只 `notify` 该醒的那一类。

```python
self.not_full = threading.Condition(self.lock)
self.not_empty = threading.Condition(self.lock)   # 同一把锁

def put(self, x):
    with self.not_full:
        while len(self.items) >= self.cap:
            self.not_full.wait()
        self.items.append(x)
        self.not_empty.notify()                    # 只叫醒消费者

def get(self):
    with self.not_empty:
        while not self.items:
            self.not_empty.wait()
        x = self.items.pop(0)
        self.not_full.notify()                     # 只叫醒生产者
        return x
```

容量 1，已满，8 个生产者在等，消费者取 9 次，数生产者被唤醒的总次数：

```
一个 Condition + notify_all -> 生产者被唤醒 36 次
两个 Condition + notify     -> 生产者被唤醒 8 次
```

**为什么。** 36 是 8+7+…+1：每次取一个，所有还在等的生产者都醒一遍。

**易错。** 两个 Condition 必须共用同一把锁，否则「检查谓词」和「改状态」不在一个临界区。`notify` 叫错了类（该叫生产者却叫了消费者）是常见 bug，后果是有人永远睡着。
