---
id: hl-j19-inlining
node: java21.j19-runtime-zgc-jit
type: qa
step: 22
---
## Q
JIT 的内联（inlining）是什么？它为什么是最重要的优化？默认大小阈值是多少，热路径的经验是什么？

## A
把被调方法的代码直接贴进调用处。去掉调用开销；更重要的是让后面的优化看到**更大的代码块**（逃逸分析、常量折叠、循环优化都靠它）。

默认：热点方法体 ≤ **325** 字节码（`FreqInlineSize`）才内联；非热点 ≤ **35**（`MaxInlineSize`）。

`PrintInlining` 输出示例：`add (7 bytes) inline`、`square (4 bytes) inline`；故意写成 492 字节的 `tooBig` 被拒绝：`hot method too big` / `callee is too large`。

**经验：热路径上的方法保持短小。**
