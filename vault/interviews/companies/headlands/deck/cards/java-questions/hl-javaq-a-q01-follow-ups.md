---
id: hl-javaq-a-q01-follow-ups
node: java-questions.a-speed
type: qa
step: 4
---
## Q
回答"Java 为什么能快"之后，面试官常追问三件事：既然这么好为什么 HFT 公司还写 C++？C1 和 C2 有什么区别（分层编译）？怎么确认某个方法被内联了？各怎么答？
If it's that good, why do HFT firms still write C++? What is tiered compilation? How would you check that a method was inlined?

## A
- **为什么 HFT 仍写 C++**：稳态吞吐可以接近，差距在**尾延迟和内存布局**（GC/safepoint 暂停、预热与去优化、对象头与指针追逐、没有内联值类型）；做低延迟系统时 C++ 仍占优。
- **C1 与 C2**：分层编译（tiered compilation）里，tier 1-3 是 C1，编译快、带 profiling；tier 4 是 C2，激进优化、编译慢；解释器是 tier 0。方法越热，层级越高。
- **怎么看内联**：`-XX:+UnlockDiagnosticVMOptions -XX:+PrintInlining`。
- 回答"和 C++ 比"的口径：稳态吞吐可以接近；尾延迟和内存布局是差距所在；我知道差距在哪、怎么缩小。
