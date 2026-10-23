---
id: hl-cq-q27-debug-framework
node: cpp-questions.f-ub-debug
type: qa
step: 23
---
## Q
面试题：给你一个带 bug 的代码框架，你怎么用 C++ 的方式 debug？
You're given a code framework with a bug. How do you debug it in C++?

## A
1. 先**复现并缩小**，再读契约（头文件注释、前置条件）和调用方——框架里的 bug 常常是接口用错。
2. 用 `assert` / 日志验证假设；必要时 `-g -O0` + 调试器（lldb / gdb）和 sanitizer。
3. **每次只改一处并重跑**；把失败用例留作回归测试。
4. 说出你的思路比立刻找到 bug 更重要。

只在 `-O2` 才出现的 bug，几乎一定是 UB 或未初始化变量。
