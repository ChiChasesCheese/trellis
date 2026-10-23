---
id: hl-cq-q04-script
node: cpp-questions.a-why-fast
type: qa
step: 24
---
## Q
用英文 60 秒回答：What does the optimizer actually do at `-O2`? How would you verify it?

## A
结构：列出优化种类 → 三种求和写法的具体例子（0 次调用、闭式）→ 用 `-S`/Compiler Explorer 验证并测量，限制因素是跨 TU、虚调用、别名 → 点题零开销抽象。

- At `-O2` the compiler does **inlining**, **constant folding**, dead-code elimination, **loop unrolling and vectorization**, and **copy elision**.
- Here's a concrete case: a hand-written loop, `std::accumulate`, and `accumulate` with a lambda all compile at `-O2` to code with **zero calls** and SIMD instructions, while at `-O0` the library versions keep a call. A loop summing `0..n-1` becomes a closed-form multiplication - eight instructions, no loop.
- I verify with `-S` or **Compiler Explorer**, and I measure with a benchmark, because the optimizer's decisions depend on what it can see: calls across translation units, virtual calls and **pointer aliasing** all limit it.
- That's what zero-overhead abstraction means in practice.
