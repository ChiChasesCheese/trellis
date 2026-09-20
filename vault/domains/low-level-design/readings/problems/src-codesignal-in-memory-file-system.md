---
nodes: [problems.components.in-memory-file-system]
url: https://github.com/PaulLockett/CodeSignal_Practice_Industry_Coding_Framework/tree/main/practice_assessments/file_storage
---
# CodeSignal Practice — Industry Coding Framework: file_storage

值得读：MIT 许可的公开仓库，复现了 CodeSignal "Industry Coding Assessment" 的一道文件
系统机考题，四个等级逐步给 `simulation.py` 加需求，节奏和本题解"分关递进"的框架一致。
它用一个扁平的 `path -> content` 字典模拟整个文件系统，`ls`/`size` 这类子树操作靠字符串
前缀匹配实现，没有真正的树结构；本题解用组合模式的嵌套 `Directory.entries` 表达真实的
父子关系，`size`/`copy`/`remove` 因此是对树的递归而不是对所有路径的一次线性扫描，代价
换来的是"复制一个目录、改动复制出来的那份不影响原目录"这类需求可以直接靠深拷贝子树
回答，不需要额外发明一套前缀重写逻辑。
