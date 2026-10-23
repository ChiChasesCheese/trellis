---
id: hl-c09-no-sanitizer-habits
node: cpp-lessons.c09-ub-sanitizers
type: qa
step: 13
---
## Q
CoderPad 上通常不能加 sanitizer，怎么靠习惯避免 UB？

## A
- 用 `.at()` 调试越界。
- 小心 `size_t` 与 `int` 混用。
- 不依赖未初始化值：声明即初始化（`int x{};`）。
- 编译时加 `-Wall -Wextra`，所有警告都当作 bug 处理。
- 本地开发时才开 `-fsanitize=address,undefined`。
