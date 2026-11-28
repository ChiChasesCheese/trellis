---
id: lct-learn-dp-8-2
node: dp.8.2
type: qa
step: 1
---
## Q
**动态规划 › 区间 DP › 区间 DP**｜学习卡

套路是什么？

## A
**一句话。** 区间 DP 的通用拆法：枚举区间里「最后一个」被处理的元素（或切点）`k`，它把区间分成互不影响的左右两段，`f(i, j) = max/min/sum(f(i, k) + f(k, j) + 合并代价)`。

下图：LC 312，枚举开区间里最后一个处理的 `k`，它把区间拆成互不影响的两半。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 140">
<rect x="20" y="50" width="50" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="45.0" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">1</text>
<rect x="70" y="50" width="50" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="95.0" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">3</text>
<rect x="120" y="50" width="50" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="145.0" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">1</text>
<rect x="170" y="50" width="50" height="28" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="195.0" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">5</text>
<rect x="220" y="50" width="50" height="28" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="245.0" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" fill="currentColor">8</text>
<rect x="270" y="50" width="50" height="28" rx="3" style="fill:var(--chip,rgba(59,111,212,0.12));stroke:var(--accent,#3b6fd4)" stroke-width="1.2"/>
<text x="295.0" y="68.0" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">1</text>
<line x1="45.0" y1="34" x2="45.0" y2="48" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="45.0,48.0 42.0,41.7 48.0,41.7" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="45.0" y="30" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">i</text>
<line x1="195.0" y1="34" x2="195.0" y2="48" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="195.0,48.0 192.0,41.7 198.0,41.7" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="195.0" y="30" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">k 最后戳</text>
<line x1="295.0" y1="34" x2="295.0" y2="48" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<polygon points="295.0,48.0 292.0,41.7 298.0,41.7" style="fill:var(--accent,#3b6fd4);stroke:var(--accent,#3b6fd4)" stroke-width="0.5"/>
<text x="295.0" y="30" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">j</text>
<line x1="45.0" y1="84" x2="45.0" y2="90" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="195.0" y1="84" x2="195.0" y2="90" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="45.0" y1="84" x2="195.0" y2="84" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="120.0" y="100" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">f(i, k)</text>
<line x1="195.0" y1="84" x2="195.0" y2="90" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="295.0" y1="84" x2="295.0" y2="90" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<line x1="195.0" y1="84" x2="295.0" y2="84" stroke-width="1.2" style="stroke:var(--accent,#3b6fd4)"/>
<text x="245.0" y="100" text-anchor="middle" font-size="12" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">f(k, j)</text>
<text x="170" y="122" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">k 最后戳破时邻居只剩 a[i]、a[j]：得 a[i]·a[k]·a[j]</text>
<text x="170" y="138" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">两侧互不影响，各自是更小的区间</text>
</svg>

```python
def max_coins(nums):                 # LC 312 戳气球
    a = [1] + nums + [1]             # 两端补虚拟气球

    @cache
    def dfs(i, j):                   # 戳光开区间 (i, j) 的最大金币
        res = 0
        for k in range(i + 1, j):    # k 是最后一个戳破的
            # 此时 i、j 还在，所以 k 的邻居固定是 a[i]、a[j]
            res = max(res, dfs(i, k) + dfs(k, j) +
                      a[i] * a[k] * a[j])
        return res

    return dfs(0, len(a) - 1)
```

**要点。**
- 为什么对？：若枚举「第一个戳破的」，剩下左右两段会因邻居改变而互相牵连；改成「最后一个」，左右两段各自的边界 `i`、`j` 始终存在，子问题互相独立。
- LC 96 怎么改？：计数型：枚举根 `i`，左右子树方案数相乘，`G(n) = Σ G(i - 1) * G(n - i)`，`G(0) = G(1) = 1`。
- LC 87 怎么改？：状态是两个等长子串（起点 `i1, i2`，长 `L`），枚举切点，不交换则左对左，交换则前段对后段；字符计数不同直接剪枝。
- 写成递推怎么改？：按区间长度从小到大，`i` 倒序、`j` 正序都可以，只要保证 `dp[i][k]`、`dp[k][j]` 先算好。

**易错点。**
- 枚举第一个戳破的：邻居随删除而变，子问题不独立，转移写不出来。
- 区间开闭不一致：开区间 `(i, j)` 时 `k` 取 `i + 1 .. j - 1`，结果在 `dfs(0, n + 1)`。
- 忘了补两端的 `1`：`[5]` 应得 `5`。

**对应题目。** LC 312 戳气球、LC 87 扰乱字符串、LC 96 不同的二叉搜索树
