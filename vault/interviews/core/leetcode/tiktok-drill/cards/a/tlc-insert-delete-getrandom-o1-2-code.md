---
id: tlc-insert-delete-getrandom-o1-2-code
node: a.insert-delete-getrandom-o1
type: qa
step: 2
---
## Q
**LC 380 O(1) 时间插入、删除和获取随机元素**｜写出 Python 实现

实现类 `RandomizedSet`：`insert(val)` 在 `val` 不存在时插入并返回 `True`，否则 `False`；`remove(val)` 在 `val` 存在时删除并返回 `True`，否则 `False`；`getRandom()` 等概率返回现有的一个元素。三个操作平均 `O(1)`；`val` 是 `int32` 范围内的整数，操作最多 `2 * 10^5` 次。

## A
**思路。** `items` 数组存元素，`pos` 字典存值到下标的映射。删除时先弹出数组末尾；如果被删元素不是末尾，就把弹出的末尾元素放进被删位置，并更新字典。

```python
import random


class RandomizedSet:
    def __init__(self) -> None:
        self.items: list[int] = []         # 紧凑数组：getRandom 按下标 O(1) 取
        self.pos: dict[int, int] = {}      # 值 -> 它在 items 里的下标

    def insert(self, val: int) -> bool:
        if val in self.pos:
            return False
        self.pos[val] = len(self.items)
        self.items.append(val)
        return True

    def remove(self, val: int) -> bool:
        if (i := self.pos.pop(val, None)) is None:
            return False
        last = self.items.pop()            # 先弹出末尾，数组保持紧凑
        if i < len(self.items):            # val 不在末尾：把 last 填进空出的 i
            self.items[i] = last
            self.pos[last] = i
        return True

    def getRandom(self) -> int:
        return random.choice(self.items)
```

运行：示例序列依次得到 `True, False, True, True, True, False, 2`（其中 `getRandom` 在 `{1, 2}` 里取）；依次插入 `10, 20, 30, 40` 再删 `20` 后 `items = [10, 40, 30]`，`pos = {10: 0, 30: 2, 40: 1}`。

**复杂度。** 三个操作均摊 `O(1)`；空间 `O(n)`。

**写法要点。** `self.pos.pop(val, None)` 一次完成「是否存在 + 取下标 + 删除」，配合海象运算符 `:=` 少写一次查找，`is None` 而不是 `not i`（下标 `0` 也是合法的）。`random.choice(seq)` 对列表是 `O(1)`，对 `set` / `dict` 不可用。先 `pop()` 再比较 `i < len(self.items)`，一并处理「被删的正是末尾」。`getRandom` 的方法名保持题目给的驼峰写法。
