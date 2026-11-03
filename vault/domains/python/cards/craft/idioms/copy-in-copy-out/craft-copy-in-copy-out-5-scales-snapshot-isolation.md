---
id: craft-copy-in-copy-out-5-scales-snapshot-isolation
node: craft.idioms.copy-in-copy-out
type: qa
step: 5
---
## Q
**边界拷贝 · 从 clone-graph 到快照隔离**｜写法

LeetCode 的 Clone Graph 要深拷贝一个有环的图；内存表的 `select` 返回副本；数据库的读者看到的是事务开始时的一致版本。三者都是「拿到的东西与源头隔离」，机制上有什么共同点和差别？

## A
**要点。** 都在回答同一个问题：读者拿到的数据，会不会被写者之后的修改影响。Clone Graph 解决的是怎么拷得正确（环要用「已拷贝」表断开，先登记后递归）；表的边界拷贝在每次读时付拷贝的钱；数据库用多版本（MVCC）让每个读者看到一个固定版本，写者追加新版本而不是原地改，于是读写不互相拷贝也不阻塞。

```python
import copy

class Node:
    def __init__(self, val: int, neighbors: "list[Node] | None" = None) -> None:
        self.val, self.neighbors = val, neighbors or []

def clone(node: Node, seen: dict[Node, Node] | None = None) -> Node:
    seen = {} if seen is None else seen
    if node in seen:                                   # 已经拷过：直接返回，环就断了
        return seen[node]
    c = seen[node] = Node(node.val)                    # 先登记再递归
    c.neighbors = [clone(n, seen) for n in node.neighbors]
    return c

a, b = Node(1), Node(2)
a.neighbors, b.neighbors = [b], [a]                    # 环
a2 = clone(a)
print(a2 is not a, a2.neighbors[0].neighbors[0] is a2, a2.neighbors[0] is not b)
a3 = copy.deepcopy(a)                                  # deepcopy 内部也是同样的 memo 表
print(a3.neighbors[0].neighbors[0] is a3)
```

实际输出：

```
True True True
True
```

**变化。** 三个规模的成本不同：拷贝在读时付钱（LeetCode 级与内存表）；版本在写时付钱，旧版本要保留到最老的读者结束（数据库）。读多写少、数据小：读时拷贝最简单；读多且数据大：写时生成不可变的新版本，读者只拿引用。

**易错。** `clone` 里「先登记再递归」的顺序决定了环不会无限递归；写成先递归再登记，遇到环就会栈溢出。`copy.deepcopy` 自带这张表，所以自定义对象通常直接用它，只在需要控制拷贝什么时才自己写。
