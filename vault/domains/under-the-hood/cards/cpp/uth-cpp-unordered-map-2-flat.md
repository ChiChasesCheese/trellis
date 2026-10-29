---
id: uth-cpp-unordered-map-2-flat
node: cpp.unordered-map
type: qa
step: 2
---
## Q
**为什么 flat_hash_map 比 unordered_map 快**｜C++ · Abseil Swiss table

同样是 O(1) 的哈希表，`absl::flat_hash_map` 为什么常常快好几倍？

## A
**结构。** 开放寻址（open addressing）：一整块数组，先是每槽一字节的控制字节，后面是紧挨着的槽位。

**细节。**

- 查找时先在控制字节里一次比较一整组槽，命中才去读元素
- `unordered_map` 要走“桶数组 → 节点 → 比较 key”，至少两次随机内存访问
- 大表的最大负载因子是 7/8，空间也更省

**为什么。** 缓存友好、没有逐元素分配；代价是放弃指针稳定。

**坑。** `flat_hash_map` 在 rehash 或被移动后，元素的指针和引用全部失效。

**对应 LeetCode：** LC 560 和为 K 的子数组 · LC 128 最长连续序列
