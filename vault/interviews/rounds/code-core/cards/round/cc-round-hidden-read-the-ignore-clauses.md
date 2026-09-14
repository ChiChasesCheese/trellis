---
id: cc-round-hidden-read-the-ignore-clauses
node: round.hidden-tests
type: qa
---
## Q
Reading a statement, which sentences most reliably predict a hidden test?

## A
**Every sentence containing "ignored", "unknown", "invalid", "may", "at most", "only if" or "otherwise".** Each names a branch the author had to implement, which means each has a test.

Practical move: as you read, keep a list of ignore-paths — unknown id, wrong state, bad arity, non-numeric field, duplicate, out-of-range index. Then check that each one is a silent no-op or the specified message, and that none of them crashes or half-applies a change. A statement that says "invalid commands are silently ignored" is telling you where most of its tests are.

## Q zh
读题面时，哪些句子最能可靠地预示一个隐藏测试？

## A zh
**每一句包含「忽略」「未知」「无效」「可能」「至多」「仅当」「否则」的话。** 每一句都点名了作者不得不实现的一个分支，也就意味着有一个测试。

实用做法：边读边列一张"忽略路径"清单 —— 未知 id、状态不对、参数个数错、非数字字段、重复、下标越界。然后逐条确认它是静默 no-op 还是题面指定的消息，并确认它既不崩溃也不会半途改动状态。一句「无效命令被静默忽略」，就是在告诉你大部分测试藏在哪。
