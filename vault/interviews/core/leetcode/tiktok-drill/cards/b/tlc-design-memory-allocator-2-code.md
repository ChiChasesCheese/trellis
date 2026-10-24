---
id: tlc-design-memory-allocator-2-code
node: b.design-memory-allocator
type: qa
step: 2
---
## Q
**LC 2502 设计内存分配器**｜写出 Python 实现

实现 `Allocator(n)`：`allocate(size, mID)` 在大小为 `n` 的内存数组里找最左侧的连续 `size` 个空闲单元，分配给 `mID` 并返回起始下标（没有则 `-1`）；`freeMemory(mID)` 释放 `mID` 的全部单元（可能分散在多个块里）并返回个数。`n, size, mID` 都在 `1..1000`，调用不超过 `1000` 次。

## A
**思路。** 用一个长度为 `n` 的列表 `mem` 表示内存，`0` 代表空闲，其他值是占用它的 `mID`。分配时顺序扫描，遇到空闲就让连续空闲数加一，遇到占用就清零，数到 `size` 的那一刻块的起点就是 `i - size + 1`，用切片一次性写入 `mID`；扫描完也没凑够就返回 `-1`。释放时扫描整个数组，把等于 `mID` 的单元清零并计数。

```python
class Allocator:
    def __init__(self, n: int) -> None:
        self.mem = [0] * n             # mem[i] 是占用该单元的 mID；mID >= 1，所以 0 表示空闲

    def allocate(self, size: int, mID: int) -> int:
        run = 0                        # 当前连续空闲单元的个数
        for i, owner in enumerate(self.mem):
            run = run + 1 if owner == 0 else 0
            if run == size:            # 第一次凑够 size 个，就是最左侧的块
                start = i - size + 1
                self.mem[start:i + 1] = [mID] * size   # 切片赋值，一次写入整块
                return start
        return -1

    def freeMemory(self, mID: int) -> int:
        freed = 0
        for i, owner in enumerate(self.mem):
            if owner == mID:           # 同一个 mID 可能分散在多个块里，全部释放
                self.mem[i] = 0
                freed += 1
        return freed
```

运行：`示例的 11 个调用` → `[None, 0, 1, 2, 1, 3, 1, 6, 3, -1, 0]`，`n=5：同一 mID 分到两个块，再一次性释放` → `[None, 0, 2, 3, 4]`，`n=1000 一次占满，再分配 1 个` → `[None, 0, -1]`。

**复杂度。** `allocate` 与 `freeMemory` 都是 `O(n)`：一遍扫描整个数组；`1000` 次调用总计约 `10^6` 次单元访问。空间 `O(n)`。

**写法要点。** `run = run + 1 if owner == 0 else 0` 一行完成「累加或清零」；`enumerate(self.mem)` 同时拿下标和值；切片赋值 `self.mem[start:i + 1] = [mID] * size` 一次写入一整块，长度必须和切片长度相等才不会改变列表长度；`mID >= 1` 的前提使得 `0` 可以做空闲标记，若 `mID` 可能为 `0`，要改用 `None`；方法名沿用题目的 `freeMemory`。
