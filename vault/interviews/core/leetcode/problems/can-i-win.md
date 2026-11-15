---
slug: can-i-win
---
## Q
**LC 464 我能赢吗**｜Medium

两人轮流从 `1..maxChoosableInteger` 中选一个没被选过的数，累加到总和，先让总和达到或超过 `desiredTotal` 的人赢。先手能否必赢？

## A
**一句话。** 状态是「已选集合的位掩码」（剩余和由掩码决定），先手赢当且仅当存在一个数，选完直接达标，或使后手落入必输态。

```python
def can_i_win(maxChoosableInteger, desiredTotal):
    m = maxChoosableInteger
    if m * (m + 1) // 2 < desiredTotal:
        return False                  # 全选完也到不了
    @cache
    def win(mask, left):              # 轮到我，还差 left
        for x in range(1, m + 1):
            if mask >> x & 1:
                continue              # 已被选过
            nxt = mask | 1 << x
            if x >= left or not win(nxt, left - x):
                return True           # 直接赢，或对手必输
        return False
    return win(0, desiredTotal)
```

**复杂度。** 时间 `O(2^m · m)`，空间 `O(2^m)`。

**易错点。**
- 没有判「全选也凑不到」：此时没人能赢，应返回 `False`，不然搜索会得出错误的胜负。
- 记忆化的键里带上 `left`：`left` 由 `mask` 唯一确定，冗余但无害，只用 `mask` 作键也可。
- `desiredTotal <= 0`：先手第一步就达标，`x >= left` 已覆盖。

**追问。**
- 为什么记忆化键只需 `mask`？：已选的数之和固定，剩余和等于 `desiredTotal` 减去它。
- 想知道必赢的第一步呢？：外层循环再试每个 `x`，返回第一个使对手必输的。

**同模式。** LC 877 石子游戏、LC 486 预测赢家、LC 294 翻转游戏 II、LC 526 优美的排列
