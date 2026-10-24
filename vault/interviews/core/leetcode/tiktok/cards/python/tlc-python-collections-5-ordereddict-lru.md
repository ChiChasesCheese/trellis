---
id: tlc-python-collections-5-ordereddict-lru
node: python.collections
type: qa
step: 5
---
## Q
**Python 工具箱｜`OrderedDict` 与「普通字典也有序」**

实现 LRU 缓存（LC 146）时，`OrderedDict` 的哪两个方法起作用？Python 3.7 之后普通 `dict` 也保持插入顺序，还需要 `OrderedDict` 吗？

## A
`OrderedDict` 在保持插入顺序的基础上多了两个 `O(1)` 操作：`move_to_end(key, last=True)` 把键移到末尾，`popitem(last=False)` 弹出**最老**的键。LRU 的「刚用过」移到末尾、「满了淘汰最久未用」弹出队首，正好对应。

```python
from collections import OrderedDict
od = OrderedDict(a=1, b=2, c=3)
od.move_to_end("a"); print(list(od))     # ['b', 'c', 'a']
print(od.popitem(last=False))            # ('b', 2)：弹出最老的
d = {"a": 1, "b": 2, "c": 3}
d["a"] = d.pop("a"); print(list(d))      # ['b', 'c', 'a']：普通字典先删再插，同样移到末尾
print(next(iter(d)))                     # b：普通字典取最老的键
```

- 普通 `dict` 的 `pop` 再赋值 + `next(iter(d))` 也能做 LRU，每步 `O(1)`；但 `next(iter(d))` 在删过很多键之后可能要跳过已删除的槽位，极端情况下不是严格 `O(1)`，面试里写 `OrderedDict` 更稳妥、意图更清楚。
- 面试官常追问「不许用 `OrderedDict`」：改写成哈希表 + 双向链表（`dict[key, Node]`，带哑头尾节点），`move_to_end` 对应「摘下节点再接到尾部」。
- **坑**：`OrderedDict` 的 `==` 比较**顺序也算**，普通 `dict` 不算。
