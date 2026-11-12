---
slug: matchsticks-to-square
---
## Q
**LC 473 火柴拼正方形**｜Medium

用数组 `matchsticks` 的所有火柴首尾相连拼成正方形，每根恰好用一次，能否做到。

## A
**一句话。** 回溯：火柴从长到短依次放进 4 条边，同一层里长度相同的边只试一次。

```python
def makesquare(matchsticks):
    total = sum(matchsticks)
    if total % 4:
        return False
    side = total // 4
    a = sorted(matchsticks, reverse=True)   # 长的先放
    if a[0] > side:
        return False
    sides = [0] * 4
    def dfs(i):
        if i == len(a):
            return True
        tried = set()
        for j in range(4):
            if sides[j] + a[i] > side or sides[j] in tried:
                continue                    # 放不下 / 对称已试过
            tried.add(sides[j])
            sides[j] += a[i]
            if dfs(i + 1):
                return True
            sides[j] -= a[i]
        return False
    return dfs(0)
```

**复杂度。** 时间 最坏 `O(4^n)`（剪枝后远小），空间 `O(n)`。

**易错点。**
- 只检查总和被 `4` 整除：`[3,3,3,3,4]` 总和 `16`，却拼不出。
- 不排序、不去重地回溯：最坏跑满 `4^15`。
- 把火柴贪心放进第一个放得下的边、不回溯：`[9,9,4,4,3,3,2,2]` 会误判为 `False`。

**追问。**
- 状压 DP 怎么做？：`dp[mask]` 记已拼长度对 `side` 取模，枚举下一根使 `dp[mask] + len <= side`，`dp[全集] == 0` 即成功。
- 分成 `k` 份（LC 698）？：把 `4` 换成 `k`，对称剪枝同样有效。

**同模式。** LC 698 划分为k个相等的子集、LC 416 分割等和子集、LC 1723 完成所有工作的最短时间
