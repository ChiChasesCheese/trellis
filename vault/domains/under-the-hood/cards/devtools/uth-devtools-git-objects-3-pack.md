---
id: uth-devtools-git-objects-3-pack
node: devtools.git-objects
type: qa
step: 3
---
## Q
**packfile：给相似对象只存差量**｜Git · pack-objects

一个大文件每次改一行，提交 100 次，仓库为什么没膨胀 100 倍？

## A
**结构。** 打包时 `git pack-objects` 把对象排序，在滑动窗口内找最相似的对象，只存差量（delta）：`OFS_DELTA` 记基对象的相对偏移，`REF_DELTA` 记基对象的哈希。

**细节。**

- 排序依次按：类型、文件名哈希、大小（大的在前），同名的 blob 就排到了一起
- 默认窗口 `pack.window` 是 10，差量链最长 `pack.depth` 是 50
- 差量内容是两种指令：从基对象复制一段区间；插入新数据

**为什么。** 窗口越大越省空间，但打包越慢、越吃内存，默认值是折中；git 不追踪文件，只靠相似度找基对象。

**对应 LeetCode：** LC 72 编辑距离 · LC 583 两个字符串的删除操作
