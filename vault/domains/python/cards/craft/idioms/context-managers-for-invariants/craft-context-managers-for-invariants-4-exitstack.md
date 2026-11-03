---
id: craft-context-managers-for-invariants-4-exitstack
node: craft.idioms.context-managers-for-invariants
type: qa
step: 4
---
## Q
**上下文管理器守不变量 · 个数不定的锁为什么用 `ExitStack`**｜写法

中转机票要同时锁住若干个航班实例，组合限流器要同时锁住所有规则的状态，个数运行时才知道。嵌套 `with` 写不出来，手写一个循环加 `try / finally` 又容易漏。`ExitStack` 解决了什么？

## A
**要点。** `ExitStack` 是「一叠」上下文管理器：用 `enter_context` 一个个压进去，离开 `with ExitStack()` 时按**后进先出**（LIFO）逐个退出。如果压到一半某一个进入失败，已经进入的那些也会被正确退出。锁正是需要这个顺序：后拿的先放，和嵌套 `with` 一样。

```python
log: list[str] = []

@contextmanager
def lock(name: str, fail: bool = False):
    if fail:
        raise RuntimeError(f"拿不到 {name}")
    log.append(f"+{name}")
    try:
        yield
    finally:
        log.append(f"-{name}")

def hold_all(names: list[str], fail_at: str | None = None):
    # 个数在运行期才知道：嵌套 with 写不出来
    with ExitStack() as stack:
        for n in sorted(names):            # 固定顺序加锁，防死锁
            stack.enter_context(lock(n, fail=(n == fail_at)))
        log.append("临界区")

hold_all(["b", "a", "c"])
print("正常:", log); log.clear()
try:
    hold_all(["b", "a", "c"], fail_at="c")
except RuntimeError as e:
    print("第三把失败:", e)
print("已拿到的会被放掉:", log)
```

实际输出：

```
正常: ['+a', '+b', '+c', '临界区', '-c', '-b', '-a']
第三把失败: 拿不到 c
已拿到的会被放掉: ['+a', '+b', '-b', '-a']
```

**为什么。** 手写版要自己记录「拿到了哪几把」，并在失败时倒序释放，一旦漏掉就是锁泄漏。航班订票还把请求按 `key` 排序再依次进入：多把锁必须按全局一致的顺序拿，才不会两个行程互相等对方的锁而死锁。

**代价。** `ExitStack` 隐藏了「这里一共持有几把锁」，在临界区里更难看出来。持锁越多，临界区越要短，也越该考虑是否该拆成更少的锁。
