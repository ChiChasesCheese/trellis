---
id: tlc-maximum-performance-of-a-team-0-whole
node: c.maximum-performance-of-a-team
type: qa
---
## Q
**LC 1383 最大的团队表现值**｜Hard · LC TikTok 全时段热度 26/100

给定两个整数 `n` 和 `k`，以及两个长度为 `n` 的整数数组 `speed` 和 `efficiency`，现有 `n` 名工程师，`speed[i]` 和 `efficiency[i]` 分别是第 `i` 位工程师的速度和效率。从中最多选择 `k` 名不同的工程师组成团队，团队表现值 = 所有工程师速度之和 × 他们效率值中的最小值。返回最大团队表现值，由于答案可能很大，返回结果对 `10^9 + 7` 取余。`1 <= k <= n <= 10^5`，`speed.length == n`，`efficiency.length == n`，`1 <= speed[i] <= 10^5`，`1 <= efficiency[i] <= 10^8`。例：`n = 6, speed = [2,10,3,1,5,8], efficiency = [5,4,3,9,7,2], k = 2` → `60`（选速度 10 与 5，`(10 + 5) * min(4, 7)`）；同数据 `k = 3` → `68`；`k = 4` → `72`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 按效率从高到低枚举「团队里效率最低的人」，此时可选的人效率都不低于他；在这些人里取速度最大的 `k` 个，用大小为 `k` 的最小堆维护速度和，`O(n log n)`。

**识别。** 「乘积 = 总和 × 最小值」且「最多选 `k` 个」：最小值那一维先固定（排序枚举），剩下的问题变成「在候选里取 `k` 个最大值的和」，这是排序 + 堆的固定组合（同类：LC 2542）。

**推导。** 暴力：枚举所有子集，指数级。固定最小效率为 `e`，则只能选效率 `>= e` 的人；速度和越大越好，选速度最大的 `k` 个。按效率降序遍历，当前人是目前最低效率，之前的人效率都不低于他，所以他加入后候选集恰好是「已遍历的人」；用最小堆保留速度最大的 `k` 个，堆满后每加入一人就弹出最小速度。每一步的表现值是 `速度和 * 当前效率`，取最大。取模只在最后做一次，因为比较要用真实值。

```python
from heapq import heappop, heappush


def max_performance(n: int, speed: list[int], efficiency: list[int], k: int) -> int:
    heap: list[int] = []                         # 最小堆：当前选中的速度，最多 k 个
    total = best = 0
    for e, s in sorted(zip(efficiency, speed), reverse=True):   # 效率从高到低
        heappush(heap, s)
        total += s
        if len(heap) > k:
            total -= heappop(heap)               # 超过 k 人：踢掉速度最小的
        best = max(best, total * e)              # 当前人 e 是团队里最低的效率
    return best % (10**9 + 7)                    # Python 整数不溢出：比较用真实值，最后才取模
```

运行：`(6, [2,10,3,1,5,8], [5,4,3,9,7,2], 2)` → `60`，`k = 3` → `68`，`k = 4` → `72`；`(1, [5], [7], 1)` → `35`，`n = k = 10^5`、速度和效率都取最大值 → `49`（真实值约 `10^18`，取模后）。

**复杂度。** 时间 `O(n log n)`（排序加堆），空间 `O(k)` 堆加 `O(n)` 排序副本。

**拓展优化。**
- 用 `heappushpop` 把「先入堆再弹」合成一次操作，满员时少一次堆调整：

```python
from heapq import heappush, heappushpop


def max_performance_pushpop(n: int, speed: list[int], efficiency: list[int], k: int) -> int:
    heap: list[int] = []
    total = best = 0
    for e, s in sorted(zip(efficiency, speed), reverse=True):
        if len(heap) < k:
            heappush(heap, s)
            total += s
        else:
            total += s - heappushpop(heap, s)    # 压入新速度并弹出最小的，和随之更新
        best = max(best, total * e)
    return best % (10**9 + 7)
```

**易错点。**
- 按效率升序遍历：表现值里的最小效率不再是当前这个人，`(6, [2,10,3,1,5,8], [5,4,3,9,7,2], 2)` 得到 `162`，正确是 `60`。
- 弹出最小速度后忘了从 `total` 里减掉：速度和只增不减，同一例子得到 `72`，正确是 `60`。
- 在比较时就取模：取模后的值不能比较大小，会选错最大值。

**追问。**
- 恰好选 `k` 个而不是最多：只在堆满 `k` 个之后才更新答案。
- 求具体选了哪些人：记录取得最大值时的效率阈值，再重新选速度最大的 `k` 个。

**同模式。** LC 2542 最大子序列的分数、LC 857 雇佣 K 名工人的最低成本、LC 502 IPO、LC 215 数组中的第K个最大元素、LC 1642 可以到达的最远建筑。
