---
id: hl-hc03-no-tco
node: problems.hc03-recursive-sum
type: qa
step: 7
---
## Q
什么是尾调用（tail call）和尾调用优化（TCO）？为什么 Java 没有 TCO，Scala / Kotlin 又怎么做？

## A
**尾调用**：函数做的最后一件事是调用另一个函数，并直接把它的返回值当自己的返回值。`return n + sum(n-1)` 不是（返回后还要做 `n +`）；`return step(n-1, acc+n)` 是（把累加器 `acc` 传下去）。尾调用返回后当前栈帧再也用不到，编译器可丢掉它，让尾递归像循环一样只占常数帧——这就是 **TCO**。Scheme、Haskell 保证 TCO。

**Java 没有 TCO**：JVM 字节码没有尾调用指令，`javac` 不做，JIT 也不保证。主要原因：栈帧对语义可见——异常栈轨迹（stack trace）、`StackWalker`、调试器、历史上按调用栈判断权限的安全检查都依赖「每次调用有一个帧」，消除帧会让它们对不上。

**Scala `@tailrec` / Kotlin `tailrec`**：在**编译期**把**自递归**改写成循环；互递归（A 调 B、B 调 A）不行，仍会爆栈，要 trampoline（Scala `TailCalls`）。

口述：「JVM 没有尾调用优化，因为栈帧对异常轨迹和调试是可见语义。Scala 和 Kotlin 编译期把自递归变循环，互递归不行。Java 里我改循环，或用 trampoline 把栈换成堆。」

C++ 对比：`-O2` 通常会把尾递归变循环（clang/gcc），Java 不会；但标准不保证，`-O0` 不做，带检查的版本做不了。要保证在 clang 里用 `[[clang::musttail]]`，或直接写循环。
