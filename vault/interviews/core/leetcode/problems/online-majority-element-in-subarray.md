---
slug: online-majority-element-in-subarray
---
## Q
**LC 1157 子数组中占绝大多数的元素**｜Hard

设计 `MajorityChecker(arr)`，`query(left, right, threshold)` 返回 `arr[left..right]` 中出现至少 `threshold` 次的元素，没有返回 `-1`；保证 `2·threshold > 区间长度`。

## A
**一句话。** 绝对众数可以用摩尔投票求候选，而投票结果能两段合并，所以线段树每个结点存 `(候选, 净票数)`；查询得到候选后，再用它的下标列表二分数出真实次数。

```python
class MajorityChecker:
    def __init__(self, arr):
        self.n = n = len(arr)
        self.pos = defaultdict(list)   # 值 -> 下标列表
        for i, x in enumerate(arr):
            self.pos[x].append(i)
        self.t = [(0, 0)] * (4 * n)    # (候选, 净票数)
        self.build(arr, 1, 0, n - 1)

    def merge(self, a, b):     # 摩尔投票：不同的两两抵消
        if a[0] == b[0]:
            return (a[0], a[1] + b[1])
        if a[1] >= b[1]:
            return (a[0], a[1] - b[1])
        return (b[0], b[1] - a[1])

    def build(self, arr, o, l, r):
        if l == r:
            self.t[o] = (arr[l], 1)
            return
        m = (l + r) // 2
        self.build(arr, 2 * o, l, m)
        self.build(arr, 2 * o + 1, m + 1, r)
        self.t[o] = self.merge(self.t[2 * o],
                               self.t[2 * o + 1])

    def ask(self, o, l, r, L, R):
        if L <= l and r <= R:
            return self.t[o]
        m = (l + r) // 2
        res = (0, 0)
        if L <= m:
            res = self.ask(2 * o, l, m, L, R)
        if R > m:
            right = self.ask(2 * o + 1, m + 1, r, L, R)
            res = self.merge(res, right)
        return res

    def query(self, left, right, threshold):
        x, _ = self.ask(1, 0, self.n - 1, left, right)
        p = self.pos[x]        # 候选不一定是众数，要验证
        cnt = bisect_right(p, right) - bisect_left(p, left)
        return x if cnt >= threshold else -1
```

**复杂度。** 建树 `O(n)`，每次查询 `O(log n)`，空间 `O(n)`。

**易错点。**
- 直接返回投票候选：区间里没有绝对众数时候选是随便剩下的，必须数一遍。
- 用计数前缀和统计次数：值域 `2·10^4` 乘长度 `2·10^4` 存不下，用下标列表加二分。

**追问。**
- 随机化做法？：在区间里随机抽 20 次，抽中众数的概率每次超过 1/2，失败概率约 `2^{-20}`。
- 为什么投票能合并？：两段各自抵消后剩下的票，合在一起再抵消，等价于整段一起投票。

**同模式。** LC 169 多数元素、LC 229 多数元素 II、LC 307 区域和检索 - 数组可修改
