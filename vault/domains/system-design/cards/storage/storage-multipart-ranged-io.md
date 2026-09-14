---
id: storage-multipart-ranged-io
node: storage.object
type: qa
---
## Q
Objects are written and read "whole" — so how do you move a 500GB object through S3 efficiently in both directions?

## A
- **Write: multipart upload** — split into parts (5MB–5GB each, up to 10,000), upload parts **in parallel with per-part retries**, then one CompleteMultipartUpload atomically assembles the object (it never exists half-visible). Required above 5GB; used well below that for parallelism. Failed uploads leave invisible parts that still bill — set a lifecycle rule to abort stale ones.
- **Read: ranged GETs** (`Range: bytes=...`) — fetch arbitrary byte ranges in parallel, or *only* the ranges you need. This is what makes Parquet-on-S3 work: read the footer, then just the needed column chunks — see [[storage-compute-separation]].

Per-request throughput is modest; **parallelism is the whole game** for object-store bandwidth.

## Q zh
对象被整个写和读——所以你如何高效地在两个方向通过 S3 移动一个 500GB 对象？

## A zh
- **写：multipart upload** ——分成部分（每个 5MB–5GB，最多 10,000 个），**并行上传部分并按每部分重试**，然后一个 CompleteMultipartUpload 原子性组装对象（它永远不存在半可见）。5GB 以上需要；在更低下用于并行性。失败的上传留下不可见的部分仍然计费——设置生命周期规则中止陈旧的。
- **读：ranged GET**（`Range: bytes=...`）——并行获取任意字节范围，或**只获取**你需要的范围。这就是 Parquet-on-S3 工作的原因：读页脚，然后只需要的列块——见 [[storage-compute-separation]]。

每请求吞吐是适度的；**并行性是整个游戏**对于对象存储带宽。
