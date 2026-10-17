---
nodes: [amazon.amz-linux-find, patterns.structural, oop.interfaces]
tags: [problem]
---
# Drill：Linux find 命令 API（File Search API）

给一棵已经存在的目录树，写一个 `find`：按大小、后缀、名字等条件搜索文件，接口要干净、可扩展。规模是几十万个节点；要求“新增一种条件，改几处代码”的答案是“零处”。

**分关要求**（每关做完再看下一关，像真实的机器编码轮）
- 第 1 关（约 20 分钟）：按大小、格式、名字搜索，如“大于 5MB 的文件”“所有 XML 文件”。写出 `File` / `Directory`、`Filter` 抽象基类和 `Extension`、`Size`、`NameGlob`，以及遍历函数。
- 第 2 关（约 15 分钟）：条件组合 AND / OR / NOT。不许为每种组合写一个类；写出 `Extension("xml") & Size.over("5MB")`，并说清楚“大于 5MB”是否包含恰好 5MB。
- 第 3 关（约 15 分钟）：现场新增一种条件（空目录或修改时间），证明遍历代码和已有过滤器零修改；再让结果变成惰性迭代器，取第一个结果就停。
- 第 4 关（选做）：符号链接环：默认不跟随；跟随时不能死循环，也不能漏掉合法的第二条路径。再说怎么搜真实磁盘。

**怎么练**：把 `vault/domains/low-level-design/problems/amz-linux-find/starter.py` 的方法体补全，然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/amz-linux-find -q`。

**评分点**
- 开场问出内存或磁盘、是否要 OR / NOT、返回方式三个问题（[[amz-linux-find-how-it-is-asked]]）。
- 节点、位置、条件、搜索器各管一件事，节点不存路径（[[amz-linux-find-objects-and-jobs]]）。
- 条件是可组合的对象树，而不是参数列表或组合类爆炸（[[amz-linux-find-specification-filter-tree]]、[[amz-linux-find-common-mistake-all-combinations]]）。
- 遍历集中在一处，不把搜索写进每个节点（[[amz-linux-find-traversal-and-judgement-separate]]）。
- 新增条件只加一个子类（[[amz-linux-find-follow-up-new-condition]]）。
- 边界说清：严格大于、后缀取最后一段、`~` 会选中目录（[[amz-linux-find-size-and-extension-edge-cases]]）。
- 生成器加显式栈，用祖先链而不是全局 visited 防环（[[amz-linux-find-lazy-walk-and-symlink-loops]]）。

**题解**：[[solution-amz-linux-find]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
