---
id: cc-round-ambiguity-pick-the-extendable-reading
node: round.ambiguity
type: qa
---
## Q
Two readings both fit the prose and both pass the worked example. Which do you implement?

## A
**The one the later parts can extend, and — failing that — the one that keeps more information.**

A reversal that *removes* the original event keeps a ledger you can also query, count and re-apply; a reversal that merely marks the event "no longer counted" throws that structure away and cannot express a partial undo in a later part.

Ranking, in order: (1) consistent with every worked example; (2) survives the last part's requirements; (3) keeps the raw record rather than a collapsed summary; (4) simpler to explain in one sentence.

## Q zh
两种读法都符合正文，也都能通过题面样例。实现哪一个？

## A zh
**后面的部分能扩展的那个；若都能，则选保留更多信息的那个。**

把原事件**移除**的撤销，留下的 ledger 还能被查询、计数、重新应用；只把事件标成「不再计入」的撤销，则丢掉了这个结构，也无法在后面的部分表达部分撤销。

排序依次是：(1) 与每个样例一致；(2) 撑得住最后一部分的要求；(3) 保留原始记录而不是压扁成汇总；(4) 一句话就能解释清楚。
