---
id: hl-cq-q27-script
node: cpp-questions.f-ub-debug
type: qa
step: 27
---
## Q
用英文 60 秒回答：You're given a code framework with a bug. How do you debug it in C++?

## A
结构：复现缩小并读契约 → 假设 + 廉价验证（`assert`、打印、`-g -O0` 断点；均值 20 对 35 的例子）→ 内存用 ASan/UBSan、竞争用 TSan、libc++ 加固，`-O2` 才有的 bug 多为 UB → 一次改一处、保留回归测试、边想边说。

- First I **reproduce and shrink** the failing case, and read the contract - the header comments and the preconditions - because in a framework the bug is often a misuse of the interface.
- Then I form a hypothesis and test it cheaply: an `assert` on the precondition, a print of the loop bounds, or a debugger breakpoint with `-g -O0`. In a toy example, the average of the last two prices came out as 20 instead of 35; printing the index showed the loop started one element too late.
- For memory problems I rebuild with **ASan and UBSan**, for races **TSan**, and libc++'s hardened mode makes `operator[]` out-of-range abort with a message. A bug that only appears at `-O2` is almost always undefined behavior or an uninitialized variable.
- I change one thing at a time, keep the failing case as a regression test, and narrate my reasoning as I go.
