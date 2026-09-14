---
id: cc-output-ordering-total-order
node: output.ordering
type: qa
---
## Q
The spec says "sorted by score descending". Two rows share a score, and your output diffs against the grader on exactly those two lines. Diagnose and fix.

## A
**A partial sort key is not a specification.** Any order of the tied rows satisfies "by score descending", so the grader's expected file encodes a tie-break you did not implement.

- Make the key **total**: append every field that can still differ, ending with the input index if nothing else does.
- If the statement names no tie-break, "input order" is the safest reading — and Python's stable sort gives it for free from the input list. Write that in a comment instead of sorting twice.
- Sort **once**, on final values. A field mutated after sorting silently invalidates the order.
- Any structure whose iteration order is not a contract (a `set`, a heap) must be sorted before printing, not iterated.

See [[cc-output-ordering-stable-two-pass]].

## Q zh
spec 写的是「按 score 降序」。两行 score 相同，而你的输出恰好在这两行上和 grader 不一致。诊断并修复。

## A zh
**部分排序键不是规范。** 并列行的任何顺序都满足「按 score 降序」，所以 grader 的期望文件里编码了一个你没实现的 tie-break。

- 把 key 做**完全**：把所有还可能不同的字段都追加进去，实在没有就以输入下标收尾。
- 如果题面没写 tie-break，「输入顺序」是最稳妥的读法 —— 而且从输入列表出发时，Python 的稳定排序免费给你这个顺序。把这一点写进注释，而不是排两次序。
- 只排序**一次**，且基于最终值。排序后再改字段会悄悄让顺序失效。
- 迭代顺序不构成契约的结构（`set`、堆）必须先排序再打印，不能直接遍历。

见 [[cc-output-ordering-stable-two-pass]]。
