---
id: tlc-patterns-design-7-allocator
node: patterns.design
type: qa
step: 7
---
## Q
**数据结构设计题｜内存分配器（LC 2502）：规模小时直接模拟**

找最左侧连续 `size` 个空闲单元、按 id 释放，怎样选数据结构？什么时候朴素扫描就够？

## A
先看规模：`n`、`size`、`mID` 和调用次数都 `<= 1000`。每次 `O(n)` 的扫描总共约 `10^6`，Python 毫秒级。**别为不需要的性能复杂化**。

```python
class Allocator:
    def __init__(self, n: int) -> None:
        self.mem = [0] * n                 # 0 表示空闲，否则是 mID（mID >= 1）

    def allocate(self, size: int, mID: int) -> int:
        run = 0
        for i, owner in enumerate(self.mem):
            run = run + 1 if owner == 0 else 0     # 当前连续空闲长度
            if run == size:
                start = i - size + 1
                self.mem[start:i + 1] = [mID] * size
                return start
        return -1

    def freeMemory(self, mID: int) -> int:
        freed = 0
        for i, owner in enumerate(self.mem):
            if owner == mID:
                self.mem[i] = 0
                freed += 1
        return freed

al = Allocator(10)
print([al.allocate(1, 1), al.allocate(1, 2), al.allocate(1, 3), al.freeMemory(2), al.allocate(3, 4),
       al.allocate(1, 1), al.allocate(1, 1), al.freeMemory(1), al.allocate(10, 2), al.freeMemory(7)])
# [0, 1, 2, 1, 3, 1, 6, 3, -1, 0]
```

- 一次扫描就能找到"最左侧"：第一次连续空闲长度达到 `size` 的位置，起点是 `i - size + 1`。
- `mem[a:b] = [mID] * size` 用切片赋值一次填写。
- 若规模放大（`n = 10^5`、调用 `10^5` 次）：改成**有序的空闲区间表**（`SortedList` 或堆）+ 每个 `mID` 已分配区间的字典；分配时找第一个足够大的空闲区间，释放时合并相邻空闲区间。
- 回答顺序：先说朴素解和复杂度，再主动说"如果规模更大我会这样改"，比一开始就写复杂结构更稳。
