---
id: tlc-tops-optimal-account-balancing-0-whole
node: backtracking.optimal-account-balancing
type: qa
---
## Q
**LC 465 最优账单平衡**｜Hard · 全公司热度第 180 名

给你一个交易数组 `transactions`，其中 `transactions[i] = [from, to, amount]` 表示编号为 `from` 的人给编号为 `to` 的人 `amount` 美元。求让所有人账目平衡（每个人最终既不欠钱也不被欠）所需要的**最少转账笔数**；转账可以在任意两人之间进行，金额任意。`1 <= transactions.length <= 8`，`transactions[i].length == 3`，`0 <= from, to < 12`，`from != to`，`1 <= amount <= 100`。例：`[[0,1,10],[2,0,5]]` → `2`；`[[0,1,10],[1,0,1],[1,2,5],[2,0,5]]` → `1`。

给出完整的最优解答：考点、识别、推导、代码、复杂度、易错点。

## A
**考点。** 净额化（net balance）+ 回溯搜索（backtracking）：每次让第一个未结清的人和一个符号相反的人对冲。

**一句话。** 先把交易压成每个人的净余额，丢掉为 `0` 的人；然后 DFS：取第一个未结清的人，尝试让他把账全部转给每一个符号相反的人，递归求剩余的最少笔数，取最小。

**识别。** 「最少转账笔数」「人数很少（`< 12`）」「结果与原来谁欠谁无关，只与净额有关」= 先净额化，再对 `m <= 12` 个非零余额做指数级搜索（回溯或状态压缩）。

**推导。** 一笔转账能让一个人彻底结清，而一个子集的余额之和为 `0` 时，内部转账 `大小 - 1` 笔即可结清，所以答案 = 非零人数 `m` − 最多能拆出的"和为 `0` 的不相交小组"个数。回溯做法：看第 `i` 个人，他必须跟某个符号相反的人 `j` 对冲一次（不然永远结不清），把他的全部余额转给 `j`，`j` 的余额变成 `debts[j] + debts[i]`，第 `i` 个人结清，递归处理 `i + 1`。余额值相同的两个人转移后的局面一样，同一层里同一个值只试一次（剪枝）。

```python
from collections import defaultdict
from math import inf


def min_transfers(transactions: list[list[int]]) -> int:
    balance: defaultdict[int, int] = defaultdict(int)
    for src, dst, amount in transactions:
        balance[src] -= amount  # 付出的人净余额减少（欠别人）
        balance[dst] += amount  # 收到的人净余额增加（被别人欠）
    debts = [b for b in balance.values() if b != 0]  # 只有非零余额的人需要转账

    def dfs(i: int) -> int:
        """debts[:i] 已全部结清，返回结清 debts[i:] 最少需要的笔数。"""
        while i < len(debts) and debts[i] == 0:  # 被前面的对冲顺带结清的人跳过
            i += 1
        if i == len(debts):
            return 0
        best = inf
        seen: set[int] = set()  # 同一层里相同余额的人效果一样，只试一次
        for j in range(i + 1, len(debts)):
            if debts[j] * debts[i] < 0 and debts[j] not in seen:  # 符号相反才能对冲
                seen.add(debts[j])
                debts[j] += debts[i]  # i 把全部余额转给 j：i 结清，j 的余额合并
                best = min(best, 1 + dfs(i + 1))
                debts[j] -= debts[i]  # 回溯
        return best

    return dfs(0)
```

运行：`[[0,1,10],[2,0,5]]` → `2`；`[[0,1,10],[1,0,1],[1,2,5],[2,0,5]]` → `1`；`[[1,4,8],[3,0,6],[5,0,7]]` → `3`；`[[0,1,5],[1,0,5]]` → `0`；`[[0,1,3],[1,2,3],[2,0,3]]` → `0`。

**复杂度。** 最坏 `O((m - 1)!)`，`m <= 12` 且有剪枝，实际远小于；空间 `O(m)`。

**拓展优化。**
- 状态压缩 DP：`best[mask]` 表示子集 `mask` 里最多拆出几个和为 `0` 的不相交小组，`best[mask]` 取"去掉一个人"的最大值，若 `mask` 的余额和为 `0` 再加 `1`，答案 `m - best[全集]`，时间 `O(2^m * m)`，不依赖搜索顺序：

```python
from collections import defaultdict


def min_transfers_mask(transactions: list[list[int]]) -> int:
    balance: defaultdict[int, int] = defaultdict(int)
    for src, dst, amount in transactions:
        balance[src] -= amount
        balance[dst] += amount
    debts = [b for b in balance.values() if b != 0]
    m = len(debts)
    total = [0] * (1 << m)  # total[mask]：子集 mask 的余额之和
    best = [0] * (1 << m)   # best[mask]：mask 里最多的和为 0 的不相交小组数
    for mask in range(1, 1 << m):
        low = (mask & -mask).bit_length() - 1  # 最低位的人
        total[mask] = total[mask & (mask - 1)] + debts[low]
        best[mask] = max(best[mask ^ (1 << i)] for i in range(m) if mask >> i & 1)
        if total[mask] == 0:
            best[mask] += 1
    return m - best[(1 << m) - 1]
```

**易错点。**
- 贪心地让最大的债务人还给最大的债权人：`[[1,4,8],[3,0,6],[5,0,7]]` 贪心需要 `4` 笔，正确是 `3`（`1`、`4` 一组 `1` 笔，`3`、`5`、`0` 一组 `2` 笔）。
- 不净额化，直接数交易笔数：示例 2 里有 `4` 笔交易，答案只要 `1` 笔（`0` 的净余额 `-4`，`1` 的 `+4`，`2` 的 `0`）。
- 回溯完忘了还原 `debts[j]`：后面分支读到被污染的余额，`[[2,5,7],[3,2,7],[2,1,3]]` 返回 `3`，正确是 `2`；用 `debts[j] -= debts[i]` 精确复原。

**同模式。** LC 1307 口算难题、LC 698 划分为 k 个相等的子集、LC 996 平方数组的数目、LC 847 访问所有节点的最短路径。
