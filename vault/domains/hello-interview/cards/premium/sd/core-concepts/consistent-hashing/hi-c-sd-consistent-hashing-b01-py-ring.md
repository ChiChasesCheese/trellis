---
id: hi-c-sd-consistent-hashing-b01-py-ring
node: sd.core-concepts.consistent-hashing.beyond
type: qa
step: 1
---
## Q
**一致性哈希 · 用 Python 实现哈希环**｜拓展 · 加分
用 Python 写一个带虚拟节点的哈希环，查找为什么要用二分？虚拟节点数对均匀度和迁移量的影响实测如何？

## A
**模式。** 有序数组加二分的环查找。
```python
import bisect
import hashlib
from typing import List, Tuple


def _h(s: str) -> int:
    # 稳定哈希（不能用内置 hash，它每个进程随机加盐）
    return int.from_bytes(hashlib.md5(s.encode()).digest()[:4], "big")


class Ring:
    def __init__(self, nodes: List[str], vnodes: int = 100) -> None:
        self._vnodes = vnodes
        self._points: List[Tuple[int, str]] = []     # 按哈希值有序
        for n in nodes:
            self.add(n)

    def add(self, node: str) -> None:
        for i in range(self._vnodes):
            bisect.insort(self._points, (_h(f"{node}#{i}"), node))

    def remove(self, node: str) -> None:
        self._points = [p for p in self._points if p[1] != node]

    def get(self, key: str) -> str:
        # 顺时针第一个 >= 键哈希的点；越界则用取模绕回起点，这就是"环"
        i = bisect.bisect_left(self._points, (_h(key), ""))
        return self._points[i % len(self._points)][1]
```
- **为什么二分：** 点按哈希有序，查找是 O(log N)；线性扫描随虚拟节点总数变慢。
- **实测（4 台机器，2 万个键，再加第 5 台）：** 每机 1 个点时各机负载差很大（267 到 11106 个键）；每机 100 个点时在 4789 到 5140 之间，均匀得多。加第 5 台后移动约 17% 到 20% 的键，理论值 20%；取模扩容则移动约 80%。
- **插入代价：** `insort` 是 O(N) 的数组搬移，增减节点不频繁，所以可以接受；高频场景可用平衡树。
- **并发：** 实际使用时通常整体替换一份不可变快照，读取不加锁。
