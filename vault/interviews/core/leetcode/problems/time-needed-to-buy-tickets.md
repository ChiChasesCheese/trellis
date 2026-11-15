---
slug: time-needed-to-buy-tickets
---
## Q
**LC 2073 买票需要的时间**｜Easy

`n` 个人排队买票，每秒队首的人买一张，买完还需要的话回到队尾，不需要就离开。`tickets[i]` 是第 `i` 个人要买的数量。求第 `k` 个人买完所需的秒数。

## A
**一句话。** 不用模拟：每个人在第 `k` 个人买完之前最多买 `tickets[k]` 张；排在 `k` 后面的人在最后一轮到不了，最多买 `tickets[k] - 1` 张。

```python
def time_required_to_buy(tickets, k):
    t = tickets[k]
    return sum(min(x, t) if i <= k else min(x, t - 1)
               for i, x in enumerate(tickets))
```

**复杂度。** 时间 `O(n)`，空间 `O(1)`。

**易错点。**
- 后面的人也用 `min(x, t)`：第 `k` 个人买完最后一张时，排在他后面的人这一轮还没轮到。
- 直接模拟：票数大时会超时，答案有公式。

**追问。**
- 怎么直接模拟？：用 `deque` 存（下标，剩余），每秒弹队首减一，没买完再入队尾。

**同模式。** LC 1535 找出数组游戏的赢家、LC 1823 找出游戏的获胜者
