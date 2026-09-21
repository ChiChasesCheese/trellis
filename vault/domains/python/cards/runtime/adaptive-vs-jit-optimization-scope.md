---
id: adaptive-vs-jit-optimization-scope
node: runtime.adaptive-jit
type: qa
source: cpython-internals
---
## Q
自适应解释器（specializing interpreter）和实验性 JIT，两者的优化范围有什么本质区别？为什么在自适应解释器之上还需要一层 JIT？

## A
自适应解释器（历史上称 tier 1）的特化逐条指令进行，每次只能替换一条指令。JIT（tier 2）的机制是把一整段连续执行的字节码指令序列（trace，执行轨迹）识别出来并整体替换，从而能做跨越多条指令的优化（比如消除相邻指令之间重复的类型检查）——这是只优化单条指令的自适应解释器做不到的。
