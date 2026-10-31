---
id: tlc-count-the-hidden-sequences-0-whole
node: b.count-the-hidden-sequences
type: qa
---
## Q
**LC 2145 统计隐藏数组数目**｜Medium · LC TikTok 全时段热度 62/100

给一个下标从 `0` 开始、长度为 `n` 的整数数组 `differences`，它表示长度为 `n + 1` 的**隐藏数组** `hidden` 相邻元素之间的差值，即 `differences[i] = hidden[i + 1] - hidden[i]`。再给两个整数 `lower` 和 `upper`，隐藏数组中所有数字都在闭区间 `[lower, upper]` 内。返回符合要求的隐藏数组的数目，没有则返回 `0`。`n == differences.length`，`1 <= n <= 10^5`，`-10^5 <= differences[i] <= 10^5`，`-10^5 <= lower <= upper <= 10^5`。例：`differences = [1,-3,4]`，`lower = 1`，`upper = 6` → `2`（`[3,4,1,5]` 和 `[4,5,2,6]`）；`differences = [3,-4,5,1,-2]`，`lower = -4`，`upper = 5` → `4`；`differences = [4,-7,2]`，`lower = 3`，`upper = 6` → `0`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 隐藏数组由起点 `hidden[0]` 唯一确定：`hidden[i] = hidden[0] + prefix[i]`，其中 `prefix` 是 `differences` 的前缀和（开头补一个 `0`）。整个数组的“形状”固定，最大值与最小值之差 `spread = max(prefix) - min(prefix)` 固定；起点能平移的位置数就是 `(upper - lower) - spread + 1`（不能为负）。`O(n)`。

**识别。** 「已知相邻差，求有多少个原序列」是前缀和（prefix sum）的信号：差分的逆运算就是前缀和。“都在 `[lower, upper]` 内”是对整条序列最大 / 最小值的约束，而不是逐个枚举。`n = 10^5`，值域 `10^5`，`O(n · 值域)` 的枚举起点不行，要 `O(n)`。

**推导。** 暴力：枚举起点 `x` 从 `lower` 到 `upper`，逐个检查 `x + prefix[i]` 是否都在范围内，`O(n · (upper - lower))`，最坏 `10^5 × 2 × 10^5`。浪费：每个起点都重新检查整条序列，而整条序列的“形状”（相对于起点的偏移）是固定的。洞察：序列合法当且仅当最小的元素 `x + min(prefix) >= lower` 并且最大的元素 `x + max(prefix) <= upper`，也就是 `lower - min(prefix) <= x <= upper - max(prefix)`。合法起点的个数是 `upper - max(prefix) - lower + min(prefix) + 1`，再与 `0` 取最大值。

```python
from itertools import accumulate


def number_of_arrays(differences: list[int], lower: int, upper: int) -> int:
    prefix = [0, *accumulate(differences)]     # hidden[i] = hidden[0] + prefix[i]，别漏掉开头的 0
    spread = max(prefix) - min(prefix)         # 数组内最大值与最小值之差，由 differences 唯一确定
    return max(0, (upper - lower) - spread + 1)   # 起点 hidden[0] 在区间内能平移多少个位置
```

运行：`([1,-3,4], 1, 6)` → `2`，`([3,-4,5,1,-2], -4, 5)` → `4`，`([4,-7,2], 3, 6)` → `0`，`([1,2], 1, 3)` → `0`，`([0], 5, 5)` → `1`；`10^5` 个随机差值 → 瞬间返回。

**复杂度。** 时间 `O(n)`：一次前缀和，加一次最大值、一次最小值；空间 `O(n)`（`prefix` 列表）。

**易错点。**
- 前缀和漏掉开头的 `0`：`hidden[0]` 本身也是数组的一个元素，也必须落在区间内。`differences = [1,2]`，`lower = 1`，`upper = 3`：真实的数组形状是 `[0,1,3]`，跨度 `3 > upper - lower = 2`，答案 `0`；漏掉 `0` 后跨度只算 `2`，返回 `1`，错。
- 没有和 `0` 取最大：跨度大于区间时公式给出负数。`([4,-7,2], 3, 6)` 的公式值是 `-3`，应当返回 `0`。
- 把答案当成 `upper - lower + 1`：忽略了差值序列已经占用了一部分空间。

**追问。**
- 流式输入或不想存 `prefix`：边累加边维护当前值、最大值、最小值，`O(1)` 额外空间。
- 要列出所有隐藏数组：起点取 `lower - min(prefix)` 到 `upper - max(prefix)`，每个起点加上 `prefix` 就是一个数组，输出规模 `O(n × 个数)`。
- 要求隐藏数组严格递增 / 元素互不相同：条件变成对 `differences` 的约束，答案要么 `0`，要么不变，视差值是否满足而定。

**同模式。** LC 1423 可获得的最大点数、LC 53 最大子数组和、LC 303 区域和检索、LC 1094 拼车、LC 370 区间加法。
