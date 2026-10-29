---
id: tlc-tt-contiguous-memory-allocator-2-code
node: b.tt-contiguous-memory-allocator
type: qa
step: 2
---
## Q
**连续内存分配器**｜写出 Python 实现

写类 `Allocator(capacity, alignment=1)` 管理地址 `[0, capacity)`（`1 <= capacity <= 10^9`）：`alloc(size)` first-fit 分配，返回起始地址（是 `alignment` 的倍数），`size <= 0` 或 `size > capacity` 抛 `ValueError`，放不下返回 `-1`；`free(addr)` 释放该次分配并与相邻空闲块合并，对未分配或已释放的地址抛 `ValueError`。

## A
**思路。** `free_list` 是按起始地址排序、互不相邻的空闲块 `(start, size)`，`used` 记录已分配块。分配时向上对齐，把块拆成「对齐空隙、已分配、剩余」三部分，空隙和剩余仍是空闲块。释放时用 `bisect_left` 找到插入位置，检查右、左邻居是否紧挨，紧挨就合并。

```python
from bisect import bisect_left


class Allocator:
    def __init__(self, capacity: int, alignment: int = 1) -> None:
        self.capacity, self.align = capacity, alignment
        self.free_list: list[tuple[int, int]] = [(0, capacity)]   # 按起始地址排序的空闲块 (start, size)，互不相邻
        self.used: dict[int, int] = {}                             # 已分配块：起始地址 -> 大小

    def alloc(self, size: int) -> int:
        if size <= 0 or size > self.capacity:
            raise ValueError(f"illegal size {size}")
        for idx, (start, length) in enumerate(self.free_list):    # first-fit：地址最小且放得下的空闲块
            addr = -(-start // self.align) * self.align            # 向上对齐到 align 的倍数
            pad = addr - start                                     # 块首被对齐跳过的空隙，仍然空闲
            if length >= pad + size:
                tail = length - pad - size                         # 分配之后右边剩下的空闲部分
                pieces = ([(start, pad)] if pad else []) + ([(addr + size, tail)] if tail else [])
                self.free_list[idx:idx + 1] = pieces
                self.used[addr] = size
                return addr
        return -1                                                  # 没有足够大的连续空闲块

    def free(self, addr: int) -> None:
        if addr not in self.used:
            raise ValueError(f"invalid or double free at {addr}")  # 从未分配、已释放都在这里被拒绝
        size = self.used.pop(addr)
        free_list = self.free_list
        idx = bisect_left(free_list, (addr, 0))                    # 按地址找到插入位置
        start, length = addr, size
        if idx < len(free_list) and free_list[idx][0] == addr + size:       # 右邻居紧挨着：合并
            length += free_list.pop(idx)[1]
        if idx:
            left_start, left_len = free_list[idx - 1]
            if left_start + left_len == addr:                                # 左邻居的末尾正好是 addr：合并
                free_list.pop(idx - 1)
                start, length, idx = left_start, length + left_len, idx - 1
        free_list.insert(idx, (start, length))
```

运行：`Allocator(10)`：`alloc(3)`、`alloc(4)`、`alloc(2)` → `0, 3, 7`，`alloc(2)` → `-1`，空闲块 `[(9, 1)]`；`free(3)` 后 `[(3, 4), (9, 1)]`，`alloc(5)` → `-1`，`alloc(4)` → `3`；`free(0)`、`free(7)` 之后空闲块 `[(0, 3), (7, 3)]`；`free(0)` 再来一次与 `free(99)` 都抛 `ValueError`；`alloc(0)`、`alloc(-1)`、`alloc(11)` 抛 `ValueError`。`Allocator(32, 8)`：`alloc(3)`、`alloc(8)`、`alloc(1)` → `0, 8, 16`，空闲块 `[(3, 5), (17, 15)]`。

**复杂度。** `alloc` 为 `O(F)`；`free` 定位 `O(log F)`、列表插入删除 `O(F)`；`F` 为空闲块数。

**写法要点。**
- `-(-start // self.align) * self.align`：用负数的向下取整实现向上取整，不引入 `math.ceil` 和浮点。
- `bisect_left(free_list, (addr, 0))`：元组比较先看起始地址，在按地址有序的列表里直接定位插入位置。
- 切片赋值 `free_list[idx:idx + 1] = pieces`：用 `0` 到 `2` 个新块替换原来的一个块，列表自动伸缩，不用分情况 `pop`、`insert`。
- 用 `ValueError` 表示调用方的错误（非法大小、非法释放），用返回值 `-1` 表示正常的“没有足够空间”，两类情形分开处理。
