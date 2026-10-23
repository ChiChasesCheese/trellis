---
id: hl-c16-compile-flags
node: cpp-lessons.c16-coderpad-survival
type: qa
step: 22
---
## Q
C++20 题集用什么编译参数？`-fno-sanitize-recover=undefined` 起什么作用？`perf` 标签的测试怎么处理？

## A
编译参数：`clang++ -std=c++20 -O2 -Wall -Wextra -fsanitize=address,undefined -fno-sanitize-recover=undefined`。
- 最后一项让 UBSan 一发现未定义行为（比如有符号溢出）就**终止进程**；默认只打印、测试照样「绿」。
- 带 `perf` 标签的测试**不在 sanitizer 版里跑**（慢几倍，限时没意义）；工具另编一个 `-O2` 无 sanitizer 的二进制只跑它们。
- reference 用 `-Werror` 编译，starter / work 的警告只提示。
- 没有额外依赖：测试框架是 `tools/cpp/minitest.hpp`。
