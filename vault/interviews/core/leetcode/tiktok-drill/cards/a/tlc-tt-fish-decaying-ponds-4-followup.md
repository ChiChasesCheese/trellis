---
id: tlc-tt-fish-decaying-ponds-4-followup
node: a.tt-fish-decaying-ponds
type: qa
step: 4
---
## Q
**鱼塘捕鱼（产量递减）**｜追问

求出最大收获后，面试官接着问：（1）要输出具体方案，即每个鱼塘各捕几次？（2）每个鱼塘最多只能捕 `c[i]` 次呢？（3）在 C++ / Java 里实现，哪里会溢出？

## A
1. **输出方案。** 用二分阈值函数 `find_threshold` 得到 `x` 之后：严格大于 `x` 的机会每塘取 `(f - x - 1) // d + 1` 次；剩下的名额拿恰好等于 `x` 的机会：序列里恰有一个 `x` 的塘（`(f - x) % d == 0`）各补一次，`decay = 0` 且 `f == x` 的塘可补多次。

```python
def fish_plan(fish: list[int], decay: list[int], t: int) -> list[int]:
    order = sorted((i for i, f in enumerate(fish) if f > 0),
                   key=lambda i: (fish[i], decay[i]), reverse=True)
    counts = [0] * len(fish)
    if not order:
        return counts
    x = find_threshold([(fish[i], decay[i]) for i in order], t)
    left = t
    for i in order:
        if fish[i] > x:
            counts[i] = (fish[i] - x - 1) // decay[i] + 1      # 严格大于 x 的机会全拿
            left -= counts[i]
    for i in order:                                              # 剩下的名额拿恰好等于 x 的机会
        f, d = fish[i], decay[i]
        if x and left and f >= x and (d == 0 or (f - x) % d == 0):
            extra = left if d == 0 else 1
            counts[i] += extra
            left -= extra
    return counts
```

   运行：`fish_plan([10, 6], [4, 1], 3)` → `[2, 1]`（共 `22`）；`fish_plan([3, 3], [1, 1], 3)` → `[2, 1]`（共 `8`）；`fish_plan([7], [0], 5)` → `[5]`。
2. **每塘最多 `c[i]` 次。** 单调性不变，只改计数：塘 `i` 里 `>= x` 的机会数是 `min(c[i], (f - x) // d + 1)`，求和时的 `k` 同样取 `min`；`decay = 0` 的塘机会数变成 `c[i]`，不再无限。
3. **溢出。** 题目范围内 `int64` 够用：总收获至多 `t · max(fish) = 10^18`，每塘的 `k · f` 与 `d · k · (k - 1)` 也在 `10^18` 量级，低于 `9.2 × 10^18`；范围再放大就要 `__int128`，或先算 `k · (k - 1) / 2` 再乘 `d`。

**Python 提醒**：`sorted(..., key=..., reverse=True)` 仍然稳定，键相同的元素保持原来的先后顺序。
