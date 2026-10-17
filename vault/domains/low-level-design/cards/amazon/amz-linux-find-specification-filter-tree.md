---
id: amz-linux-find-specification-filter-tree
node: amazon.amz-linux-find
type: qa
step: 4
tags: [grown]
---
## Q
在 Linux find 文件搜索设计里，条件为什么做成可组合的 Filter 对象树，而不是 find(name, ext, min_size, ...) 的参数列表？

## A
参数列表每加一个条件就要改签名和函数体，参数之间只能是 AND，OR 和 NOT 无处可放。

`Filter` 对象树（规约模式 Specification + 组合模式 Composite）：叶子条件是一个类，`AndFilter` / `OrFilter` / `NotFilter` 持有子过滤器，`& | ~` 返回新对象、不改原对象。

`Extension("py") & Size(min_bytes=1024)` 求值时左边为假就不求右边（短路），所以便宜的条件放左边。新增条件只加一个子类，`FileSearcher` 零处修改。
