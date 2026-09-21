%% trellis:begin %%
# 自适应解释器（PEP 659）与实验性 JIT（PEP 744）
*解释器与执行模型*

理解 3.11 起的特化（specializing）字节码如何按运行时类型内联快速路径，3.13 的 copy-and-patch JIT 处于实验阶段，以及这对"Python 慢"的回答意味着什么。

**Requires:** [[domains/python/map/runtime.frames-eval|求值循环与帧：调用栈、递归限制与尾调用]]

## Readings
- [[cpy-bytecode-interpreter|字节码解释器：栈机、调用栈重构与自适应特化]]
- [[cpy-jit-tier2|分层执行：从追踪记录到 copy-and-patch JIT]]
- [[cpyint-02-evaluation-loop|CPython Internals · 求值循环]]
- [[peps-pep659-specializing-interpreter|PEP 659：特化自适应解释器（Specializing Adaptive Interpreter）]]
- [[peps-pep744-jit-compilation|PEP 744：JIT 编译器现状说明]]

## Cards (6)
1. [[adaptive-vs-jit-optimization-scope]]
2. [[deoptimize-on-guard-failure]]
3. [[jit-executor-reuse]]
4. [[jit-experimental-two-execution-modes]]
5. [[jit-hot-loop-tracing]]
6. [[specialization-rewrite-mechanism]]
%% trellis:end %%

## Notes
