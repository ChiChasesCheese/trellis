---
id: tlc-maximal-score-after-applying-k-operations-0-whole
node: c.maximal-score-after-applying-k-operations
type: qa
---
## Q
**LC 2530 执行 K 次操作后的最大分数**｜Medium · LC TikTok 全时段热度 25/100

给定整数数组 `nums` 和整数 `k`，起始分数为 `0`。一次操作：选一个下标 `i`，分数增加 `nums[i]`，然后把 `nums[i]` 替换成 `ceil(nums[i] / 3)`。返回**恰好**执行 `k` 次操作后的最大分数。`1 <= nums.length, k <= 10^5`，`1 <= nums[i] <= 10^9`。例：`nums = [10,10,10,10,10]`，`k = 5` → `50`；`nums = [1,10,3,3,3]`，`k = 3` → `17`（取 `10`、`4`、`3`）。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 贪心：每次都取当前最大的数，加到分数里，再把它替换成 `ceil(x / 3)` 放回，用最大堆维护。

**识别。** 「每次取最大、取完后值变化再放回」：最大堆的典型场景（LC 1962、LC 1167 同类）。每次操作改变的只有被取的那一个数，所以堆里更新一个元素就够。

**推导。** 每次扫描数组找最大值，`O(n · k)`，`10^10` 不可行。贪心成立的理由：每次操作的收益是当前取走的数，而操作后的数是它的函数且单调不减；先取大的永远不亏（交换论证：取小的换大的，当前收益增加，后续替换后的值也不减）。Python 的堆是小根堆，存负数；`heapreplace` 一次完成「弹出堆顶并压入新值」，比 `heappop` 加 `heappush` 快。`ceil(x / 3)` 用整数运算写成 `(x + 2) // 3`，避免浮点。

```python
from heapq import heapify, heapreplace


def max_kelements(nums: list[int], k: int) -> int:
    heap = [-x for x in nums]                    # 小根堆存负数，等价于最大堆
    heapify(heap)
    score = 0
    for _ in range(k):
        x = -heap[0]                             # 当前最大值
        score += x
        heapreplace(heap, -((x + 2) // 3))       # 弹出最大值并压入 ceil(x / 3)，一次 O(log n)
    return score
```

运行：`([10,10,10,10,10], 5)` → `50`，`([1,10,3,3,3], 3)` → `17`；`([1], 5)` → `5`；`([10**9], 3)` → `1444444446`（`10^9 + 333333334 + 111111112`）。

**复杂度。** 时间 `O(n + k log n)`，空间 `O(n)`。

**拓展优化。**
- 数很快会衰减到 `1`（`10^9` 约 19 次操作后变 `1`），堆顶为 `1` 时剩余操作每次都加 `1`，可以提前结束：

```python
def max_kelements_early_stop(nums: list[int], k: int) -> int:
    heap = [-x for x in nums]
    heapify(heap)
    score = 0
    for done in range(k):
        x = -heap[0]
        if x == 1:                               # 堆里所有数都是 1：剩下的操作每次加 1
            return score + (k - done)
        score += x
        heapreplace(heap, -((x + 2) // 3))
    return score
```

- `k` 远大于 `n` 且数很大时，这个提前结束让复杂度与 `k` 无关（有效操作数不超过 `n · 20`）。

**易错点。**
- 用 `x / 3` 再 `math.ceil`：`10^9` 以内浮点足够精确，但整数写法 `(x + 2) // 3` 更稳，也更快。
- 先 `heappush` 新值再 `heappop`：弹出的可能是刚压入的值。先弹再压，或直接用 `heapreplace`，一步完成。
- 把最大堆写成 `-heap[0]` 却忘了存的是负数：压入时要 `-new_value`，漏掉符号会把最小值当作最大值。

**追问。**
- 每次操作的替换规则换成 `x // 2`、`sqrt(x)` 等：只要替换后不大于原值且函数单调，贪心依然成立。
- 每个下标最多操作 `m` 次：需要给堆元素加操作计数，达到上限不再放回。

**同模式。** LC 1962 移除石子使总数最小、LC 1167 连接棒材的最低费用、LC 1046 最后一块石头的重量、LC 2208 将数组和减半的最少操作次数、LC 2233 K 次增加后的最大乘积。
