---
id: craft-context-managers-for-invariants-1-cleanup-in-one-place
node: craft.idioms.context-managers-for-invariants
type: qa
step: 1
---
## Q
**上下文管理器守不变量 · 为什么「失败释放键、成败都唤醒」要写成 `@contextmanager`**｜写法

幂等转账的拥有者执行时必须保证两件事：失败就释放键，无论成败都唤醒等待者。把 `try / except / finally` 直接写在执行函数里似乎也行，为什么抽成 `_owning` 并用 `with` 调用？漏掉一条路径会出什么 bug？

## A
**要点。** 「进入时做 A，退出时一定做 B」这种配对（资源获取与释放，RAII 的思路）是不变量，不是业务。写在执行函数里，每多一个出口（早返回、新加的 `raise`、别人加的 `continue`），就多一次忘记收尾的机会。上下文管理器（context manager）把收尾放在一处，`with` 块无论怎么退出都会执行它，业务函数里只剩业务。

```python
keys: dict[str, "Slot"] = {}
class Slot:
    def __init__(self): self.done = threading.Event()

# 手写版：每个出口都要记得收尾，早返回一条就漏
def run_manual(key, work, fail_early=False):
    slot = keys[key] = Slot()
    try:
        if fail_early:
            return "early"                 # 这个出口没人释放键、没人唤醒等待者
        work()
    except BaseException:
        del keys[key]
        raise
    slot.done.set()                        # 只有走到这里才唤醒

# 上下文管理器版：收尾集中在一处，调用方只剩业务
@contextmanager
def owning(key):
    slot = keys[key] = Slot()
    try:
        yield slot
    except BaseException:
        del keys[key]                      # 失败：释放键，允许重试
        raise
    finally:
        slot.done.set()                    # 无论成败都唤醒等待者

def run(key, work, fail_early=False):
    with owning(key) as slot:
        if fail_early:
            return "early"                 # 早返回也会走 finally
        work()

run_manual("a", lambda: None, fail_early=True)
print("手写版 早返回: 等待者被唤醒了吗?", keys["a"].done.is_set())
run("b", lambda: None, fail_early=True)
print("管理器版 早返回: 等待者被唤醒了吗?", keys["b"].done.is_set())
def boom(): raise RuntimeError("网关超时")
try:
    run("c", boom)
except RuntimeError:
    print("失败后键还在表里吗?", "c" in keys)
```

实际输出：

```
手写版 早返回: 等待者被唤醒了吗? False
管理器版 早返回: 等待者被唤醒了吗? True
失败后键还在表里吗? False
```

**为什么。** 手写版的 bug 恰好出在早返回：等待者永远等不到事件，调用方看到的是「偶尔卡住」，几乎没法复现。

**代价。** 收尾逻辑不在业务代码旁边，读代码的人要跳到管理器里看。所以管理器的名字要说明它守着什么（`owning`、`locked`），docstring 写清「进入时占什么、退出时放什么」。
