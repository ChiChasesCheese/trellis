---
slug: tt-contiguous-memory-allocator
---
## Q
**连续内存分配器**｜Medium

管理 `[0, capacity)` 的分配器：`alloc(size)` 用 first-fit 返回起始地址（`size` 非法抛 `ValueError`，放不下返回 `-1`）；`free(addr)` 释放并与相邻空闲块合并（double free 抛 `ValueError`）；可选 `alignment`，返回地址须是其倍数。

## A
**一句话。** 按地址排序的空闲块列表加 `used` 字典：`alloc` 取第一个对齐后放得下的块并切分，`free` 二分定位后与左右邻居合并。

```python
class Allocator:
    def __init__(self, capacity, alignment=1):
        self.cap, self.align = capacity, alignment
        self.fl = [(0, capacity)]   # 按地址排序，互不相邻
        self.used = {}                     # 起始地址 -> 大小

    def alloc(self, size):
        if size <= 0 or size > self.cap:
            raise ValueError("illegal size")
        for idx, (start, length) in enumerate(self.fl):
            al = self.align
            addr = -(-start // al) * al      # 向上对齐
            pad = addr - start             # 对齐空隙，仍然空闲
            if length >= pad + size:
                tail = length - pad - size
                new = []
                if pad:
                    new.append((start, pad))
                if tail:
                    new.append((addr + size, tail))
                self.fl[idx:idx + 1] = new
                self.used[addr] = size
                return addr
        return -1

    def free(self, addr):
        if addr not in self.used:
            raise ValueError("invalid or double free")
        size = self.used.pop(addr)
        fl = self.fl
        idx = bisect_left(fl, (addr, 0))   # 按地址找插入位置
        start, length = addr, size
        if idx < len(fl) and fl[idx][0] == addr + size:
            length += fl.pop(idx)[1]       # 合并右邻
        if idx:
            ls, ll = fl[idx - 1]
            if ls + ll == addr:            # 合并左邻
                fl.pop(idx - 1)
                start, idx = ls, idx - 1
                length += ll
        fl.insert(idx, (start, length))
```

**复杂度。** `alloc` `O(F)`，`free` `O(F)`（`F` 为空闲块数），空间 `O(F + 已分配块数)`。

**易错点。**
- 释放只合并右邻居：`capacity = 10`，`alloc` 三次得 `0, 3, 7`，`free(0)`、`free(3)` 后应有块 `(0, 7)`，漏合并时 `alloc(7)` 返回 `-1`。
- 不登记已分配块：同一地址释放两次，空闲列表出现重叠区间，同一块内存分给两人。
- 对齐向下取整：`Allocator(32, 8)` 先 `alloc(3)` 得 `0`，再 `alloc(1)` 返回 `0`（重叠），应为 `8`。
- 丢掉对齐空隙 `pad`：它仍是空闲的，要留在列表里。

**追问。**
- `realloc(addr, new_size)`？：看后面紧挨的空闲块够不够扩，够就原地扩，不够就 `alloc` 新块、拷贝、`free` 旧块。
- 换策略？：best-fit 选最小够用块，worst-fit 选最大块；伙伴系统按 2 的幂对齐，合并只看伙伴。

**同模式。** LC 2502 设计内存分配器、LC 146 LRU 缓存、LC 705 设计哈希集合、LC 981 基于时间的键值存储
