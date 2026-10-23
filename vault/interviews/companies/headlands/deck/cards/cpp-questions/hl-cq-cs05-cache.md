---
id: hl-cq-cs05-cache
node: cpp-questions.cheatsheet
type: qa
step: 5
---
## Q
一句话背诵：缓存局部性的数字——400 万 `int` 的 `vector`、`list`、乱序链表扫描各多久，SoA 比 AoS 快多少？

## A
- CPU 一次读 **64 字节**缓存行。
- 400 万 `int`：`vector` **0.2 ms**，`list` **4.4 ms**，节点乱序的链表 **28 ms**。
- 只用一个字段时，SoA 比 AoS 快约 **10 倍**。
