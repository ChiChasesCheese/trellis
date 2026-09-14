---
id: storage-small-objects-cost
node: storage.object
type: qa
---
## Q
Storing 1 billion 4KB objects in S3 costs far more than the same 4TB as large objects. Where does the money and latency go, and what's the fix?

## A
Object storage prices and performs **per request, not per byte**:

- **Requests dominate**: writing a billion objects ≈ $5k in PUTs alone; every read is a full GET round-trip (~tens of ms) for 4KB; LISTing returns 1,000 keys per call — a full enumeration is a million paged calls.
- Lifecycle transitions and archive tiers also bill per object, and archive tiers have per-object minimum sizes/durations.

Fix: **pack small records into large objects** (Parquet/ORC files, tar-style bundles, or a log-structured layout with an index), targeting ~100MB+ per object, and read records back with ranged GETs — see [[storage-multipart-ranged-io]] and [[analytics-lakehouse-compaction]].

## Q zh
在 S3 中存储 10 亿个 4KB 对象的成本远多于相同的 4TB 作为大对象。钱和延迟去哪了，修复是什么？

## A zh
对象存储定价和执行**按请求，不是按字节**：

- **请求占主导**：写 10 亿对象 ≈ $5k 仅在 PUT；每个读都是 4KB 的完整 GET 往返（~十几毫秒）；LIST 返回每个调用 1,000 个键——完整枚举是一百万个分页调用。
- 生命周期转换和存档层也按对象计费，存档层有每对象最小大小/持续时间。

修复：**把小记录打包进大对象**（Parquet/ORC 文件、tar 风格 bundle 或日志结构化布局加索引），目标 ~100MB+ 每对象，并用 ranged GET 读记录回来——见 [[storage-multipart-ranged-io]] 和 [[analytics-lakehouse-compaction]]。
