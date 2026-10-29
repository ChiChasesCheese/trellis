---
id: tlc-tt-weighted-sampler-dynamic-update-2-code
node: b.tt-weighted-sampler-dynamic-update
type: qa
step: 2
---
## Q
**按权重采样器（支持动态修改权重）**｜写出 Python 实现

类 `Sampler(weights, rng=None)`：`weights` 是 `n` 个非负整数（`1 <= n <= 10^5`，`0 <= w[i] <= 10^6`，至少一个为正）；`sample()` 按权重比例随机返回下标；`update(i, weight)` 修改第 `i` 个权重。`sample` 和 `update` 都要 `O(log n)`。`rng` 是可注入的 `random.Random`。

## A
**思路。** 用 Fenwick 树存权重。`update` 计算增量，沿父链（下标不断加上最低位 1）加到所有覆盖该位置的节点。`sample` 先取 `r ∈ [0, total)` 的随机整数，再用倍增下降找到最大的 `pos` 使前 `pos` 个权重之和 `<= r`，下标就是 `pos`。

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

运行：权重 `[1,3,0,6]`，`locate(r)` 对 `r = 0..9` → `[0, 1, 1, 1, 3, 3, 3, 3, 3, 3]`；`update(2, 2)`、`update(0, 0)` 后，`r = 0..10` → `[1, 1, 1, 2, 2, 3, 3, 3, 3, 3, 3]`；`Sampler([5]).locate(r)` 对 `r = 0..4` 全是 `0`。

**复杂度。** 建树 `O(n)`，`update`、`sample` 各 `O(log n)`；空间 `O(n)`。

**写法要点。** `i & -i` 取最低位的 `1`，Fenwick 树的父子关系就靠它；线性建树比逐个 `update` 的 `O(n log n)` 快；`delta, self._w[i] = weight - self._w[i], weight` 在一条语句里先算增量再保存新值，避免用过期的旧权重；`locate` 拆成独立方法，传入固定的 `r` 就能做确定性测试，`sample` 只负责取随机数；`rng` 可注入，测试时传种子固定的 `random.Random`；`randrange(total)` 的上界不含 `total`，与「前缀和 `> r`」的约定一致。
