---
id: hl-c16-std-and-includes
node: cpp-lessons.c16-coderpad-survival
type: qa
step: 2
---
## Q
在不确定 `-std` 的编辑器里怎么确认语言标准？头文件应该怎么 `include`？为什么不用 `<bits/stdc++.h>`？

## A
- 先写一个小的 C++20 特性（比如 `std::span` / `contains`）试编译，失败就退回 C++17 的写法。
- 头文件**逐个 include**。
- `<bits/stdc++.h>` **只有 GCC 有**，Clang/Apple 环境没有。
- 某个头文件「碰巧」被另一个头间接包含并不可靠，换编译器就消失。
