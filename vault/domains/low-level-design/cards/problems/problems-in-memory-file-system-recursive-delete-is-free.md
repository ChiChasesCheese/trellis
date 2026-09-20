---
id: problems-in-memory-file-system-recursive-delete-is-free
node: problems.components.in-memory-file-system
type: qa
step: 4
tags: [grown]
---
## Q
用 Python 实现内存文件系统的“递归删除一整棵子树”（类似 `rm -r`），为什么可以只写一行 `del parent.entries[name]`，不需要手写递归去逐个释放子节点？换成 C++ 会有什么不同？

## A
一旦这棵子树不再被任何 `entries` 字典引用，Python 的引用计数会在这一行代码执行完的瞬间，顺着这棵子树自己把它整条链路释放掉——子节点、子节点的子节点，都不需要开发者手写“先删子节点、再删自己”的清理逻辑。这是由垃圾回收（garbage collection）管理内存的语言的免费能力；C++ 这类需要手动管理内存的语言里，组合模式的容器类几乎总要在析构函数里手写“依次删除每个子节点”，否则子树会内存泄漏。要注意的是“复制”不能享受这个免费待遇——复制是构造新数据，不是释放，递归遍历子树、为每一层重新分配新对象没有语言特性能帮你省掉。
