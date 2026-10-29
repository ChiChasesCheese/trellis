---
id: tlc-tt-fish-decaying-ponds-2-code
node: a.tt-fish-decaying-ponds
type: qa
step: 2
---
## Q
**鱼塘捕鱼（产量递减）**｜写出 Python 实现

`max_fish(fish, decay, t)`：第 `i` 个鱼塘第一次捕得 `fish[i]` 条，之后每捕一次下一次减少 `decay[i]` 条（不低于 `0`）；共 `t` 次，每次选一个鱼塘，求最大总收获。`1 <= n <= 10^5`，`0 <= fish[i], decay[i] <= 10^9`，`1 <= t <= 10^9`。

## A
**思路。** 所有收获放进一个大集合，取最大的 `t` 个。二分阈值 `x`：最大的 `x` 使“收获 `>= x` 的机会不少于 `t` 个”；严格大于 `x` 的机会全拿（每塘用等差数列求和），剩下的名额每次拿 `x`。

```python
def count_at_least(ponds: list[tuple[int, int]], x: int, cap: int) -> int:
    """单次产量 >= x 的捕鱼机会共有多少个（数到 cap 就停）。ponds 按首捞量降序。"""
    total = 0
    for f, d in ponds:
        if f < x:
            break                                    # 降序排列：后面的塘首捞量更小，都不够
        if d == 0:
            return cap                               # 这个塘永远产 f >= x：机会无限，直接记满
        total += (f - x) // d + 1                    # f, f-d, f-2d, ... 里 >= x 的项数
        if total >= cap:
            return cap
    return total


def find_threshold(ponds: list[tuple[int, int]], t: int) -> int:
    """最大的 x >= 1，使得 count_at_least(x) >= t；所有正产量加起来都不足 t 次时返回 0。"""
    if count_at_least(ponds, 1, t) < t:
        return 0
    lo, hi = 1, ponds[0][0]
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if count_at_least(ponds, mid, t) >= t:
            lo = mid
        else:
            hi = mid - 1
    return lo


def max_fish(fish: list[int], decay: list[int], t: int) -> int:
    ponds = sorted(((f, d) for f, d in zip(fish, decay) if f > 0), reverse=True)   # 产量为 0 的塘没用
    if not ponds:
        return 0
    x = find_threshold(ponds, t)
    taken = total = 0
    for f, d in ponds:
        if f <= x:
            break                                    # 严格大于 x 的机会才全拿
        k = (f - x - 1) // d + 1                     # f, f-d, ... 里 >= x+1 的项数（f > x 时 d > 0）
        taken += k
        total += k * f - d * k * (k - 1) // 2        # 等差数列求和
    return total + (t - taken) * x                   # 剩下的名额，每次恰好拿到 x
```

运行：`[10, 6]`、`[4, 1]`、`t = 3` → `22`；`[5]`、`[5]`、`t = 4` → `5`；`[0, 0]`、`[1, 1]`、`t = 5` → `0`；`[7]`、`[0]`、`t = 10^9` → `7000000000`；`[3, 3]`、`[1, 1]`、`t = 3` → `8`，`t = 100` → `12`；`[10^9]`、`[1]`、`t = 10^9` → `500000000500000000`；`n = 10^5`、随机 `fish` 与 `decay`、`t = 10^9` 的输入正常返回。

**复杂度。** 排序 `O(n log n)`；二分约 `log2(10^9) ≈ 30` 轮，每轮 `O(n)`（遇到首捞量不够的塘就提前结束）；总计 `O(n log n + n log max(fish))`；空间 `O(n)`。

**写法要点。** 先按 `(f, d)` 降序排序，`count_at_least` 才能在 `f < x` 时 `break`；`count_at_least` 带 `cap`，数到 `t` 就提前返回，既省时间，也让 `decay = 0` 的无限机会能用 `cap` 表示；二分写成“找最大的满足条件的值”，所以 `mid = (lo + hi + 1) // 2` 向上取整，`hi = mid - 1`，否则 `lo = mid` 会死循环；等差数列求和用整除 `k * (k - 1) // 2`，Python 整数不会溢出，在 64 位语言里要留意 `10^18` 量级。
