---
id: craft-copy-in-copy-out-1-copy-both-sides
node: craft.idioms.copy-in-copy-out
type: qa
step: 1
---
## Q
**边界拷贝 · 为什么存进来要拷一次，取出去还要拷一次**｜写法

一个内存表 `Table` 提供 `insert(row)` 和 `select()`，行是 dict。调用方插入后又改了自己手里的 dict，或者改了 `select` 返回的 dict，表里的数据就变了。只在一侧做防护够不够？应该怎么写？

## A
**要点。** Python 里对象是按引用传递的：存进表里的是调用方那个 dict 本身，两边指向同一个对象（别名，aliasing）。可变数据穿过边界时，两个方向各有一个泄漏口：进口（调用方事后改自己的对象）和出口（调用方改拿到的结果）。所以进来拷一次，出去再拷一次，表内部的数据才只有表自己能碰。

```python
import copy

class LeakyTable:
    def __init__(self) -> None:
        self._rows: list[dict] = []
    def insert(self, row: dict) -> None:
        self._rows.append(row)                       # 存了调用方的对象本身
    def select(self) -> list[dict]:
        return list(self._rows)                      # 只拷了外层列表，行还是共享的

class Table:
    def __init__(self) -> None:
        self._rows: list[dict] = []
    def insert(self, row: dict) -> None:
        self._rows.append(copy.deepcopy(row))        # 进来拷一次
    def select(self) -> list[dict]:
        return [copy.deepcopy(r) for r in self._rows]    # 出去再拷一次

for cls in (LeakyTable, Table):
    t = cls()
    row = {"id": 1, "tags": ["a"]}
    t.insert(row)
    row["tags"].append("B")                          # 进口泄漏：调用方事后改自己的行
    out = t.select()
    out[0]["id"] = 999                               # 出口泄漏：调用方改拿到的结果
    print(cls.__name__, t.select()[0])
```

实际输出：

```
LeakyTable {'id': 999, 'tags': ['a', 'B']}
Table {'id': 1, 'tags': ['a']}
```

**为什么。** 泄漏版两处都被改了：`tags` 来自进口，`id` 来自出口。`list(self._rows)` 看起来像拷贝，但只拷了外层列表，里面的行仍是同一批对象。

**代价。** 深拷贝（deepcopy）随数据量线性增长，每次查询都拷一遍结果；这是为正确性付的钱。热路径上的做法是让数据本身不可变，就不用拷：存冻结对象或 tuple，边界上共享同一份也安全。
