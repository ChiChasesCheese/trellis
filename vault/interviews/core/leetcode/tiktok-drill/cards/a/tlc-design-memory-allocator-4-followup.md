---
id: tlc-design-memory-allocator-4-followup
node: a.design-memory-allocator
type: qa
step: 4
---
## Q
**LC 2502 设计内存分配器**｜追问

面试官接着问：（1）`n` 是 `10^9`，数组放不下？（2）调用次数是 `10^5`，`O(n)` 每次太慢？（3）要不要合并相邻的空闲块、做碎片整理？

## A
1. **`n` 很大**：不存数组，存已分配的区间，按起点排序的 `(起点, 终点, mID)` 列表：

```python
class IntervalAllocator:
    def __init__(self, n: int) -> None:
        self.n = n
        self.blocks: list[tuple[int, int, int]] = []   # (起点, 终点（开）, mID)，按起点排序

    def allocate(self, size: int, mID: int) -> int:
        prev_end = 0
        for idx, (start, end, _) in enumerate(self.blocks):
            if start - prev_end >= size:               # 两个已分配块之间的空隙够用
                self.blocks.insert(idx, (prev_end, prev_end + size, mID))
                return prev_end
            prev_end = end
        if self.n - prev_end >= size:                  # 最后一块之后
            self.blocks.append((prev_end, prev_end + size, mID))
            return prev_end
        return -1

    def freeMemory(self, mID: int) -> int:
        freed = sum(end - start for start, end, m in self.blocks if m == mID)
        self.blocks = [b for b in self.blocks if b[2] != mID]
        return freed
```

`allocate` 依次看相邻块之间的空隙（含第一块之前和最后一块之后），第一个够大的就是最左；`freeMemory` 过滤掉 `mID` 的块。每次操作 `O(块数)`，与 `n` 无关。
2. **调用很多**：用线段树维护每段的「最长连续空闲、前缀空闲、后缀空闲」，`allocate` 在树上下降找最左的位置，`O(log n)`；释放需要 `mID -> 块列表` 的字典，对每个块区间更新。
3. **合并 / 整理**：区间表里空闲段是隐含的（块之间的空隙），天然是合并的；碎片整理 = 把所有块依次左移挤到一起，`O(块数)`，但会改变地址，现实中要谨慎。

**Python 提醒**：`self.mem[start:i + 1] = [mID] * size` 切片赋值要求右侧长度与切片长度一致，否则列表会变长或变短；在循环里直接 `self.blocks.insert(idx, ...)` 之后立刻 `return` 是安全的，若继续遍历则会被修改中的列表干扰。
