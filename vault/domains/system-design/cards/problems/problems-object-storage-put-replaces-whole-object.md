---
id: problems-object-storage-put-replaces-whole-object
node: problems.foundations.object-storage
type: qa
step: 2
tags: [grown]
---
## Q
In an S3-style object storage design, a client wants to append a few bytes to the end of an existing 10GB object. Why does the object's API only expose whole-object PUT (no seek-and-write into the middle or append operation), and what does this force the client to do instead?

## A
PUT is defined to replace the entire object atomically: the new version doesn't become visible to GET/List until the whole write completes, and there is no operation that mutates only a byte range of an already-stored object in place. This means the client cannot append in place - it must either download the object, append locally, and PUT the whole 10GB back (expensive for a small append), or restructure its data model to write new, smaller immutable objects over time (e.g. one object per log batch) instead of repeatedly mutating one large object. This whole-object-replacement rule is also why large objects need multipart upload: parts are assembled and only become visible as one unit on a single atomic completion call, not through incremental in-place writes.

## Q zh
在一个 S3 风格的对象存储设计中，客户端想在一个已存在的 10GB 对象末尾追加几个字节。为什么对象的 API 只暴露整体 PUT（没有向中间写入或 append 操作），这迫使客户端只能怎么做？

## A zh
PUT 被定义为原子性地替换整个对象：新版本在整个写入完成前对 GET/List 不可见，且没有任何操作可以只修改已存对象的某个字节范围。这意味着客户端不能就地追加——它必须要么下载整个对象、本地追加、再把整个 10GB 写回去（对小小的追加来说代价很高），要么重新设计数据模型，随时间写新的、更小的不可变对象（例如每批日志一个对象）而不是反复修改一个大对象。这个「整体替换」规则也是大对象需要 multipart 上传的原因：分片被拼装，只在一次原子性的完成调用后才作为一个整体变得可见，而不是通过逐步就地写入。
