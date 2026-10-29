---
id: uth-go-rust-rust-collections-2-hashmap
node: go-rust.rust-collections
type: qa
step: 2
---
## Q
**Rust 的 HashMap 为什么既快又防攻击**｜Rust · hashbrown 0.17

标准库 `HashMap` 底下用什么表？默认哈希函数是哪个？

## A
**结构。** 直接用 hashbrown 的瑞士表（SwissTable）：控制字节数组加槽位数组，开放寻址，二次探测。

**细节。**

- 每个槽对应 1 个控制字节：空、已删除，或哈希高 7 位
- x86 的 SSE2 一次扫 16 个控制字节，aarch64 的 NEON 一次扫 8 个
- 负载因子 7/8，实测容量依次为 `3 7 14 28 56 112`
- 默认哈希是 SipHash 1-3，每个 map 随机种子，实测两个 map 遍历顺序不同

**为什么。** SipHash 对整数等短键不是最快，但能抵御哈希洪泛（HashDoS）；要速度可换哈希器。

**对应 LeetCode：** LC 1 两数之和 · LC 560 和为 K 的子数组
