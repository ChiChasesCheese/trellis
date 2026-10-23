---
id: hl-cq-q03-build-pipeline
node: cpp-questions.a-why-fast
type: qa
step: 12
---
## Q
面试题：从 `g++ main.cpp` 到程序运行，中间发生了什么？为什么要有头文件？什么是单一定义规则（ODR）？
Walk me through what happens between `g++ main.cpp` and a running program. Why do we have header files, and what is the One Definition Rule?

## A
四步：
1. **预处理**：展开 `#include` 和宏（头文件就是文本复制粘贴）。
2. **编译**：每个 `.cpp` 单独变成目标文件 `.o`，互不影响。
3. **汇编**。
4. **链接**：把多个 `.o` 拼成 `a.out`，解析符号。

- **翻译单元**（translation unit）= 预处理后的一个 `.cpp`，它只知道自己 `#include` 进来的**声明**。
- 声明可以出现很多次；**定义**每个程序只能有一次（ODR，One Definition Rule）。
