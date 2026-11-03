---
id: craft-condition-wait-predicate-loop-1-while-not-if
node: craft.patterns.condition-wait-predicate-loop
type: qa
step: 1
---
## Q
**条件变量等待循环 · 为什么等待必须写 while 而不是 if**｜写法

阻塞队列的 `get` 在队列为空时用条件变量（Condition）等待。写成 `if not self.items: self.cv.wait()` 看起来够了：被叫醒就说明有东西。可是两个消费者同时在等，生产者放入一个元素并叫醒了两个，会发生什么？

## A
**要点。** 被唤醒不等于条件成立。醒来到重新拿到锁之间，别的线程可能已经抢先把元素取走（还有操作系统层面的虚假唤醒，spurious wakeup）。所以等待必须在循环里重新检查谓词（predicate，即「我要等的那个条件」）：`while 条件不成立: wait()`。

```python
def get(self, out):
    with self.cv:
        while not self.items:         # 醒来后重新检查谓词
            self.cv.wait()
        out.append(self.items.pop(0))

def put(self, x):
    with self.cv:
        self.items.append(x)
        self.cv.notify_all()          # 两个消费者都被叫醒，但只有一个元素
```

两个消费者都在等，放入一个元素；`if` 版与 `while` 版对比（`while` 版再补一个元素）：

```
if    -> [1, 'IndexError：醒来时已经没有元素']
while -> [1, 2]
```

**为什么。** `wait()` 会释放锁并在醒来后重新获取锁，这两步之间别的线程可以改状态；谓词只有在持锁的那一刻才可信。

**易错。** 只有在谓词表达的是「状态」（队列长度、是否关闭），而不是「事件」（有人通知过我）时，循环才有意义；通知可能先于等待到达，状态不会丢。
