---
id: tlc-patterns-design-2-randomized-set
node: patterns.design
type: qa
step: 2
---
## Q
**数据结构设计题｜O(1) 插入、删除、随机取：RandomizedSet（LC 380）**

哈希表能 `O(1)` 查找但不能随机取；数组能随机取但删除是 `O(n)`。怎样把两者结合？

## A
数组 `vals` 存元素（负责 `O(1)` 随机取），字典 `pos` 存"值 → 下标"（负责 `O(1)` 查找）。删除用**交换删除**：把要删的位置用最后一个元素覆盖，再弹出末尾。

```python
import random
class RandomizedSet:
    def __init__(self) -> None:
        self.vals: list[int] = []
        self.pos: dict[int, int] = {}

    def insert(self, val: int) -> bool:
        if val in self.pos:
            return False
        self.pos[val] = len(self.vals)
        self.vals.append(val)
        return True

    def remove(self, val: int) -> bool:
        if val not in self.pos:
            return False
        i, last = self.pos[val], self.vals[-1]
        self.vals[i] = last                # 用最后一个元素覆盖要删的位置
        self.pos[last] = i                 # 更新被移动元素的下标
        self.vals.pop()
        del self.pos[val]                  # 先更新 pos[last] 再删除 val：val 就是 last 时也正确
        return True

    def getRandom(self) -> int:
        return random.choice(self.vals)

rs = RandomizedSet()
print(rs.insert(1), rs.remove(2), rs.insert(2), rs.remove(1), rs.insert(2))   # True False True True False
```

- 所有操作平均 `O(1)`；`random.choice(list)` 等概率，`5` 个元素各取 `50000` 次，每个都在 `9000` 到 `11000` 之间。
- 交换删除的顺序：先 `vals[i] = last`、`pos[last] = i`，再 `pop` 与 `del pos[val]`。当 `val` 恰好是最后一个元素时，`i` 指向末尾，覆盖自己，`pos[last] = i` 不变，最后 `del pos[val]` 删掉它——也正确。
- 若允许重复元素（LC 381），`pos` 要存下标集合。
- 数组里的顺序不重要，这是交换删除成立的前提。
