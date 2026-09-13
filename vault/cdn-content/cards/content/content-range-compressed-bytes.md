---
id: content-range-compressed-bytes
node: content.range-compression
type: qa
---
## Q
Can a server take a byte range of the uncompressed file and then gzip only that slice while claiming it is a range of the gzip representation?

## A
No. Byte ranges apply to the selected representation, including its content coding. Offsets in identity bytes do not match offsets in a gzip stream. Either serve ranges over an identity representation, range a precompressed seekable representation with correct metadata, or ignore `Range` and return a full response. Keep validators and `Content-Length` specific to each encoded variant.

## Q zh
server 能否先截取 uncompressed file 的 byte range，再只 gzip 该片段，却声称它是 gzip representation 的一个 range？

## A zh
不能。byte range 针对 selected representation，包括它的 content coding。identity bytes 的 offset 与 gzip stream 的 offset 不一致。应对 identity representation 提供 range，或对可 seek 的 precompressed representation 按正确 metadata 提供 range；否则忽略 `Range` 并返回完整响应。validator 和 `Content-Length` 必须针对每个 encoded variant。
