%% trellis:begin %%
# 求值循环与帧：调用栈、递归限制与尾调用
*解释器与执行模型*

掌握每次函数调用创建帧对象、`sys.setrecursionlimit` 与栈溢出、生成器为何能挂起（帧被保留），以及 3.11 帧对象的惰性创建优化。

**Requires:** [[domains/python/map/runtime.compile-bytecode|从源码到字节码：编译、`code` 对象、`dis` 与 `.pyc` 缓存]]

**Unlocks:** [[domains/python/map/runtime.adaptive-jit|自适应解释器（PEP 659）与实验性 JIT（PEP 744）]]

## Readings
- [[cpy-bytecode-interpreter|字节码解释器：栈机、调用栈重构与自适应特化]]
- [[cpy-frames-internals|帧（Frame）的内存布局与 3.11 的惰性创建优化]]
- [[cpy-generators-internals|生成器对象怎么把一次函数调用变成可以反复挂起的执行]]
- [[cpyint-02-evaluation-loop|CPython Internals · 求值循环]]
- [[pydocs-sys-module|sys 模块：解释器内部状态入口]]

## Cards (6)
1. [[frame-per-thread-stack-allocation]]
2. [[function-vs-generator-frame-return]]
3. [[generator-embedded-frame-suspend]]
4. [[lazy-frame-object-creation]]
5. [[no-tail-call-optimization]]
6. [[recursionlimit-guards-c-stack]]
%% trellis:end %%

## Notes
