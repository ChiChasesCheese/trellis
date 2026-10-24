---
id: tlc-python-collections-3-defaultdict
node: python.collections
type: qa
step: 3
---
## Q
**Python 工具箱｜`defaultdict`**

分组（异位词分组）和建邻接表时，`defaultdict(list)` 比普通字典省掉了什么？它读取缺失键时有什么副作用，怎样避免？

## A
`defaultdict(factory)` 在访问缺失键时调用 `factory()` 生成默认值并**插入**，所以 `g[k].append(x)` 一步完成「没有就建、再追加」。

```python
from collections import defaultdict
g: defaultdict[str, list[str]] = defaultdict(list)
for w in ["eat", "tea", "tan", "ate", "nat", "bat"]:
    g["".join(sorted(w))].append(w)   # 以排序后的字符串为签名分组
print(dict(g))   # {'aet': ['eat','tea','ate'], 'ant': ['tan','nat'], 'abt': ['bat']}
d = defaultdict(int)
print(d["x"], "y" in d, dict(d))      # 0 False {'x': 0}：读 d["x"] 已经把 x 插进去了
```

- 常用工厂：`list`（分组、邻接表）、`int`（计数，`d[k] += 1`）、`set`（去重分组）、`lambda: [0, 0]`（成对统计）。
- 等价的普通字典写法是 `d.setdefault(k, []).append(x)`，但每次都会新建一个 `[]` 再丢掉；`defaultdict` 只在缺失时才建。
- **副作用**：只是「查一下有没有」也会插入。判断存在用 `k in d` 或 `d.get(k)`，不要用 `d[k]`；遍历前若还要保证键数不变，先转成 `dict(d)`。

适用题型：LC 49 异位词分组、图的邻接表（LC 207、210）、LC 721 账户合并。
