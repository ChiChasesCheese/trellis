---
id: cc-transfer-oa-partial-credit
node: transfer.stripe-oa
type: qa
---
## Q
Fifteen minutes left. Part 4 is half-written; parts 1–3 pass. What is the correct move, and what does the scoring model say?

## A
**Revert part 4 to the last state where parts 1–3 pass, and submit that.**

- Hidden tests are grouped per part and partial credit advances candidates: reported passing outcomes cluster around 18/20, 22/25 and 16/19, and reported rejections around 14/20. Three clean parts beat four broken ones.
- A half-finished refactor can break earlier parts, turning a 15/20 into a 5/20 in the final minute — the single most expensive mistake available in the format.
- Corollary: after each part passes, note (or comment out) the working shape so reverting is 30 seconds, not a reconstruction.
- If part 4 must stay in, guard it so it cannot execute on the inputs the earlier parts use.

## Q zh
还剩 15 分钟。part 4 写了一半，part 1–3 都能过。正确动作是什么？评分模型说明了什么？

## A zh
**把 part 4 回退到 part 1–3 还能通过的最后状态，然后提交。**

- 隐藏测试按 part 分组，部分通过也能晋级：报告中通过的成绩集中在 18/20、22/25、16/19，被拒的在 14/20 附近。三个干净的 part 胜过四个坏掉的。
- 一次改到一半的重构会打破前面的 part，在最后一分钟把 15/20 变成 5/20 —— 这是这种形式里代价最高的错误。
- 推论：每个 part 通过后就记下（或注释保留）当时能跑的形状，让回退是 30 秒的事，而不是一次重建。
- 如果 part 4 必须留着，就加守卫，让它在前面各 part 使用的输入上根本不会执行。
