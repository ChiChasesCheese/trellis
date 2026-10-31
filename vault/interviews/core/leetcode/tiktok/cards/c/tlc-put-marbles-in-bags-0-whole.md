---
id: tlc-put-marbles-in-bags-0-whole
node: c.put-marbles-in-bags
type: qa
---
## Q
**LC 2551 将珠子放入背包中**｜Hard · LC TikTok 全时段热度 26/100

你有 `k` 个背包。给你下标从 0 开始的整数数组 `weights`，`weights[i]` 是第 `i` 个珠子的重量，以及整数 `k`。按如下规则把所有珠子放进 `k` 个背包：没有背包是空的；如果第 `i` 个和第 `j` 个珠子在同一个背包里，那么下标在 `i` 到 `j` 之间的所有珠子都必须在这同一个背包中；如果一个背包有下标从 `i` 到 `j` 的所有珠子，这个背包的价格是 `weights[i] + weights[j]`。一个分配方案的分数是所有 `k` 个背包的价格之和。返回所有分配方案中，最大分数与最小分数的差值。`1 <= k <= weights.length <= 10^5`，`1 <= weights[i] <= 10^9`。例：`weights = [1,3,5,1], k = 2` → `4`（最小分数 `[1],[3,5,1]` 得 `6`，最大分数 `[1,3],[5,1]` 得 `10`）；`weights = [1,3], k = 2` → `0`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 分数 = `weights[0] + weights[-1]` 加上每个「切点」`i`（在 `i` 与 `i+1` 之间切开）贡献的 `weights[i] + weights[i+1]`；最大最小分数都要选 `k-1` 个切点，首尾项抵消，答案是「最大的 `k-1` 个相邻和」减去「最小的 `k-1` 个相邻和」，`O(n log n)`。

**识别。** 「把序列切成 `k` 段连续的块，块的价格只依赖两端」：把总分拆成「每个切点的贡献」，切点之间互相独立，变成从 `n-1` 个候选里选 `k-1` 个，最大化或最小化和，就是排序取极值。

**推导。** 第一个珠子一定是第一个背包的头，最后一个珠子一定是最后一个背包的尾，所以 `weights[0] + weights[-1]` 对所有方案相同。其余的头尾来自切点：在 `i` 与 `i+1` 之间切开，背包 A 以 `weights[i]` 收尾、背包 B 以 `weights[i+1]` 开头，贡献 `weights[i] + weights[i+1]`。任意 `k-1` 个不同切点都是合法方案，所以最大分数选最大的 `k-1` 个切点和，最小分数选最小的 `k-1` 个，做差后首尾项抵消。

```python
from itertools import pairwise


def put_marbles(weights: list[int], k: int) -> int:
    cuts = sorted(a + b for a, b in pairwise(weights))   # 每个切点的贡献：相邻两个珠子的重量和
    # 取最大的 k-1 个与最小的 k-1 个相减；k=1 时两个切片都是空，结果为 0
    return sum(cuts[len(cuts) - (k - 1):]) - sum(cuts[:k - 1])
```

运行：`([1,3,5,1], 2)` → `4`，`([1,3], 2)` → `0`；`([1,3,5], 1)` → `0`，`([7], 1)` → `0`，`([1,1,1,1], 3)` → `0`。

**复杂度。** 时间 `O(n log n)`，空间 `O(n)`。

**拓展优化。**
- 只要极值不必全排序：`heapq.nlargest` 与 `nsmallest` 取 `k-1` 个，`O(n log k)`；`k` 很小时更快。

```python
from heapq import nlargest, nsmallest
from itertools import pairwise


def put_marbles_heap(weights: list[int], k: int) -> int:
    cuts = [a + b for a, b in pairwise(weights)]
    return sum(nlargest(k - 1, cuts)) - sum(nsmallest(k - 1, cuts))   # k-1 为 0 时两者都是空列表
```

**易错点。**
- 用负数切片 `cuts[-(k - 1):]`：`k = 1` 时变成 `cuts[-0:]`，即整个列表，`([1,3,5], 1)` 得到 `12`，正确是 `0`。
- 把首尾项也算进差值：它们在最大和最小分数里相同，会被抵消，不要单独处理。
- 切点个数写成 `k`：`k` 个背包只有 `k-1` 个切点。

**追问。**
- 只求最大分数：`weights[0] + weights[-1] + 最大的 k-1 个切点和`。
- 背包价格改成 `weights[i] * weights[j]`：切点贡献不再可加，需要换成 DP。

**同模式。** LC 1235 规划兼职工作、LC 1713 得到子序列的最少操作次数、LC 410 分割数组的最大值、LC 1423 可获得的最大点数、LC 2742 给墙壁刷油漆。
