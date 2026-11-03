---
id: craft-functional-core-imperative-shell-4-same-shape
node: craft.architecture.functional-core-imperative-shell
type: qa
step: 4
---
## Q
**函数式核心 + 命令式外壳 · 表格求值、文件监视里的同一种拆法**｜架构

电子表格要求值，文件监视器要找出哪些文件变了。两个系统都得处理「格子存在哪」「快照怎么拍」这类有状态的事。它们是怎么把有状态的部分挡在算法之外的？外壳递给核心的东西各是什么？

## A
**要点。** 核心把「世界」当参数：表格求值收一个 `read(cell)` 函数，文件监视收两张快照。不变的是核心只看参数；变的是外壳递过去什么：一个读取函数、两个不可变快照。

```python
from __future__ import annotations
# spreadsheet-engine：evaluate(node, read) 不知道格子存在哪，见下面的缩小版

# amz-file-watcher：不知道快照怎么拍
def diff(old: Snapshot, new: Snapshot) -> list[Event]:
    events = [Event(EventKind.CREATED, p) for p in new.keys() - old.keys()]
    events += [Event(EventKind.DELETED, p) for p in old.keys() - new.keys()]
    events += [Event(EventKind.MODIFIED, p) for p in old.keys() & new.keys()
               if old[p] != new[p]]
    return sorted(events, key=lambda e: (e.path, e.kind.value))
```

同一个 `evaluate`，外壳换一个 `read` 就换了缓存策略。缩小版：`cells = {"A1": 2.0, "B1": ("+", "A1", 3.0)}`，求 `("*", "B1", "B1")`：

```python
Node = float | str | tuple          # 数字|格子名|(op,左,右)

def evaluate(node: Node, read: Callable[[str], float | None]) -> float:
    match node:
        case float() | int():
            return node
        case str():
            return v if (v := read(node)) is not None else 0.0  # 空格当0
        case (op, l, r):
            a, b = evaluate(l, read), evaluate(r, read)
            return a + b if op == "+" else a * b

cells = {"A1": 2.0, "B1": ("+", "A1", 3.0)}
calls = []

def read_formula(c: str) -> float | None:      # 每次现算
    calls.append(c)
    v = cells.get(c)
    return evaluate(v, read_formula) if isinstance(v, tuple) else v

cache: dict[str, float | None] = {}
def read_cached(c: str) -> float | None:        # 先查缓存
    if c not in cache:
        v = cells.get(c)
        cache[c] = evaluate(v, read_cached) if isinstance(v, tuple) else v
    return cache[c]

tree = ("*", "B1", "B1")
print(evaluate(tree, read_formula), "读格子次数", len(calls))
calls.clear()
print(evaluate(tree, read_cached), "缓存里有", sorted(cache))
```

实际输出（`calls` 记录读取次数，缓存版第二次求值前先清空）：

```
25.0 读格子次数 4
25.0 缓存里有 ['A1', 'B1']
```

**为什么。** 求值函数在「每次现算」和「带缓存」两种做法下都不用改，因为它只通过 `read` 看世界。

**易错。** `read` 如果是有副作用的（比如读时顺手写缓存），核心仍然是纯的，但副作用全在外壳传入的函数里，测试时要换成假的 `read`，别以为核心自带缓存。
