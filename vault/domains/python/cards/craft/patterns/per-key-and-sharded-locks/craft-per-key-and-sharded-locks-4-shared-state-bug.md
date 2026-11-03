---
id: craft-per-key-and-sharded-locks-4-shared-state-bug
node: craft.patterns.per-key-and-sharded-locks
type: qa
step: 4
---
## Q
**每对象一把锁与分片锁 · 每个账户一把锁，为什么还会在发转账编号时出错**｜写法

钱包转账只锁涉及的两个账户，不相干的账户对可以并行。转账编号用 `T1、T2……` 递增，写成一个生成器表达式 `(f"T{n}" for n in count(1))`，每次转账 `next(ids)`。不同账户对的转账并发取号，会发生什么？

## A
**要点。** 账户锁只保护账户，而编号生成器是所有账户对共享的状态，它不在任何一把账户锁的保护下。多个线程同时对同一个生成器调 `next`，一个线程正在执行生成器体时，另一个线程再进入，抛出 `ValueError: generator already executing`。生成器同一时刻只允许一个线程在它的帧里执行，它不是线程安全的。

```python
def slow(n):
    time.sleep(0.001)                       # 生成器体里有一点耗时：窗口被放大
    return f"T{n}"

make_ids = lambda: (slow(n) for n in itertools.count(1))       # 生成器表达式
make_ids = lambda: map("T{}".format, itertools.count(1))       # itertools.count 版
```

8 个线程各取 20 个号：

```
生成器表达式 : 取到 20 个，唯一 20 个，异常 140 次 {'generator already executing'}
itertools.count: 取到 160 个，唯一 160 个，异常 0 次 
```

**为什么用 `itertools.count`。** CPython 里 `next(count)` 在 C 里一步完成，不会被中途打断，所以参考解直接用它。这是 CPython 的实现性质，不是语言规范的承诺；自由线程构建或其他实现里，要对取号加锁。

**代价。** 生成器表达式在生成器体里没有耗时时，冲突窗口极小，错误很难复现，但仍然存在。

**信号。** 「按对象加锁」时，检查有没有被所有对象共用的东西：计数器、生成器、日志、注册表。它们需要自己的锁或原子操作。
