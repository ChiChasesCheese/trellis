---
slug: insert-delete-getrandom-o1
---
## Q
**LC 380 O(1) 时间插入、删除和获取随机元素**｜Medium

实现 `RandomizedSet`：`insert(val)`、`remove(val)`、`getRandom()`（等概率返回现有元素），平均都要 `O(1)`。

## A
**一句话。** 数组存元素以便随机取，字典存值到下标；删除时用末尾元素填坑，数组保持紧凑。

```python
class RandomizedSet:
    def __init__(self):
        self.items = []
        self.pos = {}            # 值 -> 在 items 里的下标

    def insert(self, val):
        if val in self.pos:
            return False
        self.pos[val] = len(self.items)
        self.items.append(val)
        return True

    def remove(self, val):
        if val not in self.pos:
            return False
        i = self.pos.pop(val)
        last = self.items.pop()  # 先弹出末尾
        if i < len(self.items):  # val 不在末尾才需要填坑
            self.items[i] = last
            self.pos[last] = i
        return True

    def getRandom(self):
        return random.choice(self.items)
```

**复杂度。** 时间 均摊 `O(1)`，空间 `O(n)`。

**易错点。**
- 不判断被删元素是否在末尾：`insert(1)`、`insert(2)`、`remove(2)` 抛 `IndexError`，要判 `i < len(items)`。
- 搬了末尾元素却没更新 `pos[last]`：之后删它会删错位置。
- 用 `set` 存元素：`random.choice(set)` 抛 `TypeError`，转 `list` 又是 `O(n)`。

**追问。**
- 允许重复元素（LC 381）？：字典改成值到下标集合，搬末尾元素时换掉集合里的旧下标。
- 按权重随机（LC 528）？：前缀和加 `bisect`，`getRandom` 为 `O(log n)`。

**同模式。** LC 381 O(1) 时间插入、删除和获取随机元素 II、LC 146 LRU 缓存、LC 432 全 O(1) 的数据结构、LC 528 按权重随机选择
