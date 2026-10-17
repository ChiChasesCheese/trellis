---
id: amz-linux-find-lazy-walk-and-symlink-loops
node: amazon.amz-linux-find
type: qa
step: 8
tags: [grown]
---
## Q
在 Linux find 文件搜索设计里，遍历为什么用生成器加显式栈？跟随符号链接时怎么检测环？

## A
生成器让调用方 `next(...)` 取第一个结果就停，不必走完整棵树；显式栈不受 Python 约 1000 层递归上限限制（3000 层目录链也能搜）。

环检测用「祖先目录链」，不用全局 visited：

```python
if id(node) in ancestors:
    continue                      # 走回了自己的祖先，才是环
chain = ancestors | {id(node)}    # 子节点带着这条链
```

全局 visited 会漏掉合法的第二条路径：`/alias -> /a` 与 `/a` 都该报告 `x.txt`。默认不跟随链接，链接当叶子。
