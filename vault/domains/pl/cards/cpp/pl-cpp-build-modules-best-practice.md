---
id: pl-cpp-build-modules-best-practice
node: cpp.build-modules
type: qa
step: 9
---
## Q
资深 C++ 工程师怎样组织头文件、控制编译时间、规避 ODR 问题？新项目的构建与依赖该怎样起步？

## A
**头文件规范**：
1. 每个头文件**自包含**：单独 `#include` 它也能编译（包含它自己需要的所有头文件）；并写一个只 `#include` 该头文件的 `.cpp` 来测试；
2. 用 `#pragma once` 或包含守卫；
3. 头文件里**只放接口**：声明、模板、`inline`/`constexpr`；实现放 `.cpp`；
4. **前置声明**（`class Foo;`）代替不必要的 `#include`，减少耦合和编译依赖；
5. 头文件里不写 `using namespace ...`，也不定义宏污染别人；
6. 遵循 "Include What You Use"：用到什么就包含什么，不依赖间接包含（`include-what-you-use` 工具可检查）。

**规避 ODR 问题**：
1. 仅在一个文件里使用的函数和变量放进**匿名命名空间**或标 `static`，名字不外泄；
2. 头文件里的函数定义必须标 `inline`（类内定义的成员函数自动是 `inline`）；
3. 头文件里的全局变量用 `inline` 变量（C++17）：`inline constexpr int kMax = 10;`；
4. 编译所有翻译单元用**相同的标准版本和宏定义**，否则同一个类在不同文件里布局不同；
5. 全局对象避免跨翻译单元的初始化依赖：本机实测，`a.cpp` 里 `int x = y + 1`、`b.cpp` 里 `int y = g()`，按 `a b` 的顺序链接得到 `x = 1`，按 `b a` 的顺序得到 `x = 42`；改用函数内静态变量（首次调用时初始化），或 `constinit`。

**缩短编译时间**：
- 用 `-ftime-trace` 看是谁慢；
- 预编译头、`ccache`、unity build；
- 重的模板代码和头文件（`<regex>`、`<ranges>`、大型第三方头）限制在少数 `.cpp` 里，用 pimpl 或接口类隔离；
- 显式实例化常用的模板；
- 分布式编译（`distcc`、`icecream`、Bazel 远程执行）。

**起步的构建**：
1. CMake + Ninja，目标化写法；
2. 开启 `CMAKE_EXPORT_COMPILE_COMMANDS`；
3. 选 vcpkg 或 Conan 之一并锁版本（清单文件进版本库）；
4. CI 里分别用至少两个编译器（GCC 和 Clang）编译，抓住可移植性问题；
5. 把 sanitizer 构建变成 CI 的一个固定任务。

**关于模块**：新项目可以保持头文件接口，内部库在工具链允许时再逐步试用模块。

**为什么这样**：这些做法的共同目的是让"每个翻译单元的编译输入"小而确定，让"链接时的名字匹配"不出意外，把 C++ 构建模型的先天缺陷用纪律补上。
