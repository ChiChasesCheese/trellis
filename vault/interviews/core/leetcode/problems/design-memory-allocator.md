---
slug: design-memory-allocator
---
## Q
**LC 2502 设计内存分配器**｜Medium

设计大小为 `n` 的内存：`allocate(size, mID)` 在最左侧分配 `size` 个连续空闲单元并返回起点（没有返回 `-1`）；`freeMemory(mID)` 释放该 id 的所有单元并返回个数。

## A
**一句话。** 用数组直接模拟（simulation）：`0` 表示空闲，分配时扫描连续空闲长度，首次达到 `size` 即最左。

```python
class Allocator:
    def __init__(self, n):
        self.mem = [0] * n      # mID >= 1，0 表示空闲

    def allocate(self, size, mID):
        run = 0                 # 当前连续空闲长度
        for i, owner in enumerate(self.mem):
            run = run + 1 if owner == 0 else 0
            if run == size:     # 首次凑够就是最左
                start = i - size + 1
                self.mem[start:i + 1] = [mID] * size
                return start
        return -1

    def freeMemory(self, mID):
        freed = 0
        for i, owner in enumerate(self.mem):
            if owner == mID:    # 同 id 可能分散在多块
                self.mem[i] = 0
                freed += 1
        return freed
```

**复杂度。** 时间 每次操作 `O(n)`，空间 `O(n)`。

**易错点。**
- 只释放第一块：`allocate(1,1)、(1,2)、(1,1)` 后 `freeMemory(1)` 应返回 `2`。
- 起点写成 `i - size`：`i` 是块末尾，起点是 `i - size + 1`。
- 遇到占用单元不清零 `run`：会把被隔开的两段空闲拼成一段。

**追问。**
- `n` 到 `10^9` 怎么办？：按起点排序的区间表，扫相邻块的空隙，复杂度与 `n` 无关。
- 调用很多要 `O(log n)`？：线段树维护最长连续空闲段，在树上找最左满足的位置。

**同模式。** LC 2276 统计区间中的整数数目、LC 715 Range 模块、LC 731 我的日程安排表 II、LC 146 LRU 缓存
