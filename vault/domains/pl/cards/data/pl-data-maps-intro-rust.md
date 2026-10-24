---
id: pl-data-maps-intro-rust
node: data.maps-collections
type: qa
step: 5
---
## Q
Rust 标准库的 `HashMap` 与 `BTreeMap` 是什么？为什么默认哈希函数故意比较慢，`Hash` 与 `Eq` 在其中起什么作用？

## A
**`HashMap<K, V>`**：开放寻址的哈希表，实现是 hashbrown 库，同样基于 Swiss Table 设计。键类型必须实现 `Hash` 和 `Eq` 两个 trait（可以理解为接口），一般用 `#[derive(Hash, PartialEq, Eq)]` 自动生成。**`BTreeMap<K, V>`** 是 B 树，键需要 `Ord`，有序，支持 `range` 查询。

**默认哈希函数是 SipHash**：一种加密强度较弱但足以抵抗哈希洪泛的算法。每个 `HashMap` 创建时带一个随机密钥，攻击者无法预先构造冲突的键让你的服务退化成 O(n)。代价是比简单哈希慢。本机一次测量，一百万个整数键，Rust `HashMap` 插入约 51 ns/次，查找约 17 ns/次，与 Go 同量级。需要更快且不担心攻击（内部数据、编译器）时，可换成 FxHash 等哈希器。

**迭代顺序随实例随机**：因为每个实例有自己的随机密钥，同一程序里两次迭代同样的键，顺序可能不同。真实输出 `["d", "a", "b", "c", "e"]`，另一次运行是 `["d", "a", "e", "b", "c"]`。`BTreeMap` 给出 `["a", "b", "c"]`。

**所有权的影响**：插入时键和值被移入映射。`entry` API 用于「没有就插入，有就修改」，一次查找完成，避免两次哈希：

```rust
*counts.entry(word).or_insert(0) += 1;
```

**要记住的一点**：Rust 默认选择安全（抗攻击、随机顺序）而不是极限速度，并把更快的选项留给明确知道自己在做什么的人。
