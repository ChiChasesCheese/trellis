---
id: concurrency-lock-ordering-transfer
node: concurrency.hazards
type: qa
step: 3
---
## Q
```python
def transfer(a, b, amount):
    with a.lock:
        with b.lock:
            a.balance -= amount
            b.balance += amount
```
`transfer(x, y, 10)` 和 `transfer(y, x, 5)` 并发执行时会死锁吗？怎么修？

## A
会。两次调用分别先锁 `x` 后锁 `y`、先锁 `y` 后锁 `x`，如果第一个线程刚拿到 `x.lock` 还没碰 `y.lock`，第二个线程刚好拿到 `y.lock` 还没碰 `x.lock`，两边就都在等对方持有的锁——这正是循环等待，四个死锁条件同时成立。

修法是**统一加锁顺序**：不按参数出现的顺序加锁，而是按账户的某个固定属性（比如账户 id）排序后再加锁，让所有线程无论怎么调用都按同一个顺序拿锁，从根上消灭循环等待：

```python
def transfer(a, b, amount):
    first, second = sorted([a, b], key=lambda acc: acc.id)
    with first.lock, second.lock:
        a.balance -= amount
        b.balance += amount
```
