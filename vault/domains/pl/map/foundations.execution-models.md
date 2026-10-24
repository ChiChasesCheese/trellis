%% trellis:begin %%
# 执行模型：AOT 编译、字节码 + 虚拟机 + JIT、解释执行
*语言的基本坐标*

源代码怎样变成 CPU 执行的指令：Go/Rust 提前编译成机器码，Java 编译成字节码在 JVM 上解释 + JIT，CPython 编译成字节码再解释。

**Core** — part of the first pass through this subject.

**Unlocks:** [[domains/pl/map/foundations.language-vs-implementation|语言规范与实现]], [[domains/pl/map/runtime.compiler-pipeline|编译流水线]]

## Cards (11)
1. [[pl-foundations-execution-models-principle]]
2. [[pl-foundations-execution-models-found-jvm-classloader]]
3. [[pl-foundations-execution-models-found-cpython-pyc]]
4. [[pl-foundations-execution-models-found-go-toolchain]]
5. [[pl-foundations-execution-models-found-rust-llvm]]
6. [[pl-foundations-execution-models-mechanism]]
7. [[pl-foundations-execution-models-table]]
8. [[pl-foundations-execution-models-unique-jit]]
9. [[pl-foundations-execution-models-best-practice]]
10. [[pl-foundations-execution-models-pitfall-python-compile]]
11. [[pl-foundations-execution-models-history-tiering]]
%% trellis:end %%

## Notes
