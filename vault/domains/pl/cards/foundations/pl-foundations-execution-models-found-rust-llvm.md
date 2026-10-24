---
id: pl-foundations-execution-models-found-rust-llvm
node: foundations.execution-models
type: qa
step: 5
---
## Q
`rustc` 是怎样把 Rust 代码变成机器码的？LLVM 在其中扮演什么角色？

## A
`rustc` 自己只负责前端：解析、类型检查、借用检查，然后把程序降低成一种中间表示，交给 LLVM。LLVM 是一个独立的编译器后端项目（Clang、Swift 等也用它）：接受一种与具体 CPU 无关的、类似汇编的中间语言（LLVM IR），做大量优化，再生成目标 CPU 的机器码。

用 `rustc --emit llvm-ir` 可以看到中间结果。`a * b + 1` 在开启优化（`-O`）后是：

```console
define i64 @f(i64 %a, i64 %b) {
start:
  %_3 = mul i64 %b, %a
  %_0 = add i64 %_3, 1
  ret i64 %_0
}
```

三条指令，类型 `i64` 已经完全确定，没有任何运行时类型信息。LLVM 之后的优化包括内联、循环展开、向量化、把乘加融合成一条 CPU 指令等。

后果：Rust 免费获得了 LLVM 数十年积累的优化，所以生成的代码通常很快；代价是编译时间长，因为 LLVM 做的优化多，而且 Rust 的泛型会为每个具体类型生成一份代码，交给 LLVM 的体量很大。debug 构建（不优化）和 release 构建（`-O`）的速度可能差一个数量级。
