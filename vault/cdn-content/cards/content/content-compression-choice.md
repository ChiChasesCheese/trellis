---
id: content-compression-choice
node: content.range-compression
type: qa
---
## Q
Should an edge dynamically Brotli-compress every response at maximum quality?

## A
No. Compression trades CPU and latency for fewer bytes. Precompress immutable static assets at high quality during build; use moderate dynamic levels only for compressible responses above a size threshold. Skip already compressed media and tiny bodies, honor `Accept-Encoding`, and cap concurrency. Compare saved egress and transfer time against CPU cost and p99; maximum ratio is not maximum system performance.

## Q zh
edge 是否应对每个响应都用最高质量动态 Brotli compression？

## A zh
不应。compression 用 CPU 和 latency 换取更少 bytes。immutable static asset 在 build 时以高质量 precompress；动态响应仅在可压缩且超过 size threshold 时使用中等 level。跳过已压缩 media 和 tiny body，遵守 `Accept-Encoding` 并限制 concurrency。比较节省的 egress/transfer time 与 CPU/p99 成本；最大 compression ratio 不等于最大系统性能。
