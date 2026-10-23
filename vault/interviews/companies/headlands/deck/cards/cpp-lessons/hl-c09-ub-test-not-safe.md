---
id: hl-c09-ub-test-not-safe
node: cpp-lessons.c09-ub-sanitizers
type: qa
step: 15
---
## Q
面试问：UB 为什么「测试通过也不安全」？
Interview question: Why is passing tests not enough to show the absence of undefined behaviour?

## A
- 编译器可以**假设 UB 不发生**并据此变换代码：删检查、重排读写、合并分支。
- 因此升级编译器、改优化级别、甚至加一行周围代码，行为都可能变。
- 例：`x + 1 < x` 在 `-O2` 下被编译器优化成 `return false`，检查整个消失。
- 发现手段：Sanitizer（ASan/UBSan/TSan）、静态分析、`-Wall -Wextra -Werror`、模糊测试、Valgrind。
