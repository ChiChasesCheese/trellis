---
id: hl-javaq-j-q44-main
node: java-questions.j-storage
type: qa
step: 4
---
## Q
文件访问用 `mmap` 还是 `read/write`？什么时候用 `MappedByteBuffer`，有哪些坑？
`mmap` vs `read/write` for files: when would you use a `MappedByteBuffer`, and what are its pitfalls?

## A
一句话：`mmap` 把文件的 page cache 页直接映射进进程地址空间，访问像读内存（缺页时才读盘），省去 `read` 的一次内核到用户拷贝，适合**大文件随机访问**和**多进程共享**。

- `read()`：磁盘 → page cache → 拷贝 → 你的 buffer，每次一次系统调用 + 一次拷贝。
- `mmap`：页在内存就是普通内存访问；不在就缺页，内核读入。
- 实测 2000 条记录写入映射区再 `force()` 用 16 ms，与批量写加一次 force（30 ms）同一量级——写的都是 page cache。
- 顺序读大文件时 `read` + 预读也很好，mmap 不一定更快，要测。
