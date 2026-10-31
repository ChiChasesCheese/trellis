---
id: tlc-maximum-points-you-can-obtain-from-cards-0-whole
node: c.maximum-points-you-can-obtain-from-cards
type: qa
---
## Q
**LC 1423 可获得的最大点数**｜Medium · LC TikTok 全时段热度 38/100 · CodeTop 国内累计 1 次 · 最近 2023-04-13（国内 CodeTop）

几张卡牌排成一行，点数由 `cardPoints` 给出。每次行动从行的开头或末尾拿一张牌，最终必须正好拿 `k` 张，点数是拿到的牌的点数之和，返回最大点数。`1 <= cardPoints.length <= 10^5`，`1 <= cardPoints[i] <= 10^4`，`1 <= k <= cardPoints.length`。例：`cardPoints = [1,2,3,4,5,6,1], k = 3` → `12`（拿右边三张 `1+6+5`）；`cardPoints = [9,7,7,9,7,7,9], k = 7` → `55`；`cardPoints = [1,1000,1], k = 1` → `1`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 拿走的是「左边一段 + 右边一段」，留下的是中间一段长度固定为 `n - k` 的连续子数组；拿走的点数最大等价于留下的窗口和最小，滑动窗口一次扫完。

**识别。** 「只能从两端拿」的反面是「中间连续一段不拿」；固定长度的连续子数组求最值，就是定长滑动窗口。

**推导。** 暴力：枚举左边拿 `i` 张，每次重新求和，`O(k^2)`。浪费：相邻两种拿法只差一张牌。洞察：拿走的总和 = 全部总和 - 留下窗口的和，窗口长度固定为 `n - k`，窗口右移一格只加一个减一个。

```python
def max_score(card_points: list[int], k: int) -> int:
    n = len(card_points)
    window = n - k                               # 没被拿走的牌是一段长度 n-k 的连续子数组
    cur = sum(card_points[:window])
    smallest = cur
    for i in range(window, n):                   # 滑动窗口：加入右端新元素、移出左端旧元素
        cur += card_points[i] - card_points[i - window]
        smallest = min(smallest, cur)
    return sum(card_points) - smallest           # 拿走的总点数 = 全部 - 留下的最小窗口
```

运行：`[1,2,3,4,5,6,1]`, `k = 3` → `12`；`[2,2,2]`, `k = 2` → `4`；`[9,7,7,9,7,7,9]`, `k = 7` → `55`；`[1,1000,1]`, `k = 1` → `1`；`[1,79,80,1,1,1,200,1]`, `k = 3` → `202`。

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**拓展优化。**
- 不转化为补集，直接维护「左 `i` 张 + 右 `k - i` 张」，每步把一张右牌换成一张左牌，同样 `O(k)`：

```python
def max_score_two_ends(card_points: list[int], k: int) -> int:
    n = len(card_points)
    cur = sum(card_points[n - k:])               # 先全从右边拿 k 张
    best = cur
    for i in range(k):                           # 依次把右边的一张换成左边的一张
        cur += card_points[i] - card_points[n - k + i]
        best = max(best, cur)
    return best
```

- 有负数点数时两种写法都仍然成立；若每次必须取到不同规则（如还要取中间牌），需要改用 DP。

**易错点。**
- `k == n` 时窗口长度为 `0`：`sum(card_points[:0])` 为 `0`，循环不执行，返回总和（示例三 `55`）；不要对空窗口求 `min`。
- 窗口长度写成 `k`：留下窗口的长度是 `n - k`，写错会得到「拿中间 `k` 张」的答案。
- 贪心每次拿两端较大的一张（相等取左）：`[1,2,3,4,5,6,1]`, `k = 3` 得到 `1+2+3 = 6`，正确答案是 `12`；眼前最大不等于总和最大。

**追问。**
- 返回具体拿法：记录最小窗口的起点，左边拿 `start` 张，右边拿 `k - start` 张。
- 两个人轮流拿（博弈）：改成区间 DP `dp[l][r]`，见预测赢家 LC 486。

**同模式。** LC 643 子数组最大平均数 I、LC 209 长度最小的子数组、LC 1658 将 x 减到 0 的最小操作数、LC 1004 最大连续 1 的个数 III、LC 53 最大子数组和。
