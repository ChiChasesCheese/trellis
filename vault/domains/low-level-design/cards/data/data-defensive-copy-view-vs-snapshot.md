---
id: data-defensive-copy-view-vs-snapshot
node: data.defensive-copy
type: qa
step: 4
---
## Q
`types.MappingProxyType(self._data)` 和 `dict(self._data)` 都能防止调用方直接改内部字典。它们给调用方的东西有什么不同？什么场合该选哪个？

## A
**视图是实时的，拷贝是快照**

- **只读视图（read-only view）**：不复制，`MappingProxyType` 包一层，调用方不能写；但内部之后的任何变化它都看得见；
- **拷贝**：O(n) 的一次性成本，拿到的是当时的状态，之后内部怎么变都和它无关；
- **选视图**：数据很大、调用方马上读完、读的过程中内部不会变（单线程内用完即弃）；
- **选拷贝**：调用方要长时间持有、跨线程、或者要拿它和“之后的状态”作比较；一次请求里读一个快照，前后才一致；
- **视图不挡嵌套**：内层的 list 仍然能被改（参考“不变量与封装”里的泄漏）。

```python
from types import MappingProxyType

data = {"a": 1}
view = MappingProxyType(data)
snap = dict(data)
data["b"] = 2                                   # 内部之后变了
print(dict(view), snap)                         # {'a': 1, 'b': 2} {'a': 1}
try: view["c"] = 3
except TypeError: print("read-only")
```

**知识点：**防御性拷贝（Defensive Copying）
