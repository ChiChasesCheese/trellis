---
id: tlc-first-day-where-you-have-been-in-all-the-rooms-0-whole
node: a.first-day-where-you-have-been-in-all-the-rooms
type: qa
---
## Q
**LC 1997 访问完所有房间的第一天**｜Medium · LC 字节 热度 88/100

有 `n` 个房间，编号 `0` 到 `n - 1`，日期从 `0` 开始，每天访问一个房间。第 `0` 天访问房间 `0`。给定长度为 `n` 的数组 `nextVisit`，规则是：如果今天访问房间 `i`，算上今天访问 `i` 的总次数为**奇数**，则第二天访问 `nextVisit[i]`；为**偶数**，则第二天访问 `(i + 1) mod n`。返回第一次访问完所有房间的日期，对 `10^9 + 7` 取余。`n == nextVisit.length`，`2 <= n <= 10^5`，`0 <= nextVisit[i] <= i`。例：`[0,0]` → `2`；`[0,0,2]` → `6`；`[0,1,2,0]` → `6`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 设 `first[i]` 是第一次到达房间 `i` 的日期。第一次到 `i` 时（奇数次）会被送回 `nextVisit[i]`，再把 `nextVisit[i]` 到 `i` 的路走一遍，第二次到 `i`（偶数次）后才能去 `i + 1`，于是 `first[i+1] = 2 * first[i] - first[nextVisit[i]] + 2`，答案是 `first[n-1]`。`O(n)`。

**识别。** 数据保证 `nextVisit[i] <= i`，说明只会往回跳；答案取模说明天数是指数增长的，不能模拟（`n = 10^5` 时天数远超可模拟的规模）。"到达下一个新房间需要多少天"是线性递推的信号，属于一维动态规划。

**推导。** 暴力：逐天模拟，天数最坏约 `2^n`。洞察：第一次走到房间 `i` 时，所有编号更小的房间都被访问了偶数次。因为你只在偶数次访问后才会前进，所以每个更小的房间都已"归零"，状态与第一次走到它们时相同。这时第 `first[i]` 天访问 `i`（第 1 次，奇数），第二天回到 `nextVisit[i]`，此后重走一遍从 `nextVisit[i]` 到 `i` 的路，花费与当初相同的 `first[i] - first[nextVisit[i]]` 天，第二次到达 `i`（偶数），再过一天到 `i + 1`。合计 `first[i+1] = first[i] + 1 + (first[i] - first[nextVisit[i]]) + 1`。

```python
def first_day_been_in_all_rooms(next_visit: list[int]) -> int:
    mod = 10**9 + 7
    n = len(next_visit)
    first = [0] * n                                # first[i] = 第一次到达房间 i 的日期
    for i in range(n - 1):
        # 第一次到 i（奇数次）-> 回到 nv = next_visit[i]，再走回 i 的时间是 first[i] - first[nv]
        # 第二次到 i（偶数次）-> 第二天去 i+1
        first[i + 1] = (2 * first[i] - first[next_visit[i]] + 2) % mod
    return first[-1]
```

运行：`[0,0]` → `2`，`[0,0,2]` → `6`，`[0,1,2,0]` → `6`；`n = 10^5` 且 `next_visit[i] = i` 时 → `199998`，`next_visit` 全 `0` 时 → `607723518`。

**复杂度。** 时间 `O(n)`；空间 `O(n)`：要按下标回查 `first[next_visit[i]]`，不能只留最近一个值。

**易错点。**
- 漏掉减去 `first[next_visit[i]]` 的一项，写成 `2 * first[i] + 2`：`[0,1,2,0]` 得到 `14`，正确是 `6`。
- 取模后的差可能为负。Python 的 `%` 对正模数总返回非负，所以 `(2 * first[i] - first[nv] + 2) % mod` 安全；C++ / Java 要写成 `(... + mod) % mod`。
- 答案是 `first[n-1]`，不是 `first[n]`：到达最后一个房间那天就已经访问完所有房间。

**追问。**
- 前缀和写法：设 `dp[i] = first[i+1] - first[i]`，则 `dp[i] = 1 + (first[i] - first[nv[i]]) + 1`，用前缀和可以去掉对任意下标的回查，思路等价。
- 想验证推导：对小的 `n` 直接模拟（每间房记访问次数，按奇偶决定下一个房间），和公式比较。
- 若 `nextVisit[i]` 可以大于 `i`，递推不再成立，需要重新分析状态。

**同模式。** LC 70 爬楼梯、LC 509 斐波那契数、LC 1137 第 N 个泰波那契数、LC 873 最长的斐波那契子序列的长度。
