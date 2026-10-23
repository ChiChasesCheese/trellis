---
id: hl-hc07-low-bits-fibonacci
node: problems.hc07-ticker-hash-map
type: qa
step: 3
---
## Q
为什么下标不能直接写 `hashCode() & mask`？斐波那契哈希（Fibonacci hashing）怎么写，为什么取高位？

## A
`h & 7` 只有字符串最后一两个字符起作用，真实 hashCode 的低位分布并不均匀。例：`AAPL` 2001436、`MSFT` 2375924、`TSLA` 2584628 的 `& 7` 都是 4，五个代码里三个都想住 4 号格。

两类办法：
- **混合**（mix）：先把高位搅进低位，`java.util.HashMap` 用 `h ^ (h >>> 16)`；
- **乘法哈希 / 斐波那契哈希**：乘一个特殊奇数常数然后**取高位**：
```java
private int home(String key) { return (key.hashCode() * 0x9E3779B9) >>> shift; }  // shift = 32 - log2(容量)
```
`0x9E3779B9 ≈ 2³² / 黄金比例 1.618…`。乘法让输入的**每一位**都影响乘积的**高位**，取高位就拿到混合最好的几位；黄金比例让相邻整数乘完均匀散布（三距离定理）。容量 8 时五个代码得 `AAPL→3, MSFT→6, GOOG→2, AMZN→3, TSLA→7`，只剩一对撞。对 17576 个三字母代码，最长探测距离只有 0 或 1。`>>>` 是无符号右移，保证结果非负且在 `0..容量-1`。64 位 key：`(key * 0x9E3779B97F4A7C15L) >>> (64 - log2(容量))`。

打包后的 key 低位全是补的 0，`key & mask` 对短代码完全没用：17576 个三字母代码最长探测距离 **17575**，乘法哈希只有 0 或 1。C++ 里 `std::hash<整数>` 在 libc++ 和 libstdc++ 都是**恒等函数**，所以 `hash & mask` 同样是灾难。
