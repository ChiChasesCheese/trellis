---
id: tlc-tt-weighted-sampler-dynamic-update-0-whole
node: a.tt-weighted-sampler-dynamic-update
type: qa
---
## Q
**按权重采样器（支持动态修改权重）**｜Medium · TikTok 高频

写一个类 `Sampler`：给定 `n` 个非负整数权重 `w`（至少一个为正），`sample()` 按权重比例随机返回一个下标（下标 `i` 被选中的概率是 `w[i] / sum(w)`，权重为 `0` 的下标永远不会被选中）。追问：权重会动态修改，`update(i, weight)` 把第 `i` 个权重改成新值；用前缀和每次更新要 `O(n)`，太慢，要让 `update` 和 `sample` 都是 `O(log n)`。`1 <= n <= 10^5`，`0 <= w[i] <= 10^6`，调用总数不超过 `10^5`。为了可测试，构造函数可接收一个 `random.Random`。例：权重 `[1,3,0,6]`，总和 `10`，随机整数 `r` 取 `0..9` 时分别落在下标 `[0,1,1,1,3,3,3,3,3,3]`；`update(2, 2)`、`update(0, 0)` 后权重是 `[0,3,2,6]`，`r` 取 `0..10` 时落在 `[1,1,1,2,2,3,3,3,3,3,3]`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 用 Fenwick 树（树状数组）维护权重的前缀和：`sample` 取随机整数 `r ∈ [0, total)`，在树上用倍增下降直接找「最小的下标使前缀和大于 `r`」；`update` 沿父链把增量加到所有覆盖该位置的节点。两者都是 `O(log n)`。

**识别。** 「按权重随机」是逆变换采样：权重的前缀和把 `[0, total)` 切成长度正比于权重的区间，随机整数落在哪个区间就选哪个下标，查找用二分；「权重动态修改」意味着需要支持单点更新、前缀和查询的结构：Fenwick 树、线段树、平衡树。

**推导。** 暴力：每次 `sample` 线性扫描累加，`O(n)` → 前缀和加 `bisect_right`：采样 `O(log n)`，但每次更新要重算前缀和 `O(n)` → 浪费：一次单点修改只影响少数「覆盖」它的前缀和，重算全部不必要 → 洞察：Fenwick 树的节点 `i` 负责 `(i - lowbit(i), i]` 这一段的权重和，单点更新只改 `O(log n)` 个节点，前缀和查询也只合并 `O(log n)` 个节点；采样要的是「找第一个前缀和大于 `r` 的位置」，直接在树上倍增下降（从高位到低位试着往右跨），一次 `O(log n)`，比「二分加每步求前缀和」的 `O(log² n)` 更快。

```python
import random


class Sampler:
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

运行：权重 `[1,3,0,6]`，`locate(r)` 对 `r = 0..9` → `[0, 1, 1, 1, 3, 3, 3, 3, 3, 3]`；`update(2, 2)`、`update(0, 0)` 后 `r = 0..10` → `[1, 1, 1, 2, 2, 3, 3, 3, 3, 3, 3]`；权重为 `0` 的下标不会出现在结果里；`10^5` 个权重、更新最后一个权重为 `10^6` 后仍能正常采样。

**复杂度。** 建树 `O(n)`；`update` 和 `sample` 都是 `O(log n)`；空间 `O(n)`。

**易错点。**
- 区间边界错一位：随机整数在 `[0, total)`，要找「前缀和 `> r`」的第一个位置。用 `bisect_left` 代替 `bisect_right` 会让 `[1,3,0,6]` 的 `r = 1` 落到下标 `0`（应为 `1`），整体向前偏一位，概率错误。
- `update` 的增量用了过期的旧值：必须同步更新 `self._w`。把 `[1,3,0,6]` 先 `update(1, 5)` 再 `update(1, 7)`，若第二次仍拿构造时的 `3` 算增量，总和变成 `16`，正确是 `14`。
- 总权重为 `0`（全是 `0`）：`randrange(0)` 抛 `ValueError`，需要在构造或 `update` 时拒绝，或让 `sample` 明确报错。

**追问。**
- 线段树 vs Fenwick 树：线段树也是 `O(log n)`，能扩展到区间更新、区间查询；Fenwick 更短、常数更小。需要增删元素的个数时用平衡二叉搜索树。
- 无放回加权抽样 `k` 个：每抽中一个就把它的权重 `update` 成 `0`，抽完再恢复，`O(k log n)`。
- 静态权重、采样极多：别名法（alias method）`O(n)` 建表、`O(1)` 采样，但不支持更新。

**同模式。** LC 528 按权重随机选择、LC 497 非重叠矩形中的随机点、LC 398 随机数索引、LC 380 O(1) 时间插入、删除和获取随机元素、LC 307 区域和检索 - 数组可修改。
