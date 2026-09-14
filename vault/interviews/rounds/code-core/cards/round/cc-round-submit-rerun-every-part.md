---
id: cc-round-submit-rerun-every-part
node: round.submission
type: qa
---
## Q
You fixed a bug in the Part 4 code path two minutes ago. What must you do before submitting?

## A
**Re-run the samples of every earlier part.** All parts share one program; a fix inside a shared helper — the parser, the comparator, the renderer — silently changes what Parts 1–3 print.

This is the single most common way a candidate submits a *lower* score than they held ten minutes earlier. Keep the earlier samples in files or in a list at the bottom of the file so re-running all of them is one command, and make it the routine after every change, not just before submitting.

## Q zh
你两分钟前修了 Part 4 路径上的一个 bug。提交前必须做什么？

## A zh
**把之前每一部分的样例重跑一遍。** 所有部分共用一个程序；对共享辅助函数 —— 解析器、比较器、渲染器 —— 的修改，会悄悄改变 Part 1–3 的打印结果。

这是候选人提交出比十分钟前**更低**分数的最常见方式。把早期样例存成文件或放在文件底部的一个列表里，让"全部重跑"变成一条命令，并把它变成每次改动后的例行动作，而不只是提交前。
