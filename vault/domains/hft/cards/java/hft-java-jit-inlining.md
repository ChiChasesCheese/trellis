---
id: hft-java-jit-inlining
node: java.jit
type: qa
step: 4
---
## Q
为什么说内联（inlining）是 JIT 最重要的优化？热路径上的方法为什么要保持短小？

## A
内联就是把被调方法的代码直接贴到调用处。它省掉调用开销，更重要的是让后续优化能看到**更大的一块代码**：逃逸分析、常量折叠、循环优化都要靠它。

HotSpot 对内联有大小限制：热点方法的字节码不超过约 325 字节（`FreqInlineSize`）才内联，非热点方法不超过约 35 字节（`MaxInlineSize`）。一个实验里，故意写成 492 字节的方法被拒绝，`-XX:+PrintInlining` 显示 `hot method too big`；而 7 字节的 `add` 和 4 字节的 `square` 都被内联。

所以热路径上的方法要小：一个本该内联的方法因为过长没内联，调用开销和后面所有依赖内联的优化会一起丢掉。
