---
id: hl-cq-cs03-compile-model
node: cpp-questions.cheatsheet
type: qa
step: 3
---
## Q
一句话背诵：C++ 的编译模型是什么？ODR、头文件里的函数和模板、链接错误各是什么规则？

## A
- 预处理 → 编译（每个 `.cpp` 独立）→ 汇编 → 链接。
- `#include <iostream>` 展开成 **84,248 行**。
- 声明可重复，定义只能一次（ODR）；头文件里的函数要 `inline`；模板定义放头文件。
- 声明了没定义 = **链接错误**。
