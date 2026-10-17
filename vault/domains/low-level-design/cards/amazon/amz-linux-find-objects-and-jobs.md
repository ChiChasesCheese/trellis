---
id: amz-linux-find-objects-and-jobs
node: amazon.amz-linux-find
type: qa
step: 2
tags: [grown]
---
## Q
在 Amazon 文件搜索 API（Linux find）设计里，有哪几个核心类？各自只负责什么？

## A
系统有一棵已存在的目录树，要按条件找出满足的文件。树只存放，过滤器只回答「这个位置满足吗」，搜索器只走树。

- `File` / `Directory` / `Symlink`：三种节点，不存自己的路径。
- `Entry`：遍历时算出的「路径 + 节点 + 深度」。
- `Filter`：只有 `matches(entry) -> bool`，子类是各种条件。
- `FileSearcher`：惰性遍历，只认识 `Filter` 接口。

节点不存路径，因为同一目录可通过符号链接从两个路径到达。
