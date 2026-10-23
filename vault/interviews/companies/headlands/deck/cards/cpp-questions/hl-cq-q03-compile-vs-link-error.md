---
id: hl-cq-q03-compile-vs-link-error
node: cpp-questions.a-why-fast
type: qa
step: 14
---
## Q
C++ 的编译错误和链接错误有什么区别？“声明了没定义”和“两个 `.cpp` 都定义了同一个函数”各是什么结果？
Compile error vs link error?

## A
- **编译错误**来自单个翻译单元内部。
- **链接错误**来自把多个目标文件合并时：缺定义或重复定义。
- 声明了没定义：编译通过，链接失败，报 `undefined reference`（macOS 上是 `Undefined symbols`）。
- 两个 `.cpp` 都定义了同一个非 `inline` 函数：链接时报重复符号（duplicate symbol）。
