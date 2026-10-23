---
id: hl-cq-q03-header-cost
node: cpp-questions.a-why-fast
type: qa
step: 13
---
## Q
`#include <iostream>` 预处理之后有多少行？这说明 C++ 编译慢的原因是什么？C++20 的哪个特性想解决它？

## A
- 实测：`<iostream>` 展开后约 **84,248 行**，`<cstdio>` 只有约 711 行。
- 原因：头文件是**文本复制粘贴**，每个包含它的 `.cpp` 都要把这些内容重新解析一遍，所以 C++ 编译慢。
- 解决：C++20 的 **modules**，用 `import` 取代 `#include`。
- 一个 `.cpp` 只需要声明就能编译：`lib.hpp` 里写 `int square(int x);`，调用方就能通过编译；函数体在 `lib.cpp`，由链接器接上。
