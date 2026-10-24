---
id: pl-binding-calling-convention-philosophy-no-tail-calls
node: binding.calling-convention
type: qa
step: 8
---
## Q
什么是尾调用优化（tail call optimization）？为什么 Go、Java、Python 都不做，Rust 和 C++ 也不保证？

## A
**尾调用**是函数的最后一个动作恰好是调用另一个函数并直接返回其结果：`return f(x)`。这时当前栈帧里已经没有任何还要用的东西，调用者的帧完全可以被被调用者复用：不用 `call` 而是 `jump`，栈深度不增长。这叫**尾调用优化**（tail call optimization，TCO）。

有了 TCO，递归写出来的循环（`loop(n-1, acc+n)`）可以无限运行，不会溢出；Scheme 的规范**要求**所有实现做 TCO，函数式语言（Haskell、OCaml、Scala 对自递归）也有保证。

五门语言的现状：

- **Python**：不做，而且这是明确的设计决定。Python 的创造者认为，TCO 会抹掉栈帧，让回溯（traceback）失去调用链，调试体验变差，还会鼓励一种不 Pythonic 的递归风格；递归深度上限 1000 就是对此的态度。
- **Java**：不做。JVM 栈帧承担了安全检查、`StackWalker` 回溯和反射所需的调用者信息，抹掉帧会改变这些行为。
- **Go**：不做，协程栈可增长，深递归不会溢出，也不需要。
- **C++**：标准不保证。GCC、Clang 在 `-O2` 下通常把尾递归变成循环，`-O0` 则不会：一个累加 1 亿层的 `return sum(n - 1, acc + n)`，本机 `-O0` 以段错误（退出码 139）崩溃，`-O2` 正常输出 `5000000050000000`。要硬性保证只能用编译器扩展 `[[clang::musttail]]`。
- **Rust**：不保证。LLVM 在优化构建里常常能把尾递归变成循环，但这是优化器的善意，调试构建里栈照样增长；语言层面保证尾调用的 `become` 关键字在稳定版里仍是实验特性，写出来会得到 `error[E0658]: become expression is experimental`。

共同的逻辑：这些语言把**栈帧当作可观察的、有语义的东西**：回溯、调试器、安全检查、性能剖析都依赖它。保证 TCO 等于承诺栈帧可以消失，这与「我们想让你看清调用链」的价值观相冲突。函数式语言反过来：它们把递归当作循环的唯一形式，如果没有 TCO，语言连循环都没有了。

对工程师的含义：**在这五门语言里，把深度不受控的递归当作潜在 bug。**需要遍历很深的结构，用显式栈（`Deque`、`Vec`、`list`）和循环。
