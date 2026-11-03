---
id: craft-ordered-multi-lock-acquisition-1-abba-deadlock
node: craft.patterns.ordered-multi-lock-acquisition
type: qa
step: 1
---
## Q
**固定顺序加多把锁 · 为什么转账要按账户 id 而不是按参数顺序加锁**｜写法

转账要同时改两个账户，每个账户一把锁。写成「先锁转出方、再锁转入方」，x 转给 y 的同时 y 转给 x，会发生什么？怎样改才保证不会？

## A
**要点。** 死锁。线程 1 持有 x 等 y，线程 2 持有 y 等 x，谁也等不到。这是环形等待（circular wait），破坏它最便宜的办法是让所有线程按同一个全局顺序拿锁：按账户 id 排序，与谁是转出方无关。这不是优化，而是不死锁的唯一理由。

```python
def transfer_param_order(a, b, amount):
    with a.lock:                       # 按参数顺序：先 from 后 to
        time.sleep(0.05)               # 让两个方向都先拿到第一把
        with b.lock:
            ...

def transfer_sorted(a, b, amount):
    first, second = sorted((a, b), key=lambda x: x.id)   # 全局固定顺序：按 id
    with first.lock:
        with second.lock:
            ...
```

x→y 和 y→x 同时发起，1 秒后看线程是否还卡着：

```
transfer_param_order 两个线程 1 秒后仍卡着: True
transfer_sorted      两个线程 1 秒后仍卡着: False
```

**为什么。** 排序后，两个方向都先抢 id 较小的账户，只会排队，不会互相等待。

**易错。** 死锁取决于时机：不加 `sleep` 时，它可能跑上一万次才出现一次。别靠测试发现，靠规则杜绝。
