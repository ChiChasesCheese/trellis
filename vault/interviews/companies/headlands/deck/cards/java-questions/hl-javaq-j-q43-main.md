---
id: hl-javaq-j-q43-main
node: java-questions.j-storage
type: qa
step: 1
---
## Q
对文件 `write()` 时发生什么？什么是 page cache 和 `fsync`？怎么让写既持久又快？
What happens when you `write()` to a file? What are the page cache and `fsync`? How do you make writes durable and fast?

## A
一句话：`write()` 只是把数据拷进内核 **page cache** 就返回（很快，但还没落盘，断电会丢）；`fsync` / `FileChannel.force()` 才等待数据到达持久介质（慢，毫秒级）。

- `write()` 后数据在 page cache 里，标记 dirty；读也先查这里（命中很快）；内核稍后回写到磁盘 / SSD。
- `force()` / `fsync`：等 dirty 页 + 元数据真正写到设备并确认，这一步才耐久。
- 做法：**批量写 + 组提交**（group commit，很多记录共享一次 fsync）；**顺序追加**（WAL，write-ahead log）而不是随机写；预分配文件；只在 sync 之后才确认。
- 只有 OS 崩溃 / 断电才丢未 fsync 的数据；进程崩溃但 OS 没崩，page cache 里的数据不丢。
