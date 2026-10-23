---
id: hl-cq-q06-aos-vs-soa
node: cpp-questions.a-why-fast
type: qa
step: 33
---
## Q
只对结构体里的 `qty` 一个字段求和：结构体数组（array of structs，AoS）和数组结构体（struct of arrays，SoA）差多少？什么时候反过来 AoS 更好？

## A
- 实测：AoS（每元素 64 字节）约 **1.2 ms**；SoA（只存一个 `vector<int>`，每元素 4 字节）约 **0.1 ms**，约快 10 倍。
- 原因：SoA 一条缓存行装 **16** 个 `qty`，AoS 只装 **1** 个；SoA 还能被 SIMD 向量化。
- 反过来：如果每次都要用到**全部字段**，AoS 更好，一条缓存行带来所有数据。
