---
id: problems-in-memory-file-system-no-parent-pointer-reresolve-from-root
node: problems.components.in-memory-file-system
type: qa
step: 3
tags: [grown]
---
## Q
内存文件系统的路径解析逻辑（把 `/a/b/c` 这样的字符串走到对应节点），应该让每个 `Directory` 节点自己存一个 `parent` 指针、自己知道怎么往上找，还是每次都从根节点重新往下走一遍？为什么？

## A
应该每次从根节点重新往下走，不给节点存 `parent` 指针。给节点存 `parent` 需要在每一次“挂载”和“拆卸”节点时同步维护它——`move` 要更新被移动节点的 `parent`，`copy` 复制出来的新节点的 `parent` 该指向哪里也是一个容易出错的问题（指向复制之前的位置是错的，不设置又会让“这个节点的父节点是谁”出现真假两种状态）。从根节点重新解析的代价是 `O(路径深度)`，这和真实文件系统的做法一致（`open` 一个路径同样要从挂载点逐段往下查找），换来的好处是节点永远不需要知道“我在哪”，`move`/`copy` 因此不需要更新任何反向引用。
