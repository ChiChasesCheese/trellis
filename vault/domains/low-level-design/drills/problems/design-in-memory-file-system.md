---
nodes: [problems.components.in-memory-file-system, patterns.structural]
tags: [problem]
---
# Drill：内存文件系统（In-Memory File System）

一个进程内的文件系统：目录树，`mkdir`/`ls`/写文件/读文件，后面几关加删除、移动、复制、
搜索。规模是几十万个节点、单个文件可以很大。**这道题看起来是组合模式（Composite）的
标准练习，但真正的分数在于知道这个模式在哪里该停**——文件和目录到底该不该共享一个基类，
决定了后面每一关是变简单还是变啰嗦。照真实机考的节奏分关来做，做完一关再看下一关。

**分关要求**（每关做完再看下一关，像真实的机器编码轮）
- 第 1 关（约 25 分钟）：`mkdir`（自动建中间目录）、`ls`（排序）、写文件/读文件。先想
  清楚路径解析怎么处理根目录本身、结尾的 `/`、`.` 和 `..`，尤其是 `..` 试图越过根目录
  时该怎么办——两种答案都存在，选一种并说出理由。
- 第 2 关（约 20 分钟）：`rm -r`、移动、复制，以及对一棵子树求体积。移动之前想清楚
  “先摘下节点还是先验证目标”哪个更安全；复制一个很大的文件时，复制的应该是内容的引用
  还是一份新的字节，两种答案的代价分别是什么。
- 第 3 关（约 10 分钟）：按通配符搜索文件名。判断现场遍历整棵树和维护一份按名字的索引，
  谁更适合这道题的规模，说得出索引对通配符模式为什么没有对精确匹配那么划算。
- 第 4 关（选做）：在不改动 `File`/`Directory` 定义的前提下，加一个新能力（比如整棵树
  的快照/恢复）。判分点是这个新能力能不能完全复用已有的遍历/复制逻辑。

**怎么练**：把 `vault/domains/low-level-design/problems/in-memory-file-system/starter.py` 的方法体
补全，然后在仓库根目录运行
`IMPL=starter uv run --with pytest python -m pytest vault/domains/low-level-design/problems/in-memory-file-system -q`。

**评分点**
- 认出组合模式在这道题里该在哪里停：`File`/`Directory` 不需要共享一个基类，不需要为了
  接口统一让文件实现"列出子节点"这类对它没有意义的方法
  （[[problems-in-memory-file-system-no-shared-base-class]]）。
- 节点自己不存名字，名字只活在父目录条目表的键里，说得出这和真实文件系统 inode 设计
  的对应关系（[[problems-in-memory-file-system-name-lives-in-parent-entry]]）。
- 节点不存 `parent` 反向引用，路径解析每次从根重新往下走，说得出这为什么让
  `move`/`copy` 不需要同步维护任何指针
  （[[problems-in-memory-file-system-no-parent-pointer-reresolve-from-root]]）。
- 复制一个大文件是 `O(1)`，说得出这个结论依赖 `bytes` 不可变这个前提，以及换成可变类型
  会怎样失效（[[problems-in-memory-file-system-copy-file-is-o1]]）。
- 递归删除子树不需要手写递归，说得出这是垃圾回收语言的免费能力、换成 C++ 会怎样
  （[[problems-in-memory-file-system-recursive-delete-is-free]]）。
- `move` 在真正摘下节点之前先完整验证目标路径，不会在目标非法时丢失数据或者造出环
  （[[problems-in-memory-file-system-move-validate-before-detach]]）。
- 多线程场景下选择给整个文件系统加一把锁，说得出细粒度按目录加锁在 `move` 面前会遇到
  什么死锁风险（[[problems-in-memory-file-system-single-lock-for-move]]）。
- 第 4 关的扩展完全复用已有的复制逻辑，`File`/`Directory` 一行都不改
  （[[problems-in-memory-file-system-snapshot-reuses-duplicate]]）。

**题解**：[[solution-in-memory-file-system]]——先做，再看。

**练习记录**
- [ ] 第 1 次（日期，用时，自评）：
