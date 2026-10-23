---
id: hl-cq-cs21-compile-and-live-mantra
node: cpp-questions.cheatsheet
type: qa
step: 21
---
## Q
C++ 面试里常用的编译命令是什么？现场写代码的口诀是什么？

## A
- 编译命令：`clang++ -std=c++20 -O2 -Wall -Wextra -fsanitize=address,undefined x.cpp`（测速时去掉 sanitizer；C++23 用 `-std=c++23`）。
- 现场口诀：问语言 → 最小骨架先跑通 → 小步编译 → 读第一个错误 → 先说测试用例和复杂度。
- 每次都检查三件事：`size_t` 下溢、整数溢出、迭代器失效。
