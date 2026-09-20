---
nodes: [problems.components.in-memory-file-system]
url: https://github.com/abhaypaswan/lld-python/tree/main/problems/file-system
---
# abhaypaswan/lld-python — File System

值得读：题库里少见的纯 Python 实现，带 pytest 套件。它让 `File` 和 `Directory` 共享
一个 `FileSystemEntity` 基类（两者都有 `name`、`parent` 字段），是相对标准的组合模式
教材写法。**分歧**：本题解"关键设计决策"第一、二节完整讨论了为什么这道题选择不共享
基类——节点甚至不存自己的名字（名字只存在于父目录 `entries` 字典的键里），也不存
`parent` 反向引用，路径解析全部收在 `FileSystem` 一个类里、每次从根重新往下走；这个
选择的直接好处是 `move`/`copy` 不需要在挂载、拆卸节点时同步维护任何反向引用。
