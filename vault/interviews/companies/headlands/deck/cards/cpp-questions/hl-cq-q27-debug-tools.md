---
id: hl-cq-q27-debug-tools
node: cpp-questions.f-ub-debug
type: qa
step: 25
---
## Q
C++ debug 有哪些常用工具？`assert` 有什么坑？libc++ 的加固模式（hardening mode）怎么开，开了之后 `v[i]` 越界会怎样？

## A
- `assert` 写前置条件；`-DNDEBUG` 会把它去掉，所以别放有副作用的代码。
- 往 `stderr` 打印；`clang++ -g -O0` + lldb / gdb。
- `-fsanitize=address,undefined` / `thread`。
- libc++ 加固模式：`-D_LIBCPP_HARDENING_MODE=_LIBCPP_HARDENING_MODE_DEBUG`，`v[i]` 越界会直接终止，输出 `libc++ Hardening assertion __n < size() failed: vector[] index out of bounds`。
