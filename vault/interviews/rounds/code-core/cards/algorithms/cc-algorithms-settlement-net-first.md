---
id: cc-algorithms-settlement-net-first
node: algorithms.settlement
type: qa
---
## Q
10^5 transactions among 50 parties, then "settle up". What is the first step, and what does it buy?

## A
**Net every party to a single balance before planning any transfer**, then drop every party whose net is 0.

```python
for frm, to, amount in transactions:
    net[frm] = net.get(frm, 0) + amount
    net[to]  = net.get(to, 0) - amount
```

- The number of transactions stops mattering: an expensive search then runs over ~10 numbers, not 10^5 ([[cc-algorithms-settlement-min-transfers]]).
- **Pass-through parties** — who paid and were paid the same total — net to zero and must not appear in the output at all.
- Get the direction right: `[a, b, x]` usually means "a handed x to b", so **b owes a**. Reversing it reverses every transfer in the answer, and the sample will not catch it if it is symmetric.
- The nets always sum to zero. Asserting that catches a parsing sign error immediately, and costs one line ([[cc-algorithms-settlement-floor-and-feasibility]]).

## Q zh
50 个当事方之间有 10^5 笔交易，然后要「清账」。第一步是什么，它带来什么？

## A zh
**在规划任何转账之前，先把每一方净额化为单个余额**，然后丢掉所有净额为 0 的当事方。

```python
for frm, to, amount in transactions:
    net[frm] = net.get(frm, 0) + amount
    net[to]  = net.get(to, 0) - amount
```

- 交易数量不再重要：昂贵的搜索此后只在约 10 个数上进行，而不是 10^5（[[cc-algorithms-settlement-min-transfers]]）。
- **过手方** —— 付出与收到总额相同的人 —— 净额为零，必须完全不出现在输出里。
- 方向要弄对：`[a, b, x]` 通常表示「a 交给 b 金额 x」，所以**是 b 欠 a**。搞反会让答案里的每笔转账都反向，而样例若是对称的就抓不住它。
- 净额之和恒为零。断言这一点能立刻抓出解析时的符号错误，只需一行（[[cc-algorithms-settlement-floor-and-feasibility]]）。
