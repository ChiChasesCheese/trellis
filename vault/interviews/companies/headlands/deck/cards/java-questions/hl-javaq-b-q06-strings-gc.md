---
id: hl-javaq-b-q06-strings-gc
node: java-questions.b-versions
type: qa
step: 6
---
## Q
Java 8 到 21：默认 GC、字符串内存布局、字符串拼接的实现各自怎么变了？给出紧凑字符串（compact strings）的具体字节数。

## A
- **默认 GC**：8 是 Parallel GC（吞吐优先，停顿长）；9 起默认 **G1**；ZGC 15 起正式，21 起可 `-XX:+ZGenerational`。
- **字符串内存**：8 里是 `char[]`，每字符 2 字节；9 起**紧凑字符串**，Latin-1 字符只用 1 字节。例：`"a".repeat(1000)` = **1040 字节**，`"中".repeat(1000)` = **2040 字节**。
- **字符串拼接**：8 是编译期生成 `StringBuilder` 链；9 起走 `invokedynamic makeConcatWithConstants`，由运行时选最优策略，用 `javap` 可以看到。
