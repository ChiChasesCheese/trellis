---
id: hl-c16-followup-ub-large
node: cpp-lessons.c16-coderpad-survival
type: qa
step: 18
---
## Q
面试问：这段代码有什么 UB 风险？如果输入很大，会怎么改？
Interview question: What UB risks does this code have, and how would you scale it to large input?

## A
UB 风险清单：**越界、迭代器失效、整数溢出、悬空引用、未初始化变量**。

输入很大时：
- 快速 I/O（一次读入、`from_chars`）。
- `reserve` 预留容量。
- 避免拷贝（`const&`、`move`）。
- 选择连续容器（`vector` 优先）。
