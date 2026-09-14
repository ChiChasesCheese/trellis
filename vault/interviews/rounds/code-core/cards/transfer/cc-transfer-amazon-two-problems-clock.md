---
id: cc-transfer-amazon-two-problems-clock
node: transfer.amazon
type: qa
---
## Q
Two algorithm problems, one shared timer, and one is clearly harder. How do you allocate?

## A
**Read both before starting, then bank the easier one.** With a single clock across two problems, the dominant failure is sinking everything into the hard one and submitting nothing.

- Budget by halves and hold the line: move on at the boundary even when you feel close. "Close" is where the remaining time goes.
- Submit a working brute force for the second problem before attempting the optimal one — a passing partial beats an unfinished optimum, and the brute force is also your oracle ([[cc-verification-invariant-brute-force-oracle]]).
- These are named patterns rather than bespoke specs, so reading time is short and typing time dominates. That makes raw language fluency worth more here than in a spec-heavy round ([[cc-python-portability-language-cost]]).

## Q zh
两道算法题，共用一个计时器，其中一道明显更难。怎么分配？

## A zh
**开始之前先把两道都读一遍，然后先把简单那道落袋。** 两题共用一个时钟时，最主要的失败方式是把全部时间砸进难的那道、最后什么都没交。

- 按一半一半分配预算并守住：到点就走，哪怕感觉「快好了」。「快好了」正是剩余时间的去处。
- 在尝试最优解之前，先给第二题交一个能跑的暴力解 —— 能过的部分胜过没写完的最优解，而且这个暴力解还是你的 oracle（[[cc-verification-invariant-brute-force-oracle]]）。
- 这些是有名字的套路而非定制规格，所以阅读时间短、敲键盘时间占主导。这让纯粹的语言熟练度在这里比在重规格的轮次里更值钱（[[cc-python-portability-language-cost]]）。
