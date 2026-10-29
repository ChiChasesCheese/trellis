---
id: uth-cpp-unordered-map-3-identity-hash
node: cpp.unordered-map
type: qa
step: 3
---
## Q
**int 的哈希为什么能被攻击**｜C++ · libstdc++ / libc++

怎样构造一批 `int` key，让 `unordered_map` 的每次操作都退化成 O(n)？

## A
**结构。** 桶号 = `hash(key) % 桶数`，而 `std::hash<int>` 是恒等函数。

**细节。**

- 实测：`hash(5)` 就是 5，`hash(123456)` 就是 123456
- 桶数是质数 97，把 50 个 97 的倍数插进去，实测全落进同一个桶，最长链 50
- 知道桶数的人（或在线评测的恶意数据）就能这样构造

**为什么。** 恒等哈希几乎零成本，质数取模能打散 1024 的倍数这类常见规律；但它不防刻意构造的输入。

**坑。** 面对对抗数据，换成带随机种子的哈希（如 splitmix64 加时间戳）。

**对应 LeetCode：** LC 1 两数之和 · LC 217 存在重复元素
