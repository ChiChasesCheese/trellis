---
id: cc-round-time-no-late-refactor
node: round.time
type: qa
---
## Q
Minute 48. Parts 1–4 pass. You suddenly see a cleaner model that would make Part 5 easy. Do you refactor?

## A
**No. Freeze the shape at roughly two-thirds of the clock.** A refactor touches code that currently earns points, and you have no time to re-verify the parts it touches.

If Part 5 genuinely needs a different structure, build that structure *beside* the existing one and use it only in the Part 5 path — duplication you can delete later is cheaper than a rewrite you cannot finish. The cleaner model is a lesson for the next round, written down after you submit, not a change made at minute 48.

## Q zh
第 48 分钟。Part 1–4 都通过。你忽然看到一个更干净的模型，会让 Part 5 变得很容易。要重构吗？

## A zh
**不要。大约在计时的三分之二处冻结代码形状。** 重构会动到正在得分的代码，而你已经没时间重新验证被动到的部分。

如果 Part 5 确实需要另一种结构，就把它建在现有结构**旁边**，只在 Part 5 的路径上使用 —— 事后可以删掉的重复，比做不完的重写便宜。更干净的模型是下一场的教训，提交之后写下来，而不是第 48 分钟动手改。
