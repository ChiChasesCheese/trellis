---
slug: optimal-account-balancing
---
## Q
**LC 465 最优账单平衡**｜Hard

`transactions[i] = [from, to, amount]` 表示 `from` 给 `to` 转了 `amount`。求让所有人账目归零所需的最少转账笔数（`<= 12` 人，`<= 8` 笔交易）。

## A
**一句话。** 先算每人净余额并丢掉 `0`，再 DFS：取第一个未结清的人，试着把他的账全转给每个符号相反的人。

```python
def min_transfers(transactions):
    bal = defaultdict(int)
    for src, dst, amt in transactions:
        bal[src] -= amt
        bal[dst] += amt
    debts = [b for b in bal.values() if b]

    def dfs(i):
        while i < len(debts) and debts[i] == 0:
            i += 1             # 被对冲顺带结清的人跳过
        if i == len(debts):
            return 0
        best = inf
        seen = set()           # 同层相同余额只试一次
        for j in range(i + 1, len(debts)):
            d = debts[j]
            if d * debts[i] < 0 and d not in seen:
                seen.add(d)
                debts[j] += debts[i]   # i 转给 j，i 结清
                best = min(best, 1 + dfs(i + 1))
                debts[j] -= debts[i]   # 回溯
        return best

    return dfs(0)
```

**复杂度。** 时间 `O((m-1)!)`（有剪枝，实际远小），空间 `O(m)`。

**易错点。**
- 贪心：最大债务人还给最大债权人：`[[1,4,8],[3,0,6],[5,0,7]]` 需 `4` 笔，最优 `3` 笔。
- 不先算净余额、直接数交易笔数：示例 2 有 `4` 笔交易，答案只要 `1` 笔。
- 回溯后忘了还原 `debts[j]`：后面分支读到被污染的余额。

**追问。**
- 为什么贪心不行？：最优解是把余额拆成尽可能多的零和小组，贪心每步只结清一个人。
- 有更稳的做法吗？：状压 DP，`dp[mask]` 为 `mask` 内能拆出的最多零和组数，`O(2^m·m)`。

**同模式。** LC 698 划分为 k 个相等的子集、LC 1307 口算难题、LC 847 访问所有节点的最短路径
