---
id: concurrency-condvar-wait-loop
node: concurrency.primitives
type: qa
step: 3
---
## Q
为什么 `threading.Condition` 的等待必须写成
```python
with cond:
    while not predicate():
        cond.wait()
```
而不能写成 `if not predicate(): cond.wait()`？

## A
两个理由。第一，`wait()` 允许**虚假唤醒**（spurious wakeup）——即使没人调用 `notify()`，等待也可能提前返回。第二，即使确实是被 `notify()` 唤醒的，从"被唤醒"到"重新拿回锁、真正往下执行"之间，可能有别的线程（包括被 `notify_all()` 唤醒的其他等待者）抢先把条件又改回不成立——比如队列刚被 `notify` 说"有元素了"，另一个消费者先醒来把它取走了。

`while` 循环在拿到锁之后重新检查谓词，只有条件真正成立才会跳出循环继续执行；这是使用条件变量唯一安全的写法，标准库甚至提供了等价的 `cond.wait_for(predicate)` 帮你把这个循环写对。
