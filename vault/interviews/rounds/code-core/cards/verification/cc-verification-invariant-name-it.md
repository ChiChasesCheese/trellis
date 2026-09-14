---
id: cc-verification-invariant-name-it
node: verification.invariants
type: qa
---
## Q
You have just written the state for a ledger and are about to write the rules. What one sentence do you produce first, and what do you do with it?

## A
**Name the invariant: a property that must hold after every event, stated in one sentence with no "usually".**

- "The sum of all balances equals the sum of all postings."
- "Every active connection appears in exactly one target's member list."
- "`fraud_count <= total_count` for every account."

Write it as a comment above the state, then as an `assert` in a helper your tests call. An invariant you can state is a bug you can catch on a random input; one you cannot state usually means the state holds the same fact in two places. It is also what tells you exactly what a reversal has to undo.

## Q zh
你刚写完一个账本的状态，正要开始写规则。你首先要产出哪一句话？拿它做什么？

## A zh
**点名不变量：一条在每个事件之后都必须成立的性质，用一句话说清，不带「通常」。**

- 「所有余额之和等于所有分录之和。」
- 「每个活跃连接恰好出现在一个目标的成员列表里。」
- 「对每个账户都有 `fraud_count <= total_count`。」

把它写成状态上方的注释，再写成一个供测试调用的辅助函数里的 `assert`。你说得出的不变量就是你能在随机输入上抓到的 bug；说不出来，通常意味着状态在两个地方存了同一个事实。它也正好告诉你冲正到底要撤销什么。
