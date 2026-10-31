---
id: tlc-capacity-to-ship-packages-within-d-days-0-whole
node: b.capacity-to-ship-packages-within-d-days
type: qa
---
## Q
**LC 1011 在 D 天内送达包裹的能力**｜Medium · LC TikTok 全时段热度 50/100 · CodeTop 国内累计 3 次 · 最近 2023-02-28（国内 CodeTop）

传送带上的包裹必须在 `days` 天内从一个港口运送到另一个港口。第 `i` 个包裹重 `weights[i]`。每天按给出的顺序往船上装包裹，装载的总重量不能超过船的最大载重。返回能在 `days` 天内送达所有包裹的船的**最低**载重。`1 <= days <= weights.length <= 5 * 10^4`，`1 <= weights[i] <= 500`。例：`weights = [1,2,3,4,5,6,7,8,9,10]`，`days = 5` → `15`；`weights = [3,2,2,4,1,4]`，`days = 3` → `6`；`weights = [1,2,3,1,1]`，`days = 4` → `3`。必须按顺序装，不能调换包裹位置。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 二分答案（binary search on the answer）：载重越大，需要的天数越少，这是单调的；在 `[max(weights), sum(weights)]` 上二分，判定函数用一次线性贪心——按顺序装，装不下就换一天——统计天数是否 `<= days`。`O(n log S)`，`S = sum(weights)`。

**识别。** 「求满足限制的最小载重」，限制随答案单调，并且判定只需一遍扫描，就是二分答案。顺序固定、每天装连续的一段，等价于“把数组切成不超过 `days` 段，使最大段和最小”（LC 410）。

**推导。** 暴力：载重从 `max(weights)` 起逐个试，每个 `O(n)`，最多试 `sum - max` 个（约 `2.5 × 10^7`），总量 `10^12` 以上。浪费：载重越大天数越少，可行性是单调的，不必逐个试。洞察：判定一个载重是否可行，贪心地每天尽量多装即可，因为今天多装，剩下的包裹更少，不会更差。二分约 `25` 轮，每轮 `O(n)`。下界取 `max(weights)`，因为最重的包裹必须能装下；上界取 `sum(weights)`，一天全装完一定可行。

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

**复杂度。** 时间 `O(n log S)`，`S <= 2.5 × 10^7`，二分约 `25` 轮；空间 `O(1)`。

**易错点。**
- 下界写成 `1` 而不是 `max(weights)`：载重小于某个包裹时，判定里“换一天”只是把它放进新的一天，并没有判它装不下，于是误判为可行。`[1,2,3,1,1]`、`days = 4` 得到 `2`（正确 `3`），`[10,1,1]`、`days = 3` 得到 `2`（正确 `10`）。
- 天数从 `0` 开始计：少算了第一天，`[1..10]`、`days = 5` 得到 `11`（正确 `15`）。
- 把它当成可以调换顺序的装箱问题：这里每天只能装连续的一段，贪心必须按给定顺序，不能把后面的小包裹塞进前面一天的空隙。

**追问。**
- 输出具体的装载方案：用最终载重再跑一遍贪心，记录每次换天的位置。
- 收窄二分范围：下界可以取 `max(max(weights), ceil(sum / days))`，因为总载重除以天数是平均下限。
- 把 `days` 换成 `m` 段，求最大段和的最小值，就是 LC 410，代码一行不用改。

**同模式。** LC 410 分割数组的最大值、LC 875 爱吃香蕉的珂珂、LC 1482 制作 m 束花所需的最少天数、LC 2187 完成旅途的最少时间、LC 1231 分享巧克力。
