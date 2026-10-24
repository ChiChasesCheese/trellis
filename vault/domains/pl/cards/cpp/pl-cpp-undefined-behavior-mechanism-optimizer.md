---
id: pl-cpp-undefined-behavior-mechanism-optimizer
node: cpp.undefined-behavior
type: qa
step: 3
---
## Q
编译器具体怎样利用 UB 做优化？为什么同一份代码在 `-O0` 和 `-O2` 下结果不同？

## A
**原理**：编译器的推理规则是——"程序没有 UB，所以这些情况不会发生"。凡是只在 UB 发生时才成立的分支、条件，都可以删除或简化。它不会去"检测" UB。

**实例一：有符号溢出**

```cpp
[[gnu::noinline]] bool always(int x) { return x + 1 > x; }
// 以 INT_MAX 调用
```

本机实测：`-O0` 返回 `false`（真的算了加法，回绕成负数）；`-O2` 返回 `true`（编译器推理：有符号溢出不会发生，所以 `x + 1 > x` 恒为真，函数被优化成 `return true`）；加上 `-fwrapv` 后即使 `-O2` 也回到 `false`。

**实例二：先解引用，后判空**

```cpp
int f(int* p) { int v = *p; if (p == nullptr) return -1; return v; }
```

`-O2` 的汇编只剩 `ldr w0, [x0]; ret`，判空分支被删除：既然 `*p` 在前，`p` 一定非空，后面的检查是死代码。

**实例三：读取未初始化变量**

```cpp
int x; if (argc > 5) x = 1;   // 实际没有执行赋值
println("{}", x == 1);
```

实测输出 `true`：优化器认为 `x` 只可能是 1，直接折叠。编译器还警告 `variable 'x' is used uninitialized whenever 'if' condition is false`。

**为什么这是有用的优化**：有符号整数不会溢出，编译器就能把 `for (int i = 0; i < n; ++i)` 中的 `i` 当作不会回绕的变量，从而扩展成 64 位索引、做循环向量化、提升不变量；无符号则要保留回绕语义，不能这样做。UB 为这类变换提供了前提。

**为什么 `-O0` 能"救"你**：不优化时编译器不做这些推理，代码按字面执行，掩盖了 UB。这就是"调试版正常，发布版崩溃"的常见来源。

**要记住的一点**：UB 的后果会**向前传播**：只要 UB 出现在某条路径上，编译器就可以修改之前的代码，不只是触发点之后的行为。
