---
slug: insert-delete-getrandom-o1-duplicates-allowed
---
## Q
**LC 381 O(1) 时间插入、删除和获取随机元素 - 允许重复**｜Hard

实现允许重复的集合：`insert(val)`、`remove(val)`（删一个）、`getRandom()`（概率正比于出现次数），平均 `O(1)`。

## A
**一句话。** 数组存全部元素便于随机抽，字典存「值 → 下标集合」；删除时与末尾元素互换后弹出末尾。

```python
class RandomizedCollection:
    def __init__(self):
        self.items = []               # 全部元素（含重复）
        self.pos = defaultdict(set)   # 值 -> 它的全部下标

    def insert(self, val):
        self.pos[val].add(len(self.items))
        self.items.append(val)
        return len(self.pos[val]) == 1  # 只有一个下标 = 新值

    def remove(self, val):
        if not self.pos.get(val):
            return False
        idx = self.pos[val].pop()
        last = len(self.items) - 1
        if idx != last:               # 用末尾覆盖 idx，不留空洞
            moved = self.items[last]
            self.items[idx] = moved
            self.pos[moved].remove(last)
            self.pos[moved].add(idx)  # moved 可能就是 val
        self.items.pop()
        if not self.pos[val]:
            del self.pos[val]         # 空集合要删键
        return True

    def getRandom(self):
        return random.choice(self.items)
```

**复杂度。** 三个操作均摊 `O(1)`，空间 `O(n)`。

**易错点。**
- `idx == last` 时不跳过互换：`pos[val]` 已弹出 `last`，再 `remove(last)` 抛 `KeyError`。
- 覆盖后不更新 `moved` 的下标集合：之后删 `moved` 会弹出过期下标。
- 集合删空后不删键：用 `val in self.pos` 判断存在会误判。

**追问。**
- 不允许重复（LC 380）？：下标集合退化为单个下标，字典存 `值 -> 下标`。
- 为什么用集合而不是列表存下标？：删除任意一个下标要 `O(1)`，列表按值删是 `O(n)`。

**同模式。** LC 380 O(1) 时间插入、删除和获取随机元素、LC 146 LRU 缓存、LC 460 LFU 缓存、LC 528 按权重随机选择
