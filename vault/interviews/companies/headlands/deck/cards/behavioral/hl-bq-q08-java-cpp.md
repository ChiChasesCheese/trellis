---
id: hl-bq-q08-java-cpp
node: behavioral.question-bank
type: qa
step: 17
---
## Q
Java 和 C++ 你什么时候选哪个？（≤ 60 秒）
Java vs C++: when would you choose which?

## A
- **C++**：**确定性的内存与布局**、没有 GC 暂停、能控制**缓存行为**，在**热路径**上重要。
- **Java**：**生产力**、内存安全、生态，而且 **JIT** 在稳态代码上能接近 C++；代价是 **GC**、**预热（warm-up）**、**对象布局**。
- **按瓶颈选**：**平台与工具 → Java**；**微秒敏感路径 → C++**。

被追问 GC / JIT / 逃逸分析（escape analysis）：说到你会的那层，"below that I'd measure or read the docs."
