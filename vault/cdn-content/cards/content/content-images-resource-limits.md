---
id: content-images-resource-limits
node: content.images
type: qa
---
## Q
A 5 MB compressed image expands to several gigabytes during decode and OOMs the worker. Why is upload-byte size insufficient protection?

## A
Compressed size does not bound decoded pixels or intermediate buffers. Validate dimensions, pixel count, frame/page count, format, and decompression ratio before full decode; cap memory, CPU time, output dimensions, and transformation concurrency in an isolated worker. Reject oversized work early and avoid retrying it. Treat image processing as untrusted compute, not a harmless file conversion.

## Q zh
一个 5 MB compressed image 在 decode 时膨胀到数 GB 并 OOM worker。为什么只限制 upload-byte size 不够？

## A zh
compressed size 无法限制 decoded pixel 或 intermediate buffer。full decode 前验证 dimensions、pixel count、frame/page count、format 和 decompression ratio；在 isolated worker 中限制 memory、CPU time、output dimensions 与 transformation concurrency。超限任务尽早 reject，且不要 retry。image processing 是 untrusted compute，不是无害的文件转换。
