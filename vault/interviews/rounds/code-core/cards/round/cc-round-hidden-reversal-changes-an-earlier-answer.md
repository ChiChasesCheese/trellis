---
id: cc-round-hidden-reversal-changes-an-earlier-answer
node: round.hidden-tests
type: qa
---
## Q
Why is the undo event — a dispute, a refund, a cancellation, a shutdown — where the last group of hidden tests lives?

## A
**Because it is the only event that can make an already-correct answer wrong.** Everything before it accumulates; the reversal is the first thing that must *subtract*, and it exposes every counter you incremented in more than one place.

The grader's four probes are always the same: reverse twice, reverse an unknown id, reverse the *non-offending* item (which can push a ratio up rather than down), and reverse everything so the denominator reaches zero. If your undo path is a single function that pops a ledger entry, all four fall out. See [[cc-model-rev-double-reversal-noop]].

## Q zh
为什么撤销事件 —— 争议、退款、取消、下线 —— 是最后一组隐藏测试所在的地方？

## A zh
**因为它是唯一能把已经正确的答案变错的事件。** 它之前的一切都在累加；撤销是第一个必须**做减法**的东西，它会暴露你在不止一处递增过的每一个计数器。

评测机的四个探针永远相同：撤销两次、撤销一个未知 id、撤销那个**不违规**的条目（这会把比率推高而不是推低）、以及把一切都撤销使分母归零。如果你的撤销路径是一个"弹出 ledger 条目"的单一函数，这四种都会自然成立。见 [[cc-model-rev-double-reversal-noop]]。
