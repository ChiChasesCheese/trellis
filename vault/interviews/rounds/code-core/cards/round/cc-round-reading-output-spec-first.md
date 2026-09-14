---
id: cc-round-reading-output-spec-first
node: round.reading
type: qa
---
## Q
Within a single part's statement, which paragraph do you read twice before writing any of its logic?

## A
**The output contract.** The rules are the middle of the problem; the edges are the input shape and the exact bytes you must emit.

Read for: one line per *what*, sorted by *which key with which tie-break*, what is printed when the result is empty, and whether a header or trailing line is required. Those four decide function signatures — a rule that returns a set is useless if the output needs a stable order. Getting the arithmetic right and the ordering wrong fails every test in the part just as thoroughly as getting the arithmetic wrong.

## Q zh
在某一部分的题面里，动手写逻辑之前，你要读两遍的是哪一段？

## A zh
**输出契约。** 规则是题目的中段；两端是输入形状和你必须打印的确切字节。

要读出来的是：每行代表**什么**、按**哪个 key、什么 tie-break** 排序、结果为空时打印什么、是否需要表头或结尾行。这四点决定函数签名 —— 如果输出要求稳定顺序，一个返回 set 的规则就没用。算术全对但顺序错了，和算术错了一样，会让这一部分的测试全挂。
