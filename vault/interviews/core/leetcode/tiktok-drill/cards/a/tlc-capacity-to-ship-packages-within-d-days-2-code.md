---
id: tlc-capacity-to-ship-packages-within-d-days-2-code
node: a.capacity-to-ship-packages-within-d-days
type: qa
step: 2
---
## Q
**LC 1011 在 D 天内送达包裹的能力**｜写出 Python 实现

`weights` 是按传送带顺序给出的包裹重量（`1 <= days <= weights.length <= 5 * 10^4`，`1 <= weights[i] <= 500`），每天按顺序装一段连续的包裹，总重不超过船的载重。返回能在 `days` 天内送完的最低载重。

## A
**思路。** 载重 `c` 越大所需天数越少。在 `[max(weights), sum(weights)]` 上二分，找第一个 `days_needed(c) <= days` 的 `c`。`days_needed` 按顺序装，装不下就换天。

```python
def ship_within_days(weights: list[int], days: int) -> int:
    def days_needed(capacity: int) -> int:
        used, load = 1, 0                      # 第 1 天开始装
        for w in weights:
            if load + w > capacity:            # 今天装不下，换下一天
                used += 1
                load = 0
            load += w
        return used

    lo, hi = max(weights), sum(weights)        # 至少要装得下最重的包裹；一天全装完一定够
    while lo < hi:
        mid = (lo + hi) // 2
        if days_needed(mid) <= days:
            hi = mid
        else:
            lo = mid + 1
    return lo
```

运行：三个示例依次得到 `15`、`6`、`3`；`([10], 1)` → `10`，`([10,1,1], 3)` → `10`；`5 × 10^4` 个随机重量、`days = 25000` 约 `20 ms`。

**复杂度。** 时间 `O(n log S)`：`S = sum(weights) <= 2.5 × 10^7`，二分约 `25` 轮，每轮扫描 `n` 个包裹；空间 `O(1)`。

**写法要点。** 判定函数写成嵌套函数，直接读外层的 `weights`，不用传参；换天时 `load = 0` 之后统一 `load += w`，同一行代码处理“放进新的一天”和“继续放进今天”；`lo, hi = max(weights), sum(weights)` 两个内置函数一行给出上下界；Python 3.10 起也可以写 `lo + bisect_left(range(lo, hi + 1), True, key=lambda c: days_needed(c) <= days)`。
