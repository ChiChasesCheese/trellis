---
id: tlc-insert-delete-getrandom-o1-4-followup
node: a.insert-delete-getrandom-o1
type: qa
step: 4
---
## Q
**LC 380 O(1) 时间插入、删除和获取随机元素**｜追问

面试官接着问：（1）允许重复元素（每个元素出现几次，就按几次的比例被抽中）怎么改？（2）每个元素带权重怎么办？（3）多线程使用呢？

## A
1. **允许重复（LC 381）**：字典改成 `值 -> 下标集合`。`insert` 把新下标加进集合，返回该值此前是否不存在；`remove` 从集合里取出任意一个下标，用末尾元素补位，并在末尾元素的下标集合里把旧位置（末尾下标）换成新位置。数组里重复值各占一个位置，所以被抽中的概率与出现次数成正比：

```python
import random
from collections import defaultdict


class RandomizedCollection:
    def __init__(self) -> None:
        self.items: list[int] = []
        self.pos: defaultdict[int, set[int]] = defaultdict(set)   # 值 -> 它出现的所有下标

    def insert(self, val: int) -> bool:
        self.pos[val].add(len(self.items))
        self.items.append(val)
        return len(self.pos[val]) == 1

    def remove(self, val: int) -> bool:
        if not self.pos[val]:
            return False
        i = self.pos[val].pop()
        last = self.items.pop()
        if i < len(self.items):
            self.items[i] = last
            self.pos[last].remove(len(self.items))
            self.pos[last].add(i)
        return True

    def getRandom(self) -> int:
        return random.choice(self.items)
```

2. **带权重**：`getRandom` 要按权重抽样。用前缀和数组加 `bisect`（`random.random() * 总权重` 落在哪个区间），`O(log n)`；元素会增删时，用树状数组（Fenwick tree）维护前缀和，增删改都是 `O(log n)`。
3. **多线程**：`insert` / `remove` 要同时改 `items` 与 `pos`，中间状态下两者不一致；用一把锁包住整个操作。读多写少时可以用读写锁，`getRandom` 只读。

**Python 提醒**：`random.choice(set)` 抛 `TypeError: 'set' object is not subscriptable`；`random.sample(set, k)` 在 Python 3.11 起也抛 `TypeError`（`Population must be a sequence`）；要从集合里抽元素就先转成列表，或者像本解法一样一开始就用列表存。
