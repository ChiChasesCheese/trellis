---
id: tlc-design-in-memory-file-system-4-followup
node: a.design-in-memory-file-system
type: qa
step: 4
---
## Q
**LC 588 设计内存文件系统**｜追问

面试官接着问：（1）文件很大、追加很频繁，怎么避免每次复制整个字符串？（2）再加 `rm(path)` 和 `mv(src, dst)`？（3）多个线程同时访问？

## A
1. **频繁追加**：`content` 改成片段列表 `list[str]`，追加是 `parts.append(content)`，摊还 `O(1)`；读取时 `"".join(parts)`，需要多次读取就把合并结果缓存回单个片段。字符串 `+=` 每次可能复制整个旧内容，累计 `O(n^2)`。
2. **`rm` / `mv`**：`rm` 是走到父节点后 `parent.children.pop(name)`，整棵子树一次摘掉；`mv` 是把子树从旧父节点摘下，再挂到新父节点的 `children[new_name]`，不复制内容，`O(L)`。扁平字典做 `mv` 要改所有以旧路径为前缀的键，`O(总路径数)`，这是树结构的核心优势。移动目录时要拒绝把目录移进它自己的子树。
3. **并发**：最简单是整个文件系统一把读写锁，`ls` / `read` 共享，其余独占。更细的做法是每个目录节点一把锁，沿路径逐级加锁并在拿到下一级后释放上一级（hand-over-hand locking）；`mv` 涉及两个父节点，要按固定顺序（例如路径字典序）加锁，防止死锁。

**Python 提醒**：`sorted(node.children)` 对字典迭代的是键，已经满足 `ls`；若目录项很多且要分页，改存 `sortedcontainers.SortedDict`，或用 `bisect.insort` 维护有序键列表，插入 `O(k)`、读第 `i` 页 `O(1)`。CPython 的 GIL 不保证“检查再创建”这类复合操作原子，多线程仍要自己加锁。
