%% trellis:begin %%
# 编译流水线
*编译、运行时与性能*

词法、语法、AST、类型检查、中间表示、优化、代码生成；Rust 借 LLVM、Go 自研后端追求编译速度。

**Requires:** [[domains/pl/map/foundations.execution-models|执行模型：AOT 编译、字节码 + 虚拟机 + JIT、解释执行]]

**Unlocks:** [[domains/pl/map/runtime.syntax-parsing|语法与解析]], [[domains/pl/map/runtime.optimizations|编译器优化]], [[domains/pl/map/runtime.jit|JIT 编译]], [[domains/pl/map/runtime.cpython-internals|CPython 解释器]], [[domains/pl/map/runtime.zero-cost-abstractions|零成本抽象]], [[domains/pl/map/runtime.ffi|跨语言调用（FFI）]], [[domains/pl/map/metaprogramming.macros|宏]]

## Drills
- [[runtime-first-call-and-debug-build|练习：刚发布的 Java 实例前几个请求特别慢，而 Rust 版本比 Java 还慢]]

## Cards (10)
1. [[pl-rt-compiler-principle]]
2. [[pl-rt-compiler-found-ast-ir]]
3. [[pl-rt-compiler-found-bytecode]]
4. [[pl-rt-compiler-found-llvm]]
5. [[pl-rt-compiler-mechanism]]
6. [[pl-rt-compiler-table]]
7. [[pl-rt-compiler-unique-monomorph-cost]]
8. [[pl-rt-compiler-best-practice]]
9. [[pl-rt-compiler-pitfall-debug-build]]
10. [[pl-rt-compiler-evolution]]
%% trellis:end %%

## Notes
