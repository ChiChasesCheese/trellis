---
id: lct-learn-dp-9-7
node: dp.9.7
type: qa
step: 1
---
## Q
**动态规划 › 状态压缩 DP（状压 DP） › 其他状压 DP**｜学习卡

套路是什么？

## A
**一句话。** 状压 DP：`mask` 记录已经用掉的元素集合，状态值只记「还需要知道的那一点」（桶里已装量、已用贴纸数），每次往 `mask` 里加一个元素转移。

下图：LC 698，`mask` 记录用过哪些数，状态值只记当前这个桶装了多少。

<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 340 150">
<rect x="20" y="30" width="22" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="31" y="46" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0</text>
<rect x="42" y="30" width="22" height="24" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<text x="53" y="46" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">0</text>
<rect x="64" y="30" width="22" height="24" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="75" y="46" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1</text>
<rect x="86" y="30" width="22" height="24" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="97" y="46" text-anchor="middle" font-size="11" font-family="sans-serif" fill="currentColor">1</text>
<text x="20" y="22" text-anchor="start" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">mask：已放进桶的数</text>
<rect x="150" y="26" width="30" height="70" rx="3" fill="none" stroke="currentColor" stroke-width="1.2"/>
<rect x="150" y="61" width="30" height="35" rx="3" stroke="currentColor" style="fill:var(--chip,rgba(59,111,212,0.12))" stroke-width="1.2"/>
<text x="165" y="110" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">f[mask]</text>
<text x="165" y="124" text-anchor="middle" font-size="10" font-family="sans-serif" style="fill:var(--dim,#6b7280)">当前桶已装量</text>
<text x="200" y="40" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">再放 x：</text>
<text x="200" y="56" text-anchor="start" font-size="11" font-family="sans-serif" fill="currentColor">超过 t → 不行</text>
<text x="200" y="72" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">恰好满 → 模 t 清零</text>
<text x="200" y="88" text-anchor="start" font-size="11" font-family="sans-serif" style="fill:var(--accent,#3b6fd4)">开始装下一个桶</text>
<text x="170" y="144" text-anchor="middle" font-size="11" font-family="sans-serif" style="fill:var(--dim,#6b7280)">状态值只记「还需要知道的那一点」；f[全集] == 0 即可行</text>
</svg>

```python
def can_partition(nums, k):          # 698
    s = sum(nums)
    if s % k:
        return False
    t = s // k                       # 每个桶的目标和
    nums.sort()
    if nums[-1] > t:
        return False
    n = len(nums)
    f = [-1] * (1 << n)              # 当前桶已装量，-1 不可达
    f[0] = 0
    for mask in range(1 << n):
        if f[mask] < 0:
            continue
        for i, x in enumerate(nums):
            if f[mask] + x > t:
                break                # 升序：后面的更放不下
            if mask >> i & 1 == 0 and f[mask | 1 << i] < 0:
                f[mask | 1 << i] = (f[mask] + x) % t  # 满则清零
    return f[-1] == 0
```

**要点。**
- 为什么对？：`mask` 里数的总和确定，当前桶已装量就是总和对 `t` 取余，只依赖 `mask`，所以每个 `mask` 记一个值（可达与否）就够。
- LC 691 怎么改？：`dp[mask]` 是盖住 `target` 中 `mask` 位置的最少贴纸数，只处理最低的未覆盖位，枚举含该字母的贴纸，能盖多少盖多少，`dp[new] = min(dp[new], dp[mask] + 1)`。

**易错点。**
- 用 `0` 表示不可达：`0` 是合法状态（空桶或刚装满），要用 `-1`。
- 不检查 `sum % k`：`[1,1,1,1,1,1]`、`k = 4`，`t` 取整成 `1`，错返回 `true`。
- LC 691 贪心选覆盖最多的贴纸：`["cf","bf","fffb","aaef"]`、`"ffccfc"` 贪心得 `4`，正确是 `3`。

**对应题目。** LC 691 贴纸拼词、LC 698 划分为k个相等的子集
