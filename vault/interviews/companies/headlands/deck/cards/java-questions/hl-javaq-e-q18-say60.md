---
id: hl-javaq-e-q18-say60
node: java-questions.e-jit-gc
type: qa
step: 27
---
## Q
用英文 60 秒回答：How does the JIT work? Explain the interpreter, C1, C2, tiered compilation, and OSR.

## A
结构：解释器计数 → C1（带 profiling）→ C2（激进优化）→ 后台线程编译 → OSR 处理一次性长循环 → 去优化 → 用 PrintCompilation 观察。

> "HotSpot uses tiered compilation. Code starts in the interpreter, which counts invocations and loop back-edges. Past a threshold, the method is compiled by C1 - fast to compile, moderately optimised, with profiling - and if it stays hot, by C2, which uses the collected profile to do aggressive optimisation like inlining on observed types. Compilation happens on background threads. A hot loop in a method that's called only once is handled by on-stack replacement, which swaps the running frame between iterations. If a speculation turns out wrong, the JVM deoptimises back to the interpreter and starts again. You can watch all of that with `-XX:+PrintCompilation`: the lines with a percent sign are OSR compilations."
