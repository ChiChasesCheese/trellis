---
id: tlc-super-egg-drop-4-followup
node: b.super-egg-drop
type: qa
step: 4
---
## Q
**LC 887 鸡蛋掉落**｜追问

面试官接着问：（1）要输出每一步该从哪一层扔？（2）蛋很多时能不能提前结束？（3）`n` 到 `10^18` 怎么办？

## A
1. **输出策略**：在状态“`m` 次、`k` 枚蛋、当前区间起点 `lo`”下，下一次扔 `lo + f(m-1, k-1)` 层（即下方恰好能被 `k-1` 枚蛋覆盖的上限加一）。碎了就在 `[lo, x-1]` 里用 `m-1` 次、`k-1` 枚蛋继续；没碎就把 `lo` 提到 `x + 1`，用 `m-1` 次、`k` 枚蛋继续。需要把每轮的 `floors` 快照存下来（`m` 行 × `k` 列，很小）。
2. **蛋很多**：`k >= n.bit_length()` 时蛋已经够做纯二分，答案是 `ceil(log2(n + 1))`；先写 `k = min(k, n.bit_length())` 可以把外层循环缩短，数据大时有用。
3. **`n` 到 `10^18`**：`m` 次操作、`k` 枚蛋能覆盖的层数有闭式 `f(m, k) = Σ_{i=1..k} C(m, i)`，且随 `m` 单调增，对 `m` 二分。

```python
from math import comb


def super_egg_drop_binary(k: int, n: int) -> int:
    lo, hi = 1, n
    while lo < hi:
        mid = (lo + hi) // 2
        if sum(comb(mid, i) for i in range(1, min(k, mid) + 1)) >= n:
            hi = mid
        else:
            lo = mid + 1
    return lo
```

   `(2, 6)` → `3`，`(100, 10**4)` → `14`，`(2, 10**18)` → `1414213562`。每次判定 `O(k)` 次 `comb`，`m` 的二分约 `60` 轮。

**Python 提醒**：`math.comb(n, r)` 是精确的大整数，不会像浮点那样丢精度；`r > n` 时返回 `0`，所以 `min(k, mid)` 只是少算几项，不影响结果。`n` 很大时 `comb(mid, i)` 本身是大数，`k` 取 `100` 左右时单次判定已经偏慢，可以在累加和超过 `n` 时提前 `break`。
