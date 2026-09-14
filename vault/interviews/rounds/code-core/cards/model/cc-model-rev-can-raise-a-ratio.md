---
id: cc-model-rev-can-raise-a-ratio
node: model.reversal
type: qa
---
## Q
A merchant sits at 2 fraudulent charges out of 3, just under a 0.7 ratio threshold. A dispute arrives for one of its *legitimate* charges. What happens?

## A
**It becomes 2 of 2 and crosses the threshold — the reversal *flags* the merchant.**

Reversal is not monotone. Removing a charge from the denominator raises the ratio; removing a fraudulent charge lowers it. A program that only checks "did this drop below the line" after an undo misses half the cases.

The discipline: after any reversal, run the *same* evaluation you run after a normal event, in both directions — add to the flagged set or discard from it. Never special-case the reversal path to only un-flag. See [[cc-model-state-reevaluate-only-touched]].

## Q zh
某商户 3 笔里有 2 笔欺诈，刚好低于 0.7 的比率阈值。这时它一笔**正常**扣款被争议了。会发生什么？

## A zh
**变成 2/2，越过阈值 —— 这次撤销反而把该商户标记了。**

撤销不是单调的。从分母里移掉一笔会抬高比率；移掉一笔欺诈才会压低它。只在撤销后检查"是否掉到线下"的程序，会漏掉一半情形。

纪律是：任何撤销之后，跑与普通事件**完全相同**的判定，并且双向生效 —— 加入被标记集合或从中移除。绝不要把撤销路径特化成只做取消标记。见 [[cc-model-state-reevaluate-only-touched]]。
