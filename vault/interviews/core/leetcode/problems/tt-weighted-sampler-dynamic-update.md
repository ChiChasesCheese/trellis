---
slug: tt-weighted-sampler-dynamic-update
---
## Q
**按权重采样器（支持动态修改权重）**｜Medium

`Sampler(weights)`：`sample()` 按权重比例随机返回下标（权重 `0` 永不选中）。追问：支持 `update(i, weight)` 修改权重，`update` 和 `sample` 都要 `O(log n)`。构造函数可接收 `random.Random` 以便测试。例：权重 `[1,3,0,6]`，随机整数 `r` 取 `0..9` 落在下标 `[0,1,1,1,3,3,3,3,3,3]`。

## A
**一句话。** 前缀和把 `[0, total)` 切成正比于权重的区间（LC 528 用 `bisect_right`），权重会变就换成 Fenwick 树（树状数组），`sample` 倍增下降找第一个前缀和大于 `r` 的下标。

```python
class DynamicSampler:
    def __init__(self, weights, rng=None):
        self.n = len(weights)
        self.w = list(weights)
        self.rng = rng or random.Random()
        self.tree = [0] + self.w     # Fenwick 树，下标从 1 开始
        for i in range(1, self.n + 1):   # 线性建树
            j = i + (i & -i)             # 父节点
            if j <= self.n:
                self.tree[j] += self.tree[i]
        self.total = sum(self.w)

    def update(self, i, weight):
        delta, self.w[i] = weight - self.w[i], weight
        self.total += delta
        i += 1
        while i <= self.n:      # 增量加到所有覆盖 i 的节点
            self.tree[i] += delta
            i += i & -i

    def sample(self):
        return self.locate(self.rng.randrange(self.total))

    def locate(self, r):
        # 最小下标 i，使前缀和 w[0..i] > r
        pos = 0
        step = 1 << self.n.bit_length()
        while step:             # 倍增下降，从高位往右跨
            nxt = pos + step
            if nxt <= self.n and self.tree[nxt] <= r:
                pos = nxt
                r -= self.tree[nxt]
            step >>= 1
        return pos      # 前 pos 个的和 <= r，答案是 0-based 的 pos
```

**复杂度。** 时间 `update` 与 `sample` 均 `O(log n)`，空间 `O(n)`。

**易错点。**
- 区间边界错一位：要找前缀和 `> r` 的第一个位置，静态版用 `bisect_left` 代替 `bisect_right`，`[1,3,0,6]` 的 `r = 1` 落到下标 `0`，应为 `1`。
- 随机数用 `randint(0, total)`：两端都含，多出一个值 `total`，下标越界。
- 总权重为 `0`：`randrange(0)` 抛 `ValueError`，构造时就要拒绝。
- 更新增量没用当前值算：要另存一份权重数组 `w`。

**追问。**
- 权重不变时用什么？：`accumulate` 前缀和加 `bisect_right(prefix, r)`，采样 `O(log n)`。
- 要 `O(1)` 采样？：别名法（alias method）预处理 `O(n)`，但不支持动态更新。

**同模式。** LC 528 按权重随机选择、LC 497 非重叠矩形中的随机点、LC 398 随机数索引、LC 307 区域和检索 - 数组可修改
