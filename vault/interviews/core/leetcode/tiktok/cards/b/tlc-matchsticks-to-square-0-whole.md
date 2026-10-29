---
id: tlc-matchsticks-to-square-0-whole
node: b.matchsticks-to-square
type: qa
---
## Q
**LC 473 火柴拼正方形**｜Medium · LC TikTok 热度 50/100 · CodeTop 国内累计 3 次 · 最近 2024-04-09（CodeTop）

给整数数组 `matchsticks`，`matchsticks[i]` 是第 `i` 根火柴棒的长度。要用**所有**火柴棒拼成一个正方形：不能折断火柴，可以把火柴首尾相连，每根火柴必须恰好用一次。能拼成返回 `true`，否则 `false`。`1 <= matchsticks.length <= 15`，`1 <= matchsticks[i] <= 10^8`。例：`[1,1,2,2,2]` → `true`（边长 `2`，每边两根或一根）；`[3,3,3,3,4]` → `false`。

给出完整的最优解答：识别、推导、代码、复杂度、易错点、追问。

## A
**一句话。** 总长必须被 `4` 整除，边长 `side = 总长 / 4`；把火柴**从长到短**依次放进 4 条边，任一条边放不下就剪枝，放不下就回溯。两个关键剪枝：长的先放；某一层里长度相同的边只试一次。

**识别。** 「把所有元素分成 `k` 组，每组和相等」是子集划分（k-way partition）；`n <= 15` 说明可以指数级搜索（回溯 `4^15`，或状态压缩 `2^15`）。它是 LC 416（分成 2 份）的推广：2 份时有位集 / 背包的多项式伪解，`k >= 3` 份是 NP 难，只能搜索。

**推导。** 暴力：每根火柴选 4 条边之一，`4^15 ≈ 10^9`，太慢 → 剪枝一：总和不被 `4` 整除，或最长火柴超过边长，直接 `False` → 剪枝二：先放最长的，它们最受限，失败得早 → 剪枝三：对称性。当前所有边中，长度相同的边是等价的，把这根火柴放进其中任何一条结果一样，只需试一次（尤其是开头四条都为 `0` 时，只试一条）。 → 备选：状态压缩 DP，`dp[mask]` 表示用掉 `mask` 里的火柴后，当前正在拼的那条边已有的长度，`O(2^n · n)`。

```python
def makesquare(matchsticks: list[int]) -> bool:
    total = sum(matchsticks)
    if total % 4:
        return False
    side = total // 4
    sticks = sorted(matchsticks, reverse=True) # 先放长的，更早发现放不下
    if sticks[0] > side:
        return False
    sides = [0] * 4                            # 四条边当前已经凑到的长度

    def dfs(i: int) -> bool:
        if i == len(sticks):
            return True                        # 总和是 4·side 且没有边超过 side，所以四条边都恰好是 side
        tried: set[int] = set()
        for j in range(4):
            if sides[j] + sticks[i] > side or sides[j] in tried:
                continue                       # 放不下；或长度相同的边已经试过（对称，结果一样）
            tried.add(sides[j])
            sides[j] += sticks[i]
            if dfs(i + 1):
                return True
            sides[j] -= sticks[i]
        return False

    return dfs(0)
```

运行：`[1,1,2,2,2]` → `True`，`[3,3,3,3,4]` → `False`，`[1]` → `False`，`[2,2,2,2]` → `True`，`[5,5,5,5,4,4,4,4,3,3,3,3,2,2,2]` → `False`；`[10^8] * 12` → `True`、`[10^8] * 15` → `False`；`300` 组随机的 `15` 根火柴最慢不到 `0.01` 秒。

**复杂度。** 时间最坏 `O(4^n)`，剪枝后实际远小（对称剪枝把第一根的 4 种选择降为 1 种）；空间 `O(n)` 递归深度。状压 DP：时间 `O(2^n · n)`，空间 `O(2^n)`。

**易错点。**
- 只检查总和能被 `4` 整除就返回 `True`：`[3,3,3,3,4]` 总和 `16`，边长 `4`，实际拼不出（`3 + 3 > 4`）。
- 不排序、不去重地回溯：结果对，但最坏会跑满 `4^15`。
- 贪心地把每根火柴放进第一个放得下的边、不回溯：`[9,9,4,4,3,3,2,2]`（边长 `9`）会失败返回 `False`，正确是 `True`（`9`、`9`、`4+3+2`、`4+3+2`）。

**追问。**
- 状压 DP：`dp[mask]` 记录这批火柴已拼出的长度（对 `side` 取模），按位枚举下一根能放进去的火柴（`dp[mask] + len <= side`）；`dp[全集] == 0` 即成功。它不需要排序，也不需要对称剪枝，最坏 `15 · 2^15 ≈ 5 · 10^5` 次操作。
- 分成 `k` 份（LC 698）：把 `4` 换成 `k`，对称剪枝同样有效。
- 要输出每条边由哪些火柴组成：回溯时把火柴编号存进各边的列表。

**同模式。** LC 698 划分为k个相等的子集、LC 416 分割等和子集、LC 1723 完成所有工作的最短时间、LC 2305 公平分发饼干。
