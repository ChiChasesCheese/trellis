---
id: hl-cq-cs04-virtual
node: cpp-questions.cheatsheet
type: qa
step: 4
---
## Q
一句话背诵：C++ 虚函数的成本和规则是什么？热路径用什么替代？

## A
- 每对象一个 vptr（一个 `int` 的类 4 字节，加 `virtual` 变 **16 字节**）。
- 调用是间接的、不能内联。
- 基类要有 **virtual 析构**，否则 `delete` 基类指针是 UB（派生析构不运行）。
- 热路径用 CRTP / `final` / `variant`。
