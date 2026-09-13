---
id: leetcode-q-stone-game-ix-pattern
node: dp-game-probability.zero-sum-game
type: qa
anki: 1787102261781
tags: [lc::2029, leetcode, pattern, recall]
---
## Q
Stone Game IX（2029）：如何用余数分类 + 计数判断先手是否必胜？

## A
将所有石子按 val % 3 分为三类，统计 cnt0（余0）、cnt1（余1）、cnt2（余2）的个数。核心不变量：真正影响胜负走向的是石子取值的余数序列，余0的石子只是“占位”（不改变当前累计和的余数，但会白白消耗一个回合），因此只需讨论 cnt0 的奇偶性：
- 若 cnt0 为偶数：Alice 必胜当且仅当 cnt1 >= 1 且 cnt2 >= 1（双方都必须避免让累计和被 3 整除，一旦 cnt1、cnt2 都存在，先手可以掌控节奏迫使对方送出必输局面）；
- 若 cnt0 为奇数：多出的一个 cnt0 会把先后手身份翻转一次，此时胜负条件变为 abs(cnt1 - cnt2) > 2。
复杂度 O(n) 时间、O(1) 空间，属于纯计数 + 博弈论结论题，不需要显式 DP/递归。

**Evidence**

```
class Solution:
    def stoneGameIX(self, stones: List[int]) -> bool:
        cnt0 = cnt1 = cnt2 = 0
        for val in stones:
            if (typ := val % 3) == 0:
                cnt0 += 1
            elif typ == 1:
                cnt1 += 1
            else:
                cnt2 += 1
        if cnt0 % 2 == 0:
            return cnt1 >= 1 and cnt2 >= 1
        return abs(cnt1 - cnt2) > 2
```

[原文 ↗](obsidian://open?vault=lc&file=questions%2F2029%20-%20Stone%20Game%20IX)
