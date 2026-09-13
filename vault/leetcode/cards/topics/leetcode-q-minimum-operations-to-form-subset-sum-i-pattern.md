---
id: leetcode-q-minimum-operations-to-form-subset-sum-i-pattern
node: topics.uncategorised
type: qa
anki: 1788391211599
tags: [lc::4040, leetcode, pattern, recall]
---
## Q
给定数组nums,每个元素可反复乘2(必须先做完所有乘法再做除法),floor除2,每次操作代价1,求某个子集经过操作后和恰为sum的最小操作数,如何解?

## A
两层处理:①对每个num单独展开其“可达值→最小代价”的映射——先枚举所有乘法倍数(x=num,num*2,num*4,...直到超过2*sum就停),再对每个倍数做除法链(不断//2直到0),记录每个可达值(不超过sum)的最小mul+div代价;②把问题转化为0/1背包:dp[s]表示凑出和s的最小总代价,dp[0]=0,对每个num的选项列表(value,cost)做一次“每个物品只能选一种取值”的背包转移(逆序遍历current避免同一物品重复使用),最终答案是dp[sum]。核心思想是把“单个数的可达状态空间”与“多个数的组合选择”解耦成两步。

**Evidence**

```
for num in nums:
    cur = dict()
    x, mul = num, 0
    while True:
        y, div = x, 0
        while y:
            if y <= sum:
                cur[y] = min(cur.get(y, inf), mul + div)
            y //= 2
            div += 1
        if x > 2 * sum:
            break
        x *= 2
        mul += 1
    choices.append(list(cur.items()))
dp = [inf] * (sum + 1)
dp[0] = 0
for options in choices:
    for current in range(sum, -1, -1):
        ...
```

[原文 ↗](obsidian://open?vault=lc&file=questions%2F4040%20-%20Minimum%20Operations%20to%20Form%20Subset%20Sum%20I)
