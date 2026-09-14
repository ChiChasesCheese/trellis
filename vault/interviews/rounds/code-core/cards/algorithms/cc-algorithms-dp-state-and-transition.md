---
id: cc-algorithms-dp-state-and-transition
node: algorithms.dp
type: qa
---
## Q
What is the one sentence you must be able to say before writing any DP, and what does saying it fix?

## A
**"`dp[i][j]` is the best value of *…precisely defined…*, and it is reached from *…these earlier states…*."**

Saying it fixes four things at once: the table's dimensions, the base case, the loop order, and where the answer is read.

- If the sentence needs the word "somehow", the state is under-specified — usually a dimension is missing: remaining capacity, the last choice taken, a parity, how many segments are open.
- Loop order follows the dependency: every state a transition reads must already be final when it is read.
- Write the **answer's location** down too (`dp[n][K]`, or `max(dp[n])`). Reading the wrong cell is a silent wrong answer, not a crash, and it survives all your small tests.
- Say it out loud in an interview before coding; a wrong state gets corrected in ten seconds, a wrong table in ten minutes.

## Q zh
在写任何 DP 之前，你必须能说出的那一句话是什么？说出来又确定了什么？

## A zh
**「`dp[i][j]` 是*……精确定义……*的最优值，它由*……这些更早的状态……*转移而来。」**

说出这句话一次性确定四件事：表的维度、边界情况、循环顺序，以及答案从哪里读。

- 如果这句话里需要「不知怎么地」，说明状态定义不足 —— 通常是少了一个维度：剩余容量、上一次的选择、奇偶性、当前开着几段。
- 循环顺序跟随依赖：转移读到的每个状态，在被读时都必须已经定稿。
- 把**答案的位置**也写下来（`dp[n][K]`，或 `max(dp[n])`）。读错格子是静默的错误答案而不是崩溃，而且能扛过你所有的小测试。
- 面试时在写代码前把它说出来；状态说错十秒就能纠正，表写错要花十分钟。
