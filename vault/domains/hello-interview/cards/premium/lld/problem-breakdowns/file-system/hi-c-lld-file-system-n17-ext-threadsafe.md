---
id: hi-c-lld-file-system-n17-ext-threadsafe
node: lld.problem-breakdowns.file-system.notes
type: qa
step: 17
---
## Q
**内存文件系统 · 扩展一：线程安全（竞态与粗粒度锁）**｜摘要 · 追问

两个线程同时创建同一个文件会怎样？最简单的修法是什么？

## A
- **竞态：** 线程 A、B 都解析出 `/home`，都检查"有没有 `notes.txt`"得到"没有"，都去添加；结果要么 B 悄悄覆盖 A（丢数据），要么破坏数据结构。
- **本质：** 检查（`has_child`）和动作（`add_child`）不是一个原子步骤，别的线程能插在中间（先检查后操作，check-then-act）。
- **粗粒度锁：** 每个公开方法都在文件系统对象的一把锁里执行；B 要等 A 完成才能开始检查，竞态消失。
- **代价：** 简单且正确，但限制并发：在 `/home/alice` 和 `/home/bob` 里分别建文件，本来互不相干，也要互相等。
- **面试范围内：** 粗粒度通常足够；提到细粒度存在即可。
