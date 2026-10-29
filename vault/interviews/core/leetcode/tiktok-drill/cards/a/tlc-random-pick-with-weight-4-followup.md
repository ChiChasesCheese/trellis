---
id: tlc-random-pick-with-weight-4-followup
node: a.random-pick-with-weight
type: qa
step: 4
---
## Q
**LC 528 按权重随机选择**｜追问

面试官接着问：（1）权重会动态更新，`update(i, delta)` 之后继续抽？（2）抽取要 `O(1)`？（3）不放回，连续抽出互不相同的下标？分别怎么改。

## A
1. **动态更新**：前缀和数组更新一次要改 `O(n)` 个元素，换成树状数组（Fenwick tree）：更新 `O(log n)`；抽取时在树上从高位往低位“倍增下降”，找最大的 `pos` 使前 `pos` 个元素的和 `<= r`，这个 `pos` 就是答案下标。

```python
class WeightedPicker:
    def __init__(self, w: list[int]):
        self.n = len(w)
        self.tree = [0] * (self.n + 1)           # 树状数组，下标从 1 开始
        for i, x in enumerate(w):
            self.update(i, x)

    def update(self, i: int, delta: int) -> None:
        i += 1
        while i <= self.n:
            self.tree[i] += delta
            i += i & -i

    def locate(self, r: int) -> int:
        pos, step = 0, 1 << self.n.bit_length()
        while step:                              # 倍增下降
            nxt = pos + step
            if nxt <= self.n and self.tree[nxt] <= r:
                pos = nxt
                r -= self.tree[nxt]
            step >>= 1
        return pos                               # 0-based 下标
```

   总权重可以另存一个变量，随 `update` 同步增减；抽取为 `locate(random.randrange(total))`。
2. **`O(1)` 抽取**：别名法（alias method）。构造 `O(n)`，每次抽取一个随机下标加一个随机数就能决定；代价是不支持更新，常数也比二分大，只在抽取次数远多于下标数时才值得。
3. **不放回**：抽中后把该下标的权重 `update(i, -w[i])` 减到 `0`，总权重同步减小，再抽；每次 `O(log n)`。重建前缀和每次要 `O(n)`。

**Python 提醒**：`random.choices(population, weights=w)` 每次调用都会重新对 `w` 做 `accumulate`，是 `O(n)`；反复抽样要传预先算好的 `cum_weights`。另外 `choices` 是有放回的，不放回用 `random.sample`（它不支持权重）。
