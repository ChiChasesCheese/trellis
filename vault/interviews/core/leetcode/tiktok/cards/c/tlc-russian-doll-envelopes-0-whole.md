---
id: tlc-russian-doll-envelopes-0-whole
node: c.russian-doll-envelopes
type: qa
---
## Q
**LC 354 俄罗斯套娃信封问题**｜Hard · LC TikTok 全时段热度 26/100 · CodeTop 国内累计 4 次 · 最近 2022-08-28（国内 CodeTop）

给你一个二维整数数组 `envelopes`，`envelopes[i] = [wi, hi]` 表示第 `i` 个信封的宽度和高度。当另一个信封的宽度和高度都**严格**比这个信封大的时候，这个信封就可以放进另一个信封里，如同俄罗斯套娃一样。计算最多能有多少个信封能组成一组「俄罗斯套娃」信封（即可以把一个信封放到另一个信封里面）。不允许旋转信封。`1 <= envelopes.length <= 10^5`，`envelopes[i].length == 2`，`1 <= wi, hi <= 10^5`。例：`envelopes = [[5,4],[6,4],[6,7],[2,3]]` → `3`（`[2,3] => [5,4] => [6,7]`）；`envelopes = [[1,1],[1,1],[1,1]]` → `1`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 按宽度升序、宽度相同时高度**降序**排序，然后只看高度序列求严格最长递增子序列（LIS），用二分维护 `tails` 数组，`O(n log n)`。

**识别。** 「两个维度都要严格增大」的链是二维偏序，经典做法是先排序消掉一维，剩下一维求 LIS。`n = 10^5` 排除 `O(n²)`。

**推导。** 暴力：按宽度排序后 `dp[i] = 1 + max dp[j]`（`j` 的宽、高都小于 `i`），`O(n²)`。排序只解决了宽度的顺序，但**宽度相同**的信封不能互相嵌套，LIS 却可能把它们选进同一条链。洞察：宽度相同的信封按高度**降序**排，这样在高度序列里它们是递减的，严格递增子序列最多选其中一个。排完后，问题就是 `h` 序列的严格 LIS：`tails[k]` 记录长度为 `k + 1` 的递增子序列的最小结尾高度，新高度用 `bisect_left` 找到第一个 `>= h` 的位置并替换，位置等于长度就追加。

**简单解法。** 按宽度排序后做 `O(n²)` 的 LIS DP，宽、高都用严格比较。

```python
def max_envelopes_dp(envelopes: list[list[int]]) -> int:
    order = sorted(envelopes)
    dp = [1] * len(order)                        # dp[i]：以 order[i] 作最外层的最长链
    for i in range(len(order)):
        for j in range(i):
            if order[j][0] < order[i][0] and order[j][1] < order[i][1]:   # 宽、高都严格更小
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)
```

`O(n²)`，`n = 10^5` 时超时；但逻辑最直白，不依赖「同宽降序」的技巧。

最优解：

```python
from bisect import bisect_left


def max_envelopes(envelopes: list[list[int]]) -> int:
    # 宽度升序；同宽时高度降序，这样同宽的信封在高度序列里递减，不会被同时选进严格递增子序列
    order = sorted(envelopes, key=lambda e: (e[0], -e[1]))
    tails: list[int] = []                        # tails[k]：长度 k+1 的递增子序列的最小结尾高度
    for _, h in order:
        k = bisect_left(tails, h)                # 严格递增：相等的高度要替换，不能追加
        if k == len(tails):
            tails.append(h)
        else:
            tails[k] = h                         # 用更小的结尾替换，之后更容易接长
    return len(tails)
```

运行：`[[5,4],[6,4],[6,7],[2,3]]` → `3`，`[[1,1],[1,1],[1,1]]` → `1`；`[[1,1]]` → `1`，`[[4,5],[4,6],[6,7],[2,3],[1,1]]` → `4`，`[[1,3],[1,4],[1,5]]` → `1`。

**复杂度。** 时间 `O(n log n)`，空间 `O(n)`。

**拓展优化。**
- 还原具体的套娃链：`tails` 里存的改成排序后的下标，另用 `prev[i]` 记录 `i` 接在哪个下标后面，最后沿 `prev` 回溯。

```python
def max_envelopes_chain(envelopes: list[list[int]]) -> list[list[int]]:
    order = sorted(envelopes, key=lambda e: (e[0], -e[1]))
    tails: list[int] = []                        # tails[k]：长度 k+1 的链的最小结尾对应的 order 下标
    prev = [-1] * len(order)                     # prev[i]：链上排在 order[i] 前面的下标
    for i, (_, h) in enumerate(order):
        k = bisect_left(tails, h, key=lambda t: order[t][1])
        if k:
            prev[i] = tails[k - 1]
        if k == len(tails):
            tails.append(i)
        else:
            tails[k] = i
    chain: list[list[int]] = []
    i = tails[-1]
    while i != -1:                               # 从最长链的结尾倒着走回开头
        chain.append(order[i])
        i = prev[i]
    return chain[::-1]
```

- 三维（盒子套盒子）：不能再靠排序消维，需要 CDQ 分治或树套树。

**易错点。**
- 宽度相同时高度升序排：`[[1,3],[1,4],[1,5]]` 得到 `3`，正确是 `1`。
- `bisect_right` 代替 `bisect_left`：高度相等的信封被当成可以嵌套，`[[1,1],[2,1]]` 得到 `2`，正确是 `1`。
- 只按宽度排序、不处理同宽：同宽信封互相嵌套，答案偏大。

**追问。**
- 允许旋转信封：每个信封先把 `(w, h)` 规范成 `w <= h` 再排序，其余不变。
- 在线插入信封、随时查询最长链：不能再用排序技巧，改用平衡树或线段树维护。

**同模式。** LC 300 最长递增子序列、LC 646 最长数对链、LC 673 最长递增子序列的个数、LC 1626 无矛盾的最佳球队、LC 960 删列造序 III。
