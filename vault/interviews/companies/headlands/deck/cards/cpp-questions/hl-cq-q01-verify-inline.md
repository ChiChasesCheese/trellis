---
id: hl-cq-q01-verify-inline
node: cpp-questions.a-why-fast
type: qa
step: 4
---
## Q
追问：有人说“这个函数被内联了”，你怎么验证这句话？
How would you check a claim like “this got inlined”?

## A
不要猜，要看证据：
- 用编译器生成汇编（`-S`），读里面有没有对该函数的 `call`。
- 或者用性能剖析器（profiler）测。
- 对比 `-O0` 和 `-O2` 的汇编：`-O0` 通常保留调用，`-O2` 才会内联。
- 也可以用 Compiler Explorer 在线看。
