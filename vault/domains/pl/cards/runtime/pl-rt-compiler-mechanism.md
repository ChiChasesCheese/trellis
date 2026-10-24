---
id: pl-rt-compiler-mechanism
node: runtime.compiler-pipeline
type: qa
step: 5
---
## Q
同一个函数 `a * 2 + b`，在 Python、Java、Rust、Go 的编译流水线里分别变成了什么？
这说明各语言的编译器走到了哪一步？

## A
同一个函数（整数 `a * 2 + b`）各阶段的真实产物：

**Python**：AST → 字节码，到此为止，运行时由解释器逐条执行。
```
Return(value=BinOp(left=BinOp(left=Name(a), op=Mult(), right=Constant(2)), op=Add(), right=Name(b)))
LOAD_FAST_BORROW a / LOAD_SMALL_INT 2 / BINARY_OP * / LOAD_FAST_BORROW b / BINARY_OP + / RETURN_VALUE
```

**Java**：`javac` 编译到 JVM 字节码，一种基于栈的指令集，体系结构无关。
```
iload_0, iconst_2, imul, iload_1, iadd, ireturn
```
机器码要等运行时由 JIT 生成。

**Rust**：源码 → HIR → MIR（借用检查在这一级进行）→ LLVM IR → 优化 → 汇编。LLVM IR（`-O3`）：
```
%_3 = shl i32 %a, 1
%_0 = add i32 %_3, %b
```
乘 2 被优化成左移 1 位；最终的 ARM64 汇编只有一条指令：`add w0, w1, w0, lsl #1`。

**Go**：源码 → 类型检查 → SSA → 自带的后端优化与代码生成。同样的函数得到 ARM64 的 `ADD R0<<1, R1, R0`，也是一条指令。

结论：
- 两个 AOT（提前编译）编译器，不同的后端，殊途同归，得到的机器码相同。简单函数上 Go 的自研后端没有落后。差距出现在复杂的优化（内联深度、循环向量化、跨函数分析）上。
- Java 和 Python 把“最后一步”留到运行时：Java 的字节码是稳定的中间格式，运行时可以按实际热点 JIT；CPython 的字节码只是解释器的输入。
- 字节码是一个设计选择：它让“编译一次，到处运行”成立，也让运行时拿到真实 profile 后再优化。
