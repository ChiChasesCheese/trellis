---
slug: finding-mk-average
---
## Q
**LC 1825 求出 MK 平均值**｜Hard

数据流，给定 `m`、`k`。`addElement(num)` 加入一个数；`calculateMKAverage()`：不足 `m` 个返回 `-1`；否则取最近 `m` 个数，去掉最小的 `k` 个和最大的 `k` 个，返回剩余数的平均值（向下取整）。`num ≤ 10^5`。

## A
**一句话。** 对窗口里的值建"按值下标的树状数组"，同时存个数和总和；用树状数组上二分求最小 `j` 个数的和，中间和 = 最小 `m-k` 个之和 - 最小 `k` 个之和。

```python
N = 100000

class MKAverage:
    def __init__(self, m, k):
        self.m, self.k = m, k
        self.q = deque()
        self.cnt = [0] * (N + 1)
        self.sm = [0] * (N + 1)

    def _add(self, v, d):                 # d = +1 加入，-1 移出
        i = v
        while i <= N:
            self.cnt[i] += d
            self.sm[i] += d * v
            i += i & -i

    def _smallest(self, j):               # 最小 j 个数的和
        pos = tot = 0
        for b in range(16, -1, -1):
            nxt = pos + (1 << b)
            if nxt <= N and self.cnt[nxt] <= j:
                pos = nxt
                j -= self.cnt[nxt]
                tot += self.sm[nxt]
        return tot + j * (pos + 1)        # 剩下 j 个都等于 pos+1

    def addElement(self, num):
        self.q.append(num)
        self._add(num, 1)
        if len(self.q) > self.m:
            self._add(self.q.popleft(), -1)

    def calculateMKAverage(self):
        if len(self.q) < self.m:
            return -1
        m, k = self.m, self.k
        mid = self._smallest(m - k) - self._smallest(k)
        return mid // (m - 2 * k)
```

**复杂度。** 加入 `O(log N)`，查询 `O(log N)`，空间 `O(N + m)`。

**易错点。**
- 二分后忘了补尾巴：第 `j` 小的值可能有多个，余下的 `j` 个都取 `pos + 1`。
- 窗口超过 `m` 才移出旧元素：不足 `m` 时不能弹。
- 用排序列表每次重排：`O(m log m)` 每次查询会超时。

**追问。**
- 不用树状数组还能怎么做？：三个有序容器（最小 `k`、中间、最大 `k`），每次插入删除后搬动边界元素。

**同模式。** LC 295 数据流的中位数、LC 239 滑动窗口最大值、LC 480 滑动窗口中位数
