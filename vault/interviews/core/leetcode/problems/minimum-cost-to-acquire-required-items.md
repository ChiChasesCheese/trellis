---
slug: minimum-cost-to-acquire-required-items
---
## Q
**LC 3789 采购的最小花费**｜Medium

物品 1 花 `cost1` 满足需求 1 一个单位，物品 2 花 `cost2` 满足需求 2 一个单位，物品 3 花 `costBoth` 两种需求各满足一个单位。求需求 1 至少 `need1`、需求 2 至少 `need2` 的最小总花费，`need <= 10^9`。

## A
**一句话。** 花费是物品 3 件数的分段线性函数，最小值只在拐点 `0`、`min(need)`、`max(need)` 取到，三者取最小。

```python
def min_cost(cost1, cost2, cost_both, need1, need2):
    lo, hi = sorted((need1, need2))
    # 物品 3 只有三个候选件数：0、lo、hi
    return min(
        need1 * cost1 + need2 * cost2,
        # 成对买 lo 件，多出的那一类单买
        lo * cost_both + (need1 - lo) * cost1
        + (need2 - lo) * cost2,
        hi * cost_both)     # 全买物品 3，较少的一类溢出
```

**复杂度。** 时间 `O(1)`，空间 `O(1)`。

**易错点。**
- 漏掉全买物品 3：`cost1=3, cost2=2, costBoth=1, need1=3, need2=2` 得 `5`，应为 `3`（需求可以超额）。
- 漏掉成对买 `lo` 件：`cost1=5, cost2=5, costBoth=6, need1=1, need2=3` 得 `18`，应为 `16`。
- 枚举物品 3 的件数：`need` 到 `10^9`，超时。

**追问。**
- 为什么只看三个点？：件数每加一，在 `[0, lo]` 省 `cost1 + cost2 - costBoth`，在 `[lo, hi]` 省单类价减 `costBoth`，每段斜率不变。

**同模式。** LC 2706 购买两块巧克力、LC 1217 玩筹码、LC 134 加油站、LC 122 买卖股票的最佳时机 II
