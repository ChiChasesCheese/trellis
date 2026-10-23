---
id: hl-javaq-a-q01-say60
node: java-questions.a-speed
type: qa
step: 19
---
## Q
用英文 60 秒回答：Why can Java be fast even though it is garbage-collected and runs on a VM? What does the JVM do at run time that a C++ compiler does ahead of time?

## A
结构：稳态不是解释执行 → C1 再 C2 编译 → 用运行时信息优化（去虚化、逃逸分析）→ 实测数字 → 代价是预热、GC、内存布局。

> "Java isn't interpreted in steady state. The JVM starts in an interpreter, profiles the code, and compiles hot methods to machine code - first with C1, then with C2, which does aggressive optimization: inlining, escape analysis, loop optimizations, bounds-check elimination. The interesting part is that it optimizes with *runtime* information, like which classes a call site has actually seen, so it can devirtualize and inline calls a static compiler has to leave virtual. In a quick experiment, the same loop allocated zero bytes with escape analysis on and 4.8 GB with it off, about eight times slower. The price is warm-up time, GC, and a heavier memory layout - object headers and pointers - which is where C++ still wins on tail latency."
