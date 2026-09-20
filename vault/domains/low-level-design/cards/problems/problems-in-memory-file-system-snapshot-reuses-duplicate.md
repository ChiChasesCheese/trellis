---
id: problems-in-memory-file-system-snapshot-reuses-duplicate
node: problems.components.in-memory-file-system
type: qa
step: 8
tags: [grown]
---
## Q
内存文件系统的第 4 关要求“在不改动 `File`/`Directory` 节点模型的前提下”加一个新能力，为什么“给整棵树拍一个快照、之后可以恢复”比“加一套权限系统”更能满足这条约束？

## A
权限系统天然需要往 `File`/`Directory` 里加新字段（比如 owner、mode），并且要在每一个读写操作里插入一次鉴权检查——`File`/`Directory` 的定义和文件系统门面类的每个方法都要改。快照/恢复不需要新增任何字段：它做的事情和“复制一个目录”完全一样，都是深拷贝一棵子树，区别只是拍快照时复制的对象是整棵树的根，而不是某个子路径——`snapshot()` 可以直接复用“复制目录”已经写好的那个递归复制函数，`File`/`Directory` 两个类因此一行都不需要改，这正是任务书要求的“不碰节点模型”的字面意思。
