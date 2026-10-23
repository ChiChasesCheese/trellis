---
id: hl-j19-q5-escape-latency
node: java21.j19-runtime-zgc-jit
type: qa
step: 38
---
## Q
面试问：什么是逃逸分析？它和延迟有什么关系？
What is escape analysis and how does it relate to latency?

## A
- 若 JIT 能证明对象不逃出方法，就用普通局部变量替换它（**标量替换**），根本不分配；
- 实测：2000 万个临时 `Point` record，开逃逸分析分配约 **5 MB**，关掉是 **640 MB**；
- 分配少 → GC 少 → 尾部更平；
- 依赖**内联**，所以热路径方法要保持小。

英文骨架：「If the JIT proves an object never escapes, scalar replacement avoids allocating it. Less allocation means fewer GCs and a flatter tail. It relies on inlining.」
