---
id: hl-c16-practice-kit-overview
node: cpp-lessons.c16-coderpad-survival
type: qa
step: 20
---
## Q
Headlands 面试官可以指定语言，所以高频题除了 Java 版还有 C++20 版。这套 C++20 题的每道题目录里有哪些文件？覆盖了哪些题？

## A
同样的 Part、同样的测试用例，外加 C++ 特有的边界。每道题的 C++ 目录里：
- `reference.hpp`：参考实现（单头文件，在命名空间里）。
- `starter.hpp`：起点，类型和签名已给，函数体 `throw std::logic_error("TODO")`。
- `work.hpp`：你的工作副本（start 命令从 `starter.hpp` 复制）。
- `test.cpp`：测试，用 `#include IMPL_HEADER` 选择实现。
- `main.cpp`：只有 stdin→stdout 的题有；`cases/*.in|out` 是它的端到端样例。

覆盖：oa01、hc01–hc09、hc11、hc13，目前所有编码题都有 C++ 版。
