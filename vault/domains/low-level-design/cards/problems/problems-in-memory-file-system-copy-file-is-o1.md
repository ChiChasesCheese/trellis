---
id: problems-in-memory-file-system-copy-file-is-o1
node: problems.components.in-memory-file-system
type: qa
step: 5
tags: [grown]
---
## Q
内存文件系统里，把一个 10GB 的大文件复制到另一个路径，为什么可以是 `O(1)` 的操作，而不需要遍历它的内容？这个结论依赖 Python 的什么特性，什么情况下会失效？

## A
文件内容如果用不可变的 `bytes` 存储，复制一个文件只需要创建一个新的 `File` 包装对象，让它的 `content` 字段指向和原文件同一个 `bytes` 对象——两者共享同一份数据不会有风险，因为 `bytes` 不可变，唯一能“改变”一个文件内容的操作是整体替换（创建一份新的 `File` 放回目录），原来那个 `bytes` 对象永远不会被就地修改。这让复制一个文件的代价和文件多大完全无关，只有复制一个目录时才需要为每一层重新构造 `entries` 字典（代价是 `O(子树里的条目数)`）。如果把文件内容换成可变类型（比如可以原地追加的 `bytearray`），这条零拷贝的安全性就不成立了——共享同一个 `bytearray` 的两个“独立”文件会在其中一个被原地修改时一起变。
