---
id: storage-object-vs-filesystem
node: storage.object
type: qa
---
## Q
What can't you do with S3-style object storage that you can with a filesystem or block store, and why doesn't that matter for its main use cases?

## A
No **partial update**: objects are written whole (PUT replaces; no seek-and-write into the middle), listing is a paged API call rather than a cheap directory read, and first-byte latency is tens of ms, not µs.

Doesn't matter because its targets are **write-once, read-many blobs**: images, video, logs, backups, data-lake files (Parquet), ML artifacts. In exchange you get ~unlimited capacity, 11-nines durability, per-GB pricing, and HTTP access with no capacity planning — which is why "big or cold bytes go to object storage" is the modern default.

## Q zh
什么是你用 S3 风格对象存储无法做但用文件系统或块存储能做的，为什么这对它的主要用例不重要？

## A zh
无**部分更新**：对象被整个写（PUT 替换；在中间无 seek-and-write），列出是一个分页 API 调用而不是便宜的目录读，首字节延迟是十几毫秒，不是微秒。

不重要是因为它的目标是**一写多读 blob**：图像、视频、日志、备份、数据湖文件（Parquet）、ML 工件。作为交换你获得 ~无限容量、11-nines 持久性、每 GB 定价、HTTP 访问无容量规划——这就是"大或冷字节走对象存储"是现代默认的原因。
