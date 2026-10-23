---
id: hl-cache-qa-long-vs-list
node: foundations.cpu-cache-locality
type: qa
step: 34
---
## Q
追问：为什么 `long[]` 比 `ArrayList<Long>` 快？

## A
推荐答三点：
1. **内存**：`Long` 是对象，12 字节头加对齐和引用，每元素 28 字节对 8 字节（实测 28.2 对 8.2）。
2. **间接**：遍历要先读引用再跳到对象，对象不在一起就是随机访问、缓存缺失；打乱顺序后慢 **16 倍**。
3. **GC**：10⁷ 个小对象给 GC 增加压力。

而 `long[]` 是一块连续内存，预取器和向量化都能用上。
