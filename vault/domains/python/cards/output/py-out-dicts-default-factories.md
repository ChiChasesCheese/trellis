---
id: py-out-dicts-default-factories
node: output.dicts
type: qa
step: 3
---
## Q
**get、defaultdict 与 setdefault**｜读代码说输出

```python
from collections import defaultdict
d = {}
d.get("x"); print(d)
dd = defaultdict(list)
dd["x"]; print(dict(dd))
def mk(): print("built"); return []
e = {}
e.setdefault("k", mk()); e.setdefault("k", mk())
print(e)
```

输出什么？

## A
**输出。**
```
{}
{'x': []}
built
built
{'k': []}
```

**为什么。**
- `d.get("x")` 只读，不插入，字典仍为空。
- `defaultdict` 的 `dd["x"]` 触发 `__missing__`：调用 `list()` 造出默认值**并存进字典**，所以只是“读一下”也让字典多了一个键。
- `setdefault(key, default)` 的 `default` 是普通参数，调用前就已求值：第二次 key 已存在，`mk()` 照样跑了，只是结果被丢弃。

**语言为什么这样设计。**
- `defaultdict` 把“缺键时造默认值”做成工厂（factory，每次缺键才调用一个无参函数），避免每次写 `if k not in d`；代价是读操作会改字典。
- `setdefault` 是普通方法，参数先求值是函数调用的通用规则；惰性求值只有 `and/or` 与条件表达式才有。Java 的 `computeIfAbsent` 用 lambda 才做到惰性。

**怎么写才对。**
```python
groups = defaultdict(list)
groups[key].append(item)      # 只在缺键时才创建列表
```

**面试里一句话。**
`defaultdict` inserts on read, and `setdefault` evaluates its default eagerly, so use a factory when the default is expensive.
