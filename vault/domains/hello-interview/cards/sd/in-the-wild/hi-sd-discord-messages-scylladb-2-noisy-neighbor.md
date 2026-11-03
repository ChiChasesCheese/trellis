---
id: hi-sd-discord-messages-scylladb-2-noisy-neighbor
node: sd.in-the-wild.discord-messages-scylladb.exam
type: qa
step: 2
---
## Q
**Discord 消息：热门频道如何拖慢无关请求**｜系统设计 · 业界案例

为什么一个热门频道会让 Discord 里完全无关的查询也变慢？Cassandra 的读路径和仲裁（quorum）起了什么作用？

## A
**读路径的代价。** Cassandra 写入便宜：追加到提交日志（commit log），写进内存的 memtable，写满后刷成不可变的 SSTable 文件。因为从不原地更新，一行的最新版本可能散在 memtable 和多个 SSTable 里，读取要查多个位置再合并。后台的压实（compaction）定期合并 SSTable，让之后的读要查的文件变少。

**热点放大。** 成千上万读者同时读热门频道最新消息，每个请求都落到同样三个副本上，每个副本都要做同样昂贵的读工作。

**连带效应。** 这三个节点还存着成千上万个冷门频道的分区。Discord 的读写按仲裁级别执行，即每次查询等待三个副本中的两个返回，所以一个节点被某热门频道压垮时，凡是也需要这个节点的无关查询都会排在它后面变慢。

**要点。** 共享节点加仲裁等待，把局部热点变成了对其他分区的噪声邻居（noisy neighbor）问题。
