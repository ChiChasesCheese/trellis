---
id: tlc-tt-percentile-finder-4-followup
node: b.tt-percentile-finder
type: qa
step: 4
---
## Q
**PercentileFinder：实时维护数字并返回第 p 百分位**｜追问

面试官接着问：除了 `bisect` 的有序列表，还可以用什么数据结构优化？分别在什么场景下更好？

## A
1. **值域有界（如 `0..V`）**：用 Fenwick 树记录每个值的出现次数，加入 `O(log V)`，按秩找第 `k` 小也是 `O(log V)`，与数据个数 `N` 无关。

```python
class BoundedPercentile:
    def __init__(self, max_value: int) -> None:
        self._n = max_value + 1                    # 值域 [0, max_value]
        self._tree = [0] * (self._n + 1)           # Fenwick 树：每个值出现的次数
        self._count = 0

    def add(self, x: int) -> None:
        self._count += 1
        i = x + 1
        while i <= self._n:
            self._tree[i] += 1
            i += i & -i

    def kth(self, k: int) -> int:                  # 第 k 小（从 1 开始）
        pos, step = 0, 1 << self._n.bit_length()
        while step:                                # 倍增下降：找前缀和仍 < k 的最大位置
            nxt = pos + step
            if nxt <= self._n and self._tree[nxt] < k:
                pos = nxt
                k -= self._tree[nxt]
            step >>= 1
        return pos                                 # 树下标 pos + 1 对应的值是 pos

    def find_percentile(self, p: int) -> int:
        return self.kth(max(1, -(-p * self._count // 100)))
```

加入 `15,20,35,40,50` 后（值域 `0..100`），`p = 0, 5, 30, 40, 50, 100` → `[15, 15, 20, 20, 35, 50]`。
2. **`p` 固定**：两个堆，最大堆存最小的 `k` 个，最小堆存其余，`k = ceil(p * N / 100)` 随 `N` 增长而调整，插入 `O(log N)`，查询 `O(1)` 读堆顶。`p` 经常变时不合适。
3. **任意 `p`、数据量大、值域无界**：平衡二叉搜索树 / 顺序统计树（每个节点存子树大小）或跳表，插入和按秩查询都是 `O(log N)`；Python 里常用第三方 `sortedcontainers.SortedList`，它是分块的有序列表，实际很快。
4. **允许近似**：t-digest、GK 摘要，内存与误差参数成正比，与 `N` 无关，适合监控类场景。

**Python 提醒**：`list.insert` 是 `O(N)` 的平移，所以 `bisect.insort` 的总成本不是 `O(log N)`；平移用 `memmove` 完成，常数很小，数据量不大时足够；数据量很大或插入非常频繁时要换结构。`bisect` 只在列表已排序时才正确，它不会检查。
