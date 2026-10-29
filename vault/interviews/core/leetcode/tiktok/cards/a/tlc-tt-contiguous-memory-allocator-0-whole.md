---
id: tlc-tt-contiguous-memory-allocator-0-whole
node: a.tt-contiguous-memory-allocator
type: qa
---
## Q
**连续内存分配器**｜Medium · 近一年被问：美国 2 次、国内 0 次 · 最近 2026-06-11（面试记录）

实现管理一段连续地址空间 `[0, capacity)` 的内存分配器。`alloc(size) -> int`：用 first-fit（最左能放下的空闲块）分配 `size` 个单元，返回起始地址；`size` 为 `0`、负数或大于 `capacity` 时抛 `ValueError`；没有足够大的连续空闲块返回 `-1`。`free(addr)`：释放以 `addr` 开头的那次分配，释放后要与相邻的空闲块合并（coalesce）；对已经释放或从未分配过的地址抛 `ValueError`（double free）。构造函数可选 `alignment`：返回的地址必须是它的倍数（默认 `1`）。`1 <= capacity <= 10^9`，最多 `10^5` 次操作。例：`capacity = 10`，依次 `alloc(3)`、`alloc(4)`、`alloc(2)` → `0, 3, 7`，再 `alloc(2)` → `-1`；`free(3)` 后 `alloc(5)` → `-1`（只有 `4` 个连续单元），`alloc(4)` → `3`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 维护一个按起始地址排序的空闲块列表 `free_list`（互不相邻）和一个 `used` 字典（起始地址 → 大小）。`alloc` 扫描空闲块，取第一个按对齐后放得下的，切掉前面对齐空隙、已分配部分和后面的剩余，剩余的仍留在空闲列表里；`free` 用二分按地址找到插入位置，与左右相邻的空闲块合并。

**识别。** 「first-fit、释放后合并相邻空闲块、检测 double free」是内存分配器的标准题（LC 2502 同型）。数据结构的选择取决于要支持的操作：按地址找邻居要有序，释放合并要能 `O(log n)` 定位，已分配块用字典 `O(1)` 校验合法性。

**推导。** 暴力：开一个长度为 `capacity` 的数组标记每个单元是否被占用，`alloc` 线性找连续的空闲段，`free` 清零，`O(capacity)` 每次，`10^9` 不可行。浪费：大段空闲或大段占用的区域逐格存储。洞察：只存空闲区间，数量远小于容量。`alloc` 一次扫描区间列表；`free` 时二分定位，只检查左右两个邻居是否紧挨着：紧挨就合并，列表始终保持“互不相邻”，下一次分配就不会遇到被切碎的空闲块。

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

运行：`Allocator(10)`，`alloc(3)`、`alloc(4)`、`alloc(2)` → `0, 3, 7`，再 `alloc(2)` → `-1`，此时空闲块 `[(9, 1)]`；`free(3)` 后空闲块 `[(3, 4), (9, 1)]`，`alloc(5)` → `-1`，`alloc(4)` → `3`；再 `free(0)`、`free(7)` 得到 `[(0, 3), (7, 3)]`（`7` 号块与 `(9, 1)` 合并）；对已释放的 `0` 或从未分配的 `99` 调用 `free` 抛 `ValueError`；`alloc(0)`、`alloc(-1)`、`alloc(11)` 抛 `ValueError`。`Allocator(32, 8)`：`alloc(3)`、`alloc(8)`、`alloc(1)` → `0, 8, 16`，空闲块 `[(3, 5), (17, 15)]`。

**复杂度。** `alloc` 为 `O(F)`（`F` 是空闲块数，第一个放得下的块就停）；`free` 为 `O(log F)` 定位加 `O(F)` 的列表插入或删除；空间 `O(F + 已分配块数)`。

**易错点。**
- 释放时只合并右邻居、漏掉左邻居：`capacity = 10`，`alloc(3)`、`alloc(4)`、`alloc(2)` 得到 `0, 3, 7`，依次 `free(0)`、`free(3)`，空闲块应是 `[(0, 7), (9, 1)]`，`alloc(7)` 返回 `0`；漏合并时空闲块是 `[(0, 3), (3, 4), (9, 1)]`，`alloc(7)` 返回 `-1`。
- 不登记已分配块，无法发现 double free：同一个地址释放两次，会往空闲列表里插入重叠的区间，之后的分配把同一块内存分给两个人。
- 对齐向下取整：`start // align * align` 会得到小于 `start` 的地址，落在别人的块里。`Allocator(32, 8)` 先 `alloc(3)` 得 `0`，再 `alloc(1)`，向下取整返回 `0`（与上一块重叠），正确是 `8`。
- 对齐空隙 `pad` 不能丢：它仍是空闲的，要作为独立的空闲块留在列表里。

**追问。**
- 地址对齐、非法释放检测：已包含在上面的 `alignment` 参数与 `used` 字典里。
- `realloc(addr, new_size)`：看地址后面紧挨着的空闲块够不够扩，够就原地扩；不够就 `alloc` 新块、拷贝、`free` 旧块。
- 线程安全：所有方法加同一把锁；吞吐不够再按大小分级（size class）拆成多个分配器。
- 换策略：best-fit 选最小的够用块，worst-fit 选最大的；伙伴系统（buddy system）把块按 `2` 的幂对齐，合并只看伙伴。

**同模式。** LC 2502 设计内存分配器、LC 146 LRU 缓存、LC 705 设计哈希集合、LC 981 基于时间的键值存储。
