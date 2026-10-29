---
id: tlc-tt-weighted-sampler-dynamic-update-0-whole
node: b.tt-weighted-sampler-dynamic-update
type: qa
---
## Q
**按权重采样器（支持动态修改权重）**｜Medium · TikTok 高频

写一个类 `Sampler`：给定 `n` 个非负整数权重 `w`（至少一个为正），`sample()` 按权重比例随机返回一个下标（下标 `i` 被选中的概率是 `w[i] / sum(w)`，权重为 `0` 的下标永远不会被选中）。追问：如果权重会动态修改（`update(i, weight)` 把第 `i` 个权重改成新值），前缀和每次更新要 `O(n)`，怎样让 `update` 和 `sample` 都是 `O(log n)`？`1 <= n <= 10^5`，`0 <= w[i] <= 10^6`，调用总数不超过 `10^5`。为了可测试，构造函数可接收一个 `random.Random`。例：权重 `[1,3,0,6]`，总和 `10`，随机整数 `r` 取 `0..9` 时分别落在下标 `[0,1,1,1,3,3,3,3,3,3]`；`update(2, 2)`、`update(0, 0)` 后权重是 `[0,3,2,6]`，`r` 取 `0..10` 时落在 `[1,1,1,2,2,3,3,3,3,3,3]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 主体就是 LC 528：权重的前缀和把 `[0, total)` 切成长度正比于权重的区间，取随机整数 `r`，用 `bisect_right` 找第一个前缀和大于 `r` 的下标，采样 `O(log n)`；追问权重会变时，把前缀和数组换成 Fenwick 树（树状数组），`update` 和 `sample` 都变成 `O(log n)`。

**识别。** 「按权重随机返回下标」就是前缀和加二分（逆变换采样），这是要写出来的主体；「权重会动态修改」是加在上面的追问，需要「单点更新 + 前缀和查询」的结构：Fenwick 树、线段树、平衡树，面试里能说清选择并写出 Fenwick 就够了。

**推导。** 暴力：每次 `sample` 线性扫描累加，`O(n)` → 前缀和只算一次，`r` 落在哪段用二分找，采样 `O(log n)` → 追问时的浪费：一次单点修改让后面所有前缀和都要重算，`O(n)` → 洞察：Fenwick 树节点 `i` 只负责 `(i - lowbit(i), i]` 这一段的和，单点更新只改 `O(log n)` 个节点；找「第一个前缀和大于 `r` 的位置」直接在树上倍增下降，一次 `O(log n)`。

```python
import random
from bisect import bisect_right
from itertools import accumulate


class Sampler:
    def __init__(self, weights: list[int], rng: random.Random | None = None) -> None:
        self._prefix = list(accumulate(weights))       # _prefix[i] = w[0] + ... + w[i]
        self._rng = rng or random.Random()              # 可注入，测试时传固定种子

    def sample(self) -> int:
        return self.locate(self._rng.randrange(self._prefix[-1]))   # r 在 [0, total) 均匀取整数

    def locate(self, r: int) -> int:
        return bisect_right(self._prefix, r)            # 第一个前缀和 > r 的下标
```

运行：权重 `[1,3,0,6]`，前缀和 `[1, 4, 4, 10]`，`locate(r)` 对 `r = 0..9` → `[0, 1, 1, 1, 3, 3, 3, 3, 3, 3]`；`Sampler([5]).locate(r)` 对 `r = 0..4` 全是 `0`；权重为 `0` 的下标 `2` 不会出现。

**复杂度。** 建前缀和 `O(n)`；`sample` 为 `O(log n)`；空间 `O(n)`。

**易错点。**
- 区间边界错一位：`r` 在 `[0, total)`，要找「前缀和 `> r`」的第一个位置。用 `bisect_left` 代替 `bisect_right`，`[1,3,0,6]` 的 `r = 1` 会落到下标 `0`（应为 `1`），下标 `0` 拿到 2 份、下标 `3` 只拿到 5 份，概率不对。
- 随机数用 `randint(0, total)`：两端都含，多出一个值 `total`，`bisect_right` 返回 `n`，下标越界。
- 总权重为 `0`：`randrange(0)` 抛 `ValueError`，构造时就要拒绝。

**追问。**
- 权重会动态修改：前缀和数组换成 Fenwick 树。`update` 算出增量，沿父链（`i += i & -i`）加到所有覆盖该位置的节点；`sample` 从高位到低位试着往右跨，跨过后前缀和仍 `<= r` 就跨，最后停下的位置就是答案。两者都 `O(log n)`；注意增量要用「当前值」算，所以要另存一份权重。

```python
class DynamicSampler:
    def __init__(self, weights: list[int], rng: random.Random | None = None) -> None:
        self._n = len(weights)
        self._w = list(weights)
        self._rng = rng or random.Random()
        self._tree = [0] + self._w                     # Fenwick 树（下标从 1 开始），线性建树
        for i in range(1, self._n + 1):
            j = i + (i & -i)                           # 父节点：把 i 的最低位 1 加回去
            if j <= self._n:
                self._tree[j] += self._tree[i]
        self._total = sum(self._w)

    def update(self, i: int, weight: int) -> None:
        delta, self._w[i] = weight - self._w[i], weight
        self._total += delta
        i += 1
        while i <= self._n:                            # 沿父链把增量加到所有覆盖 i 的节点
            self._tree[i] += delta
            i += i & -i

    def sample(self) -> int:
        return self.locate(self._rng.randrange(self._total))

    def locate(self, r: int) -> int:
        """找最小的下标 i，使前缀和 w[0..i] > r（r 取 [0, total) 均匀分布）。"""
        pos = 0
        step = 1 << self._n.bit_length()
        while step:                                    # 倍增下降：从高位到低位试着往右跨
            nxt = pos + step
            if nxt <= self._n and self._tree[nxt] <= r:
                pos = nxt
                r -= self._tree[nxt]
            step >>= 1
        return pos                                     # 此时 pos 个元素的前缀和 <= r，所以答案是 0-based 的 pos
```

运行：`[1,3,0,6]` 执行 `update(2, 2)`、`update(0, 0)` 后，`r = 0..10` → `[1, 1, 1, 2, 2, 3, 3, 3, 3, 3, 3]`。

- 线段树 vs Fenwick 树：都是 `O(log n)`；Fenwick 更短、常数小；线段树还能做区间更新；元素个数会增减时用平衡树。
- 静态权重、采样极多：别名法（alias method）`O(n)` 建表、`O(1)` 采样，但不支持更新。

**同模式。** LC 528 按权重随机选择、LC 497 非重叠矩形中的随机点、LC 398 随机数索引、LC 307 区域和检索 - 数组可修改。
