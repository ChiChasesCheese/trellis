---
id: problems-in-memory-file-system-name-lives-in-parent-entry
node: problems.components.in-memory-file-system
type: qa
step: 2
tags: [grown]
---
## Q
在一个用组合模式实现的内存文件系统里，为什么 `File`/`Directory` 节点本身可以完全不存自己的名字（`name` 字段），“名字”这个信息应该放在哪里？

## A
名字应该只存在于父目录 `entries` 字典的键里，不需要作为节点自己的属性——这和真实文件系统的 inode 设计是同一个道理：inode 记录内容和元数据，名字属于目录项（directory entry），不属于 inode 本身，所以同一个 inode 才能同时拥有多个名字（硬链接）。节点不存名字的直接好处是：`move`（改名或换位置）只需要把它从旧目录的字典里摘下、放进新目录字典的新键下，节点自身不需要任何改动；如果节点自己存着 `name` 字段，`move` 还要额外同步更新这个字段，多一处必须记得同步的地方。
